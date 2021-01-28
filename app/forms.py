from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password",
                              validators=[DataRequired(),
                                          EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")


class TrialForm(FlaskForm):
    chosen_bin = StringField()

    def validate_chosen_bin(self, chosen_bin):
        if len(chosen_bin.data) < 3:
            raise ValidationError("Please choose a bin")
        if not (chosen_bin.data[0] == "b"):
            raise ValidationError("Please choose a bin")

    submit_trial = SubmitField("Next Trial")

class ClearTrialForm(FlaskForm):
    submit_trial = SubmitField("Clear all Trials")

class ConsentForm(FlaskForm):
    submit_consent = SubmitField("I have read and understood the information above and want to participate in this research.")

class TrainingForm(FlaskForm):
    submit_training = SubmitField("Got it, I'm ready to begin!")

class DemoForm(FlaskForm):
    submit_demo = SubmitField("Next Demonstration")

class ClearDemoForm(FlaskForm):
    submit_demo = SubmitField("Clear all Demos")

class SurveyForm(FlaskForm):
    
    robot_teaching = RadioField("", choices=[(0, "Strongly Disagree"), (1, "Disagree"), (2, "Neutral"), (3, "Agree"), (4, "Strongly Agree")])
    user_learning = RadioField("", choices=[(0, "Strongly Disagree"), (1, "Disagree"), (2, "Neutral"), (3, "Agree"), (4, "Strongly Agree")])
    age = RadioField("", choices=[(0, "18-24"), (1, "25-34"), (2, "35-44"), (3, "45-54"), (4, "55-64"), (5, "65-74"), (6, "75-84"), (7, "85 or older")])
    gender =  RadioField("", choices=[(0, "Male"), (1, "Female"), (2, "Other")])
    education = RadioField("", choices=[(0, "Less than high school degree"), (1, "High school graduate (high school diploma or equivalent including GED)"), (2, "Some college but no degree"), (3, "Associate degree in college (2-year)"), (4, "Bachelor’s degree in college (4-year)"), (5, "Master’s degree"), (5, "Doctoral degree"), (5, "Professional degree (JD, MD)")])
    ethnicity = RadioField("", choices=[(0, "White"), (1, "Black or African American"), (2, "American Indian or Alaska Native"), (3, "Asian"), (4, "Native Hawaiian or Pacific Islander"), (5, "Other")])
    robot = RadioField("", choices=[(0, "Not at all"), (1, "Slightly"), (2, "Moderately"), (3, "Very"), (4, "Extremely")])
    submit_survey = SubmitField("Submit")

class ClearSurveyForm(FlaskForm):
    submit_survey = SubmitField("Clear Survey Responses")

class ClearConsentForm(FlaskForm):
    submit_consent = SubmitField("Clear Consent")

class ClearTrainingForm(FlaskForm):
    submit_training = SubmitField("Clear Training")
