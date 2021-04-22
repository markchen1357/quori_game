from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models

##Comment out below when initializing database
# from app.params import CONDITIONS
# rows = db.session.query(models.Condition).count()
# if rows == 0:
#     for condition in CONDITIONS:
#         difficulty = []
#         nonverbal = []
#         for ii in condition:
#             difficulty.append(ii[0])
#             nonverbal.append(ii[1])
#         db.session.add(models.Condition(difficulty=difficulty, nonverbal=nonverbal, count=0))
# db.session.commit()


