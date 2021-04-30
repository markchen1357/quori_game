from flask import render_template, flash, redirect, url_for, request, Response
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO, emit
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, TrialForm, DemoForm, ConsentForm, TrainingForm, SurveyForm
from app.models import User, Trial, Demo, Survey, Condition
from app.params import *
from utils import rules_to_str, str_to_rules
import numpy as np
from datetime import datetime
import time
from wand.image import Image
import os

PATH_TO_TEST_IMAGES_DIR = './images'
PATH_TO_EXTRACTION = '/mnt/d/users/chenm/OpenFace/build/bin/'
socketio = SocketIO(app, cors_allowed_origins = '*')
image_data = open('image_data.csv', 'w')
with open('./app/static/template.csv', 'r') as f:
    headers = f.readlines()
    image_data.write(headers[0])
    


@socketio.on('connect')
def handle_connect():
    print('Client {} connected'.format(request.sid))
    #clients.append(request.sid)
    socketio.emit('connected')
   
@socketio.on('send image')
def image(json, methods = ['GET', 'POST']):
    print('image received from client {}'.format(request.sid))
    i = json['image']  # get the image
  
    pic_id = time.strftime("%Y%m%d-%H%M%S") #unique id
    with Image(blob = i) as img:
        img.save(filename = './images/{}.jpg'.format(pic_id))

    # extract features
    os.system('{}FaceLandmarkImg -f \"./images/{}.jpg\"'.format(PATH_TO_EXTRACTION, pic_id))
    os.rename('./processed', './features/{}'.format(pic_id))
    
    with open('./features/{}/{}.csv'.format(pic_id, pic_id)) as f:
        data = f.readlines()
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_data = '{}, {}'.format(dt_string, data[1])
        image_data.write(write_data)
    return Response("%s saved" % pic_id)

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)
    num_rounds = len(current_condition.difficulty)
    
    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)

    completed = []
    for round in range(num_rounds):
        completed.append([])
        rule_name = current_condition.difficulty[round]
        
        demo_cards = RULE_PROPS[rule_name]['demo_cards']
        num_completed_demos = db.session.query(Demo).filter_by(user_id=current_user.id, round_num=round).count()
        if num_completed_demos < len(demo_cards):
            completed[round].append(False)
        else:
            completed[round].append(True)
        
        cards = RULE_PROPS[rule_name]['cards']
        num_completed_trials = db.session.query(Trial).filter_by(user_id=current_user.id, round_num=round).count()
        if num_completed_trials < len(cards):
            completed[round].append(False)
        else:
            completed[round].append(True)
        
        num_completed_surveys = db.session.query(Survey).filter_by(user_id=current_user.id, round_num=round).count()
        if num_completed_surveys < 1:
            completed[round].append(False)
        else:
            completed[round].append(True)

    #Check whether final survey is done
    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)
    num_rounds = len(current_condition.difficulty)
    num_completed_surveys = db.session.query(Survey).filter_by(user_id=current_user.id, round_num=num_rounds-1).count()
    if num_completed_surveys < 1:
        completed = False
    else:
        completed = True

    return render_template("index.html",
                           title="Home Page",
                           completed=completed,
                           code=current_user.code)

@app.route("/consent", methods=["GET", "POST"])
@login_required
def consent():
    form = ConsentForm()
    if form.validate_on_submit():
        current_user.consent = 1
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.ethnicity = form.ethnicity.data
        current_user.education = form.education.data
        current_user.robot = form.robot.data
        db.session.commit()
        redirect(url_for("training"))
    if current_user.consent:
        flash("Consent completed!")
        return redirect(url_for("training"))
    else:
        return render_template("consent.html", title="Consent", form=form)

@app.route("/training", methods=["GET", "POST"])
@login_required
def training():
    form = TrainingForm()
    if form.validate_on_submit():
        current_user.training = 1
        db.session.commit()
        redirect(url_for("demos", round=0))
    if current_user.training:
        # flash("Training already completed!")
        return redirect(url_for("demos", round=0))
    elif not current_user.consent:
        # flash("Consent not yet completed!")
        return redirect(url_for("consent"))
    else:
        return render_template("training.html", title="Training", form=form, consent=current_user.consent)

