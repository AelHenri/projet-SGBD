#!/usr/bin/python
from flask import Flask,render_template
from flaskext.mysql import MySQL
from flask import jsonify

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'ProjetSGBD'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

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

	query = "SELECT Commentaire, Date_commentaire, Login_eleve FROM Recette NATURAL JOIN Commenter NATURAL JOIN Eleve WHERE Id_recette = '" + Id_recette + "'" 
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

	return render_template('recette.html', recette=recette, commentaires=commentaires, avis=avis, notes=notes, nbavis=NbAvis)

app.run(debug=True)