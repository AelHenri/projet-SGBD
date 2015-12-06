#!/usr/bin/python
from flask import Flask,render_template, request, flash, Session, url_for, redirect
from flaskext.mysql import MySQL
from flask import jsonify
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'ProjetSGBD'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['SECRET_KEY'] = 'POOp'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
	"""docstring for User"""
	def __init__(self, login, id, active=True):
		self.login = login
		self.id = id
		self.active = active

		cursor = mysql.connect().cursor()
		query = "SELECT * FROM Eleve WHERE Id_eleve = " + str(id)
		cursor.execute(query)
		eleve = cursor.fetchone()
		self.lastname = eleve[1]
		self.firstname = eleve[2]
		self.date = eleve[4]
		self.pwd = eleve[5]

	def is_active(self):
		return self.active

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

@login_manager.user_loader
def load_user(id):
	cursor = mysql.connect().cursor()
	query = "SELECT * FROM Eleve WHERE Id_eleve = " + id
	cursor.execute(query)
	eleve = cursor.fetchone()
	userLogin = eleve[3]
	return User(userLogin, id)
		

@app.route("/")
@app.route("/index")
@app.route("/index/<categorie>")
def index(categorie=None):
	cursor = mysql.connect().cursor()
	if (categorie == None):
		query = "SELECT Recette.Id_recette, Nom_recette, Nb_personnes, Budget, COUNT(Date_avis), (avg( Note_qualite ) + avg( Note_justesse ) + avg( Note_respect )) /3 AS Note, Url_image FROM Recette LEFT OUTER JOIN Avis ON Recette.Id_recette = Avis.Id_recette GROUP BY Id_recette, Nom_recette, Nb_personnes, Budget, Url_image"
	else:
		query = "SELECT Recette.Id_recette, Nom_recette, Nb_personnes, Budget, COUNT(Date_avis), (avg( Note_qualite ) + avg( Note_justesse ) + avg( Note_respect )) /3 AS Note, Url_image FROM Recette LEFT OUTER JOIN Avis ON Recette.Id_recette = Avis.Id_recette WHERE Recette.Categorie_recette = '" + categorie + "' GROUP BY Id_recette, Nom_recette, Nb_personnes, Budget, Url_image"
	cursor.execute(query)
	recettes = cursor.fetchall()

	return render_template('index.html', recettes=recettes, categorie=categorie)

@app.route("/recette/<Id_recette>")
def recettes(Id_recette):
	cursor = mysql.connect().cursor()
	query = "SELECT * FROM Recette WHERE Recette.Id_recette = '" + Id_recette + "'"
	cursor.execute(query)
	recette = cursor.fetchone()

	query = "SELECT Nom_ingredient, Unite_mesure, Quantite FROM Ingredient,Composer,Recette WHERE Ingredient.Id_ingredient = Composer.Id_ingredient AND Composer.Id_recette = Recette.Id_recette AND Recette.Id_recette = '" + Id_recette + "'"
	cursor.execute(query)
	ingredients = cursor.fetchall()

	query = "SELECT Commentaire, Date_commentaire, Login_eleve FROM Commenter NATURAL JOIN Eleve WHERE Id_recette = '" + Id_recette + "'" 
	cursor.execute(query)
	commentaires = cursor.fetchall()

	query = "SELECT Note_qualite, Note_justesse, Note_respect, Date_avis, Avis_recette, Login_eleve, (Note_qualite+Note_justesse+Note_respect)/3 FROM Avis NATURAL JOIN Eleve WHERE Id_recette = '" + Id_recette + "'"
	cursor.execute(query)
	avis = cursor.fetchall()

	query = "SELECT avg( Note_qualite ), avg( Note_justesse ), avg( Note_respect ), (avg( Note_qualite ) + avg( Note_justesse ) + avg( Note_respect )) /3 FROM Recette LEFT OUTER JOIN Avis ON Avis.Id_recette = '" + Id_recette + "'"
	cursor.execute(query)
	notes = cursor.fetchone()

	query = "SELECT COUNT(Date_avis) FROM Avis WHERE Id_recette = '" + Id_recette + "'"
	cursor.execute(query)
	NbAvis = cursor.fetchone()

	return render_template('recette.html', recette=recette, ingredients=ingredients, commentaires=commentaires, avis=avis, notes=notes, nbavis=NbAvis)


@app.route("/login", methods=['GET', 'POST'])
def login():
	isValidLogin = False
	isValidPassword = False

	cursor = mysql.connect().cursor()
	query = "SELECT * FROM Eleve"
	cursor.execute(query)
	eleves = cursor.fetchall()

	if request.method == "POST" and "username" in request.form:
		login = request.form['username']
		pwd = request.form['password']

		for e in eleves:
			if e[3] == login:
				isValidLogin = True
				if e[5] == pwd:
					isValidPassword = True
					userId = e[0]

		if isValidLogin and isValidPassword:
			validUser = User(login, userId)
			if login_user(validUser):
				return redirect(url_for("index"))
			else:
				return render_template("login.html", error="inconnue")
		elif isValidLogin and not(isValidPassword):
			return render_template("login.html", error="password")
		else:
			return render_template("login.html", error="username")
	return render_template("login.html")

@app.route("/profil/<login>/edit", methods=['GET', 'POST'])
@login_required
def edit_profil(login):
	conn = mysql.connect()
	cursor = conn.cursor()
	query = "SELECT * FROM Eleve"
	cursor.execute(query)
	eleves = cursor.fetchall()

	if request.method == "POST":
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		login = request.form['login']
		pwd = request.form['pwd']
		cpwd = request.form['cpwd']

		if login != current_user.login:
			for e in eleves:
				if login == e[3]:
					return render_template('profile.html', error = "Login deja pris !")

		if pwd != cpwd:
			return render_template('profile.html', error = "Mots de passe differents !")

		query = "UPDATE Eleve SET Nom_eleve = %s, Prenom_eleve = %s, Login_eleve = %s, Mot_de_passe = %s WHERE Id_eleve =" + current_user.id
		cursor.execute(query, (lastname, firstname, login, pwd))
		conn.commit()
		return redirect(url_for('index'))

	return render_template('profile.html', error = None)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	conn = mysql.connect()
	cursor = conn.cursor()
	query = "SELECT * FROM Eleve"
	cursor.execute(query)
	eleves = cursor.fetchall()

	if request.method == "POST":
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		login = request.form['login']
		pwd = request.form['pwd']
		cpwd = request.form['cpwd']

		#if login != current_user.login
		for e in eleves:
			if login == e[3]:
				return render_template('profile.html', error = "Login deja pris !")

		if pwd != cpwd:
			return render_template('profile.html', error = "Mots de passe differents !")

		query = "INSERT INTO Eleve (Nom_eleve, Prenom_eleve, Login_eleve, Mot_de_passe) VALUES(%s, %s, %s, %s)"
		cursor.execute(query, (lastname, firstname, login, pwd))
		conn.commit()
		return redirect(url_for('login'))

	return render_template('profile.html', error = None)

if __name__ == "__main__":
	app.run(debug=True)