#!/usr/bin/python
from flask import Flask,render_template
from flaskext.mysql import MySQL
from flask import jsonify
from flask import request

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

	query = "SELECT Commentaire, Date_commentaire, Nom_eleve FROM Recette NATURAL JOIN Commenter NATURAL JOIN Eleve WHERE Id_recette = '" + Id_recette + "'"
	cursor.execute(query)
	commentaires = cursor.fetchall()

	query = "SELECT * FROM Recette NATURAL JOIN Avis WHERE Id_recette = '" + Id_recette + "'"
	cursor.execute(query)
	avis = cursor.fetchall()
	return render_template('recette.html', recette=recette, commentaires=commentaires, avis=avis)

@app.route("/recherche")
@app.route("/recherche/")
@app.route("/recherche/",methods=['POST'])
def recherche():
	cursor = mysql.connect().cursor()
	categorie_request = ""
	budget_request = ""
	difficulte_request = ""
	duree_request = ""
	keywords_request = ""
	order_request = ""
	if request.method == 'POST':
		if (request.form['categorie'] != "Tous"):
			categorie_request = "AND Recette.Categorie_recette = '" + request.form['categorie'] + "'"
		if (request.form['minsupBud'] != "Tous" and request.form['budget']!= ""):
			budget_request = "AND (Budget "+ request.form['minsupBud']+ request.form['budget'] +")"
		if (request.form['minsupDif'] != "Tous" and request.form['difficulte']!= ""):
			difficulte_request = "AND (Difficulte "+ request.form['minsupDif']+ request.form['difficulte'] +")"
		if (request.form['minsupDur'] != "Tous" and request.form['duree']!= ""):
			duree_request = "AND (( Temps_preparation + Temps_cuisson) "+ request.form['minsupDur']+ request.form['duree'] +")"
		if (request.form['keywords'] != ""):
			tabkeywords = request.form['keywords'].split()
			keywords_request += " AND ( " 
			for word in tabkeywords:
				keywords_request += "((lower(Nom_recette) LIKE '%" +word+"%') OR ((lower(Nom_ingredient) LIKE '%" +word+"%') AND Composer.Categorie_recette = 'principal')) OR "
			keywords_request += " 0 ) "
		order_request = " ORDER BY "+ request.form['tri'] + " " + request.form['order']
		
		query1 = "SELECT distinct Recette.Id_recette, Nom_recette, Nb_personnes, Budget, COUNT(Date_avis), (avg( Note_qualite ) + avg( Note_justesse ) + avg( Note_respect )) /3 AS Note, Url_image, Count(*) FROM Recette LEFT OUTER JOIN Avis ON Recette.Id_recette = Avis.Id_recette LEFT OUTER JOIN Commenter ON Recette.Id_recette = Commenter.Id_recette INNER JOIN Composer INNER JOIN Ingredient where Recette.Id_recette = Composer.Id_recette and Composer.Id_ingredient = Ingredient.Id_ingredient " + categorie_request + budget_request + difficulte_request + duree_request + keywords_request + " GROUP BY Id_recette, Nom_recette, Nb_personnes, Budget, Url_image" + order_request
		cursor.execute(query1)
		recettes = cursor.fetchall()	
		
		query2 = "SELECT count(distinct Nom_recette) FROM Recette LEFT OUTER JOIN Avis ON Recette.Id_recette = Avis.Id_recette LEFT OUTER JOIN Commenter ON Recette.Id_recette = Commenter.Id_recette INNER JOIN Composer INNER JOIN Ingredient where Recette.Id_recette = Composer.Id_recette and Composer.Id_ingredient = Ingredient.Id_ingredient " + categorie_request + budget_request + difficulte_request + duree_request + keywords_request
		cursor.execute(query2)
		nbRecettes = cursor.fetchone()		
		
		return render_template('recherche.html',recettes=recettes,nbRecettes=nbRecettes)
	else:
		return render_template('recherche.html',nbRecettes=None)

	
app.run(debug=True)