@app.route("/demos/<int:round>", methods=["GET", "POST"])
@login_required
def demos(round):
    form = DemoForm()
    
    num_completed_demos = db.session.query(Demo).filter_by(user_id=current_user.id, round_num=round).count()
    
    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)
    rule_name = current_condition.difficulty[round]
    rule = RULE_PROPS[rule_name]['rule']
    demo_cards = RULE_PROPS[rule_name]['demo_cards']
    demo_answers = RULE_PROPS[rule_name]['demo_answers']
    
    previous_cards = [[], []]
    for ii in range(num_completed_demos):
        if demo_answers[ii] == 0:
            previous_cards[0].append(demo_cards[ii])
        if demo_answers[ii] == 1:
            previous_cards[1].append(demo_cards[ii])
    if form.validate_on_submit():
        demo = Demo(author=current_user,
                    demo_num=num_completed_demos + 1,
                    round_num=round,
                    card_num=demo_cards[num_completed_demos],
                    correct_bin=demo_answers[num_completed_demos],
                    rule_set=rule)
        db.session.add(demo)
        db.session.commit()
        return redirect(url_for('demos', round=round, consent=current_user.consent))

    if num_completed_demos == len(demo_cards):
        return redirect(url_for("trials",round=round, consent=current_user.consent))
    
    #Check if previous thing is done

    #If first round, training must be done
    if (round == 0) and (not current_user.training):
        return redirect(url_for("consent"))
    
    #If not first round, previous survey must be done
    if round > 0:
        check_previous_surveys = db.session.query(Survey).filter_by(user_id=current_user.id, round_num=round-1).count()
        if check_previous_surveys < 1:
            return redirect(url_for("consent"))

    #Pick the video to play
    feedback_counts = current_user.feedback_counts
    cur_names = []
    cur_counts = []
    for vid_name in NEUTRAL:
        cur_names.append(vid_name)
        cur_counts.append(feedback_counts[vid_name])
    cur_counts = np.array(cur_counts)
    if np.sum(cur_counts) == 0:
        p = np.ones_like(cur_counts)/np.sum(np.ones_like(cur_counts))
    else:
        p= 1 - cur_counts/np.sum(cur_counts)
    for ii in range(len(p)):
        if p[ii] < 0.05:
            p[ii] = 0.05
    p = p / np.sum(p)
    vid_choice = np.random.choice(np.arange(cur_counts.shape[0]), p= p)
    vid_name = cur_names[vid_choice]
    
    new_feedback_counts = {}
    for new_vid_name in VIDEO_LIST:
        if new_vid_name == vid_name:
            new_feedback_counts[new_vid_name] = feedback_counts[new_vid_name] + 1
        else:
            new_feedback_counts[new_vid_name] = feedback_counts[new_vid_name]

    current_user.feedback_counts = new_feedback_counts
    db.session.commit()

    #Render the next demonstration
    return render_template("demos.html",
        title="Demonstrations",
        form=form,
        num_bins=len(rule),
        card=demo_cards[num_completed_demos],
        correct_bin=demo_answers[num_completed_demos],
        num_completed_demos=num_completed_demos + 1,
        num_demos=len(demo_cards),
        previous_cards=previous_cards,
        round=round,
        vid_name=vid_name,
        consent=current_user.consent)

@app.route("/trials/<int:round>", methods=["GET", "POST"])
@login_required
def trials(round):
    start_time = datetime.now().utcnow().isoformat()
    form = TrialForm(start_time=start_time)
    
    num_completed_trials = db.session.query(Trial).filter_by(user_id=current_user.id, round_num=round).count()
    
    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)
    rule_name = current_condition.difficulty[round]
    rule = RULE_PROPS[rule_name]['rule']
    demo_cards = RULE_PROPS[rule_name]['demo_cards']
    cards = RULE_PROPS[rule_name]['cards']
    answers = RULE_PROPS[rule_name]['answers']
    demo_answers = RULE_PROPS[rule_name]['demo_answers']
    
    previous_cards = [[], []]
    for ii in range(len(demo_cards)):
        if demo_answers[ii] == 0:
            previous_cards[0].append(demo_cards[ii])
        if demo_answers[ii] == 1:
            previous_cards[1].append(demo_cards[ii])

    for ii in range(num_completed_trials):
        if answers[ii] == 0:
            previous_cards[0].append(cards[ii])
        if answers[ii] == 1:
            previous_cards[1].append(cards[ii])

    if form.validate_on_submit():
        chosen_bin = int(form.chosen_bin.data[3])
        feedback_chosen = form.feedback_chosen.data
        trial = Trial(author=current_user,
                      trial_num=num_completed_trials + 1,
                      card_num=cards[num_completed_trials],
                      round_num=round,
                      correct_bin=answers[num_completed_trials],
                      chosen_bin=chosen_bin,
                      feedback=feedback_chosen,
                      rule_set=rule,
                      confidence=int(form.confidence.data),
                      switches=int(form.switches.data))
        db.session.add(trial)

        feedback_counts = current_user.feedback_counts
        new_feedback_counts = {}
        for new_vid_name in VIDEO_LIST:
            if new_vid_name == feedback_chosen:
                new_feedback_counts[new_vid_name] = feedback_counts[new_vid_name] + 1
            else:
                new_feedback_counts[new_vid_name] = feedback_counts[new_vid_name]

            current_user.feedback_counts = new_feedback_counts
        
        db.session.commit()
        return redirect(url_for('trials', round=round, consent=current_user.consent))

    if num_completed_trials == len(cards):
        # flash("You have seen all the trials in this round!")
        return redirect(url_for("survey", round=round, consent=current_user.consent))
    
    #Check if previous thing is done, previous demos must be done
    check_rule_name = current_condition.difficulty[round]
    check_previous_demos = db.session.query(Demo).filter_by(user_id=current_user.id, round_num=round).count()
    if check_previous_demos < len(RULE_PROPS[check_rule_name]['demo_cards']):
        return redirect(url_for("consent"))

    #Choose the video to play - neutral
    feedback_counts = current_user.feedback_counts
    cur_names = []
    cur_counts = []
    for vid_name in NEUTRAL:
        cur_names.append(vid_name)
        cur_counts.append(feedback_counts[vid_name])
    cur_counts = np.array(cur_counts)
    if np.sum(cur_counts) == 0:
        p = np.ones_like(cur_counts)/np.sum(np.ones_like(cur_counts))
    else:
        p= 1 - cur_counts/np.sum(cur_counts)
    for ii in range(len(p)):
        if p[ii] < 0.05:
            p[ii] = 0.05
    p = p / np.sum(p)
    vid_choice = np.random.choice(np.arange(cur_counts.shape[0]), p= p)
    neutral_vid_name = cur_names[vid_choice]
    
    new_feedback_counts = {}
    for new_vid_name in VIDEO_LIST:
        if new_vid_name == vid_name:
            new_feedback_counts[new_vid_name] = feedback_counts[new_vid_name] + 1
        else:
            new_feedback_counts[new_vid_name] = feedback_counts[new_vid_name]

    current_user.feedback_counts = new_feedback_counts
    db.session.commit()

    if answers[num_completed_trials] == 0:
        correct_bin = 'bin0'
    else:
        correct_bin = 'bin1'

    #Choose correct video
    current_nonverbal = current_condition.nonverbal[round]
    cur_names = []
    cur_counts = []
    if correct_bin == 'bin0':
        for vid_name in FEEDBACK[current_nonverbal]['CORRECT-LEFT']:
            cur_names.append(vid_name)
            cur_counts.append(feedback_counts[vid_name])
    else:
        for vid_name in FEEDBACK[current_nonverbal]['CORRECT-RIGHT']:
            cur_names.append(vid_name)
            cur_counts.append(feedback_counts[vid_name])
    cur_counts = np.array(cur_counts)
    if np.sum(cur_counts) == 0:
        cur_counts = np.ones_like(cur_counts)
    vid_choice = np.random.choice(np.arange(cur_counts.shape[0]), p=cur_counts/np.sum(cur_counts))
    correct_vid_name = cur_names[vid_choice]

    #Choose incorrect video
    cur_names = []
    cur_counts = []
    if correct_bin == 'bin0':
        for vid_name in FEEDBACK[current_nonverbal]['INCORRECT-LEFT']:
            cur_names.append(vid_name)
            cur_counts.append(feedback_counts[vid_name])
    else:
        for vid_name in FEEDBACK[current_nonverbal]['INCORRECT-RIGHT']:
            cur_names.append(vid_name)
            cur_counts.append(feedback_counts[vid_name])
    cur_counts = np.array(cur_counts)
    if np.sum(cur_counts) == 0:
        cur_counts = np.ones_like(cur_counts)
    vid_choice = np.random.choice(np.arange(cur_counts.shape[0]), p=cur_counts/np.sum(cur_counts))
    incorrect_vid_name = cur_names[vid_choice]

    return render_template("trials.html",
        title="Trials",
        form=form,
        num_bins=len(rule),
        card=cards[num_completed_trials],
        correct_bin=correct_bin,
        num_completed_trials=num_completed_trials + 1,
        num_trials=len(cards),
        previous_cards=previous_cards,
        round=round,
        vid_name=neutral_vid_name,
        correct_vid_name = correct_vid_name,
        incorrect_vid_name = incorrect_vid_name,
        consent=current_user.consent)

@app.route("/survey/<int:round>", methods=["GET", "POST"])
@login_required
def survey(round):
    form = SurveyForm()

    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)
    
    if form.validate_on_submit():
        survey = Survey(author=current_user,
                        round_num=round,
                        difficulty = form.difficulty.data,
                        user_learning = form.user_learning.data,
                        animacy1 = form.animacy1.data,
                        animacy2 = form.animacy2.data,
                        animacy3 = form.animacy3.data,
                        intelligence1 = form.intelligence1.data,
                        intelligence2 = form.intelligence2.data)
        db.session.add(survey)
        db.session.commit()

        if round+1 < len(current_condition.difficulty):
            return redirect(url_for("demos", round=round+1))
        else:
            return redirect(url_for("index"))

    #Check if survey already completed
    check_previous_surveys = db.session.query(Survey).filter_by(user_id=current_user.id, round_num=round).count()
    if check_previous_surveys == 1:
        if round+1 < len(current_condition.difficulty):
            return redirect(url_for("demos", round=round+1))
        else:
            return redirect(url_for("index"))

    #Check if previous thing is done, previous trials must be done
    check_rule_name = current_condition.difficulty[round]
    check_previous_trials = db.session.query(Trial).filter_by(user_id=current_user.id, round_num=round).count()
    if check_previous_trials < len(RULE_PROPS[check_rule_name]['cards']):
        return redirect(url_for("consent"))
    
    return render_template("survey.html", methods=["GET", "POST"], form=form, round=round)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        cond = user.set_condition()
        code = user.set_code()
        db.session.add(user)
        
        cond.users.append(user)
        cond.count += 1

        feedback = {}
        for vid in VIDEO_LIST:
            feedback[vid] = 0
        
        user.feedback_counts = feedback

        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)