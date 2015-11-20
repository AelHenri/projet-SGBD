#!/usr/bin/python
from flask import Flask,render_template
from flaskext.mysql import MySQL
from flask import jsonify

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
@app.route("/index")
def index():
	user = {'nickname': 'JeanPierre'}
	posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
	return render_template('index.html',title='Projet SGBD', user=user, posts = posts)


@app.route("/test")
def test():
	user = {'nickname': 'JeanPierre'}
	cursor = mysql.connect().cursor()
	query = "SELECT * FROM User"
	cursor.execute(query)
	data = cursor.fetchall()
	return render_template('test.html',title='Projet SGBD', user=user, data=data)

app.run(debug=True)