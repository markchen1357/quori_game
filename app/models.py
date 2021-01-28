from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    trials = db.relationship("Trial", backref="author", lazy="dynamic")
    demos = db.relationship("Demo", backref="author", lazy="dynamic")
    surveys = db.relationship("Survey", backref="author", lazy="dynamic")

    condition_id = db.Column(db.Integer, db.ForeignKey("condition.id"))

    consent = db.Column(db.Integer)
    training = db.Column(db.Integer)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_condition(self):
        min_count = db.session.query(func.min(Condition.count)).scalar()
        min_cond = db.session.query(Condition).filter_by(count = min_count).first()
        return min_cond

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Trial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    round_num = db.Column(db.Integer)
    trial_num = db.Column(db.Integer)
    card_num = db.Column(db.Integer)
    correct_bin = db.Column(db.PickleType)
    chosen_bin = db.Column(db.Integer)
    text_feedback = db.Column(db.String(300))
    nonverbal_feedback = db.Column(db.String(300))
    feedback_type = db.Column(db.String(20))
    rule_set = db.Column(db.PickleType)


class Demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    round_num = db.Column(db.Integer)
    demo_num = db.Column(db.Integer)
    card_num = db.Column(db.Integer)
    correct_bin = db.Column(db.PickleType)
    rule_set = db.Column(db.PickleType)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    round_num = db.Column(db.Integer)
    robot_teaching = db.Column(db.Integer)
    user_learning = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    ethnicity = db.Column(db.Integer)
    education = db.Column(db.Integer)
    robot = db.Column(db.Integer)

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.PickleType)
    nonverbal = db.Column(db.PickleType)
    count = db.Column(db.Integer)
    users = db.relationship('User', backref='person', lazy="dynamic")
    


