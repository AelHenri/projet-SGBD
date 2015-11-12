from app import app
from flask import render_template
from flaskext.mysql import MySQL

mysql = MySQL()

@app.route("/")
@app.route("/index")
def index():
	user = {'nickname': 'JeanPierre'}
	return render_template('index.html',title='Projet SGBD', user=user)