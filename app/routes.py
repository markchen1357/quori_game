from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, TrialForm, DemoForm, ConsentForm, TrainingForm, SurveyForm
from app.models import User, Trial, Demo, Condition
from app.params import *
from utils import rules_to_str, str_to_rules


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)
    num_rounds = len(current_condition.difficulty)

    return render_template("index.html",
                           title="Home Page",
                           consent=current_user.consent,
                           training=current_user.training,
                           num_rounds=num_rounds)

@app.route("/consent", methods=["GET", "POST"])
@login_required
def consent():
    form = ConsentForm()
    if form.validate_on_submit():
        current_user.consent = 1
        db.session.commit()
        redirect(url_for("index"))
    if current_user.consent:
        flash("Consent already completed!")
        return redirect(url_for("index"))
    else:
        return render_template("consent.html", title="Consent", form=form)

@app.route("/training", methods=["GET", "POST"])
@login_required
def training():
    form = TrainingForm()
    if form.validate_on_submit():
        current_user.training = 1
        db.session.commit()
        redirect(url_for("index"))
    if current_user.training:
        flash("Training already completed!")
        return redirect(url_for("index"))
    elif not current_user.consent:
        flash("Consent not yet completed!")
        return redirect(url_for("index"))
    else:
        return render_template("training.html", title="Training", form=form)

@app.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        current_user.robot_teaching = form.robot_teaching.data
        current_user.user_learning = form.user_learning.data
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.ethnicity = form.ethnicity.data
        current_user.education = form.education.data
        current_user.robot = form.robot.data
        db.session.commit()
        redirect(url_for("index"))

    num_completed_trials=current_user.trials.count()
    num_completed_demos=current_user.demos.count()
    if current_user.robot_teaching:
        flash("You have completed the survey!")
        return redirect(url_for("index"))
    else:
        if current_user.consent and num_completed_demos == NUM_DEMOS and num_completed_trials == NUM_TRIALS and current_user.training:
            return render_template("survey.html", methods=["GET", "POST"], form=form)
        else:
            flash("You must complete the modules in order!")
            return redirect(url_for("index"))

@app.route("/trials/<int:round>", methods=["GET", "POST"])
@login_required
def trials(round):
    form = TrialForm()
    
    num_completed_trials = db.session.query(Trial).filter_by(user_id=current_user.id, round_num=round).count()
    
    condition_id = current_user.condition_id
    current_condition = db.session.query(Condition).get(condition_id)
    rule_name = current_condition.difficulty[round]
    rule = RULE_PROPS[rule_name]['rule']
    cards = RULE_PROPS[rule_name]['cards']
    answers = RULE_PROPS[rule_name]['answers']
    
    previous_cards = [[], []]
    for ii in range(num_completed_trials):
        if answers[ii][0]:
            previous_cards[0].append(cards[ii])
        if answers[ii][1]:
            previous_cards[1].append(cards[ii])

    if form.validate_on_submit():
        chosen_bin = int(form.chosen_bin.data[3])
        trial = Trial(author=current_user,
                      trial_num=num_completed_trials + 1,
                      card_num=cards[num_completed_trials],
                      round_num=round,
                      correct_bin=answers[num_completed_trials],
                      chosen_bin=chosen_bin,
                      text_feedback='',
                      nonverbal_feedback='',
                      feedback_type='',
                      rule_set=rule)
        db.session.add(trial)
        db.session.commit()
        return redirect(url_for('trials', round=round))

    if num_completed_trials == len(cards):
        flash("You have seen all the trials in this round!")
        return redirect(url_for("index"))
    else:
        #Check if all previous things have been completed
        previous_completed = True

        #Demo from this round completed
        check_round = round
        check_rule_name = current_condition.difficulty[check_round]

        check_previous_demos = db.session.query(Demo).filter_by(user_id=current_user.id, round_num=check_round).count()
        if check_previous_demos < len(RULE_PROPS[check_rule_name]['demo_cards']):
            previous_completed = False

        if round > 0:
            #All demos, trials, and survey completed from previous rounds
            for check_round in range(round):
                check_rule_name = current_condition.difficulty[check_round]

                check_previous_demos = db.session.query(Demo).filter_by(user_id=current_user.id, round_num=check_round).count()
                if check_previous_demos < len(RULE_PROPS[check_rule_name]['demo_cards']):
                    previous_completed = False
                
                check_previous_trials = db.session.query(Trial).filter_by(user_id=current_user.id, round_num=check_round).count()
                if check_previous_trials < len(RULE_PROPS[check_rule_name]['cards']):
                    previous_completed = False
                
        if not current_user.consent or not current_user.training or not previous_completed:
            flash("You must complete the modules in order!")
            return redirect(url_for("index"))
        
        #Render the next trial
        else:
            return render_template("trials.html",
                title="Trials",
                form=form,
                num_bins=len(rule),
                card=cards[num_completed_trials],
                correct_bin=answers[num_completed_trials],
                num_completed_trials=num_completed_trials + 1,
                num_trials=len(cards),
                previous_cards=previous_cards)
        
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

    if form.validate_on_submit():
        demo = Demo(author=current_user,
                    demo_num=num_completed_demos + 1,
                    round_num=round,
                    card_num=demo_cards[num_completed_demos],
                    correct_bin=demo_answers[num_completed_demos],
                    rule_set=rule)
        db.session.add(demo)
        db.session.commit()
        return redirect(url_for('demos', round=round))

    if num_completed_demos == len(demo_cards):
        flash("You have seen all the demonstrations in this round!")
        return redirect(url_for("index"))
    else:
        #Check if all previous things have been completed
        previous_completed = True

        #All demos, trials, and surveys from previous rounds completed
        if round > 0:
            for check_round in range(round):
                check_rule_name = current_condition.difficulty[check_round]

                check_previous_demos = db.session.query(Demo).filter_by(user_id=current_user.id, round_num=check_round).count()
                if check_previous_demos < len(RULE_PROPS[check_rule_name]['demo_cards']):
                    previous_completed = False
                
                check_previous_trials = db.session.query(Trial).filter_by(user_id=current_user.id, round_num=check_round).count()
                if check_previous_trials < len(RULE_PROPS[check_rule_name]['cards']):
                    previous_completed = False
                
        if not current_user.consent or not current_user.training or not previous_completed:
            flash("You must complete the modules in order!")
            return redirect(url_for("index"))
        
        #Render the next demonstration
        else:
            return render_template("demos.html",
                title="Demonstrations",
                form=form,
                num_bins=len(rule),
                card=demo_cards[num_completed_demos],
                correct_bin=demo_answers[num_completed_demos],
                num_completed_demos=num_completed_demos + 1,
                num_demos=len(demo_cards))

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
        db.session.add(user)
        cond.users.append(user)
        cond.count += 1
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)