from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

@app.route("/")
@app.route("/index")
def home():
	return "Hello world !"