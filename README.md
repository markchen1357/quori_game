# robot-teaches-game

## Installation
- Install VS Code
- Do the set-up instructions from https://code.visualstudio.com/docs/python/tutorial-flask starting with the Prerequisites and Create Project Environment sections
- Select Interpretor to the `venv` and `Ctrl + Shift +` ` to open console within the env
```
pip install flask
pip install email-validator
pip install flask-wtf
pip install flask-login
pip install flask-sqlalchemy
pip install flask-migrate
pip install numpy scipy matplotlib pandas pingouin
```
- Create the database using
```
flask db init
flask db migrate -m "user table"
flask db upgrade
flask db migrate -m "trial table"
flask db upgrade
flask db migrate -m "demo table"
flask db upgrade
flask db migrate -m "condition table"
flask db upgrade
```
- Run the app with `python -m flask run`

## Useful Links
- https://stackoverflow.com/questions/56199111/visual-studio-code-cmd-error-cannot-be-loaded-because-running-scripts-is-disabl
- https://github.com/bevacqua/dragula/
- Alt + Shift + F is auto-indent
- Flask Login with Database https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
- DB to CSV with https://www.rebasedata.com/convert-sqlite-to-csv-online