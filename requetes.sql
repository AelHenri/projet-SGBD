-- OK	suppression Eleve -> recette associée id_eleve = null 
-- OK	suppression Eleve -> suppression Commentaires et Avis associés
--		suppression Recette -> suppression Images associées
--


-- liste des recettes utilisant du poivre
select Nom_recette
from Recette, Composer, Ingredient
where Recette.Id_recette = Composer.Id_recette and Composer.Id_ingredient = Ingredient.Id_ingredient and Nom_ingredient = "poivre";

-- moyenne des prix des recettes proposées par un élève donné
select avg(Budget)
from Recette
where Id_eleve = 1;

-- nombres recettes dispo pour chaque catégorie
SELECT count( * )
FROM Recette
WHERE Categorie_recette = "dessert"

-- classement des recettes selon le meilleur rapport qualité/prix
-- (on pourra supposer par exemple qu’une recette non commenté a une note par défaut de 2)
select Recette.Nom_recette, avg(Avis.Note_qualite/Recette.budget) as QualitePrix
from Recette, Avis
where Recette.Id_recette=Avis.Id_recette
group by Recette.Id_recette
order by QualitePrix DESC;


-- classement des desserts les plus rapides à réaliser
select *
from Recette
where Categorie_recette = "Dessert"
order by (Temps_preparation + Temps_cuisson) DESC;


-- classement des plats les plus commentés
select Nom_recette, count(Commentaire) as Nombre_Commentaires
from Recette
left outer join Commenter
on Recette.Id_recette = Commenter.Id_recette
group by Nom_recette
order by Nombre_Commentaires DESC;


-- on souhaite décerner le prix du critique gastronomique le plus fiable :
-- calculer l’élève dont l’écart type des notes à la moyenne de chacun des plats 
-- qu’il a commenté est le plus faible

-- calcul moyenne notes plats
SELECT Nom_recette, avg(Note_qualite), avg(Note_justesse), avg(Note_respect)
FROM Avis, Recette
WHERE Avis.Id_recette = Recette.Id_recette
group by Nom_recette;

-- calcul note globale recette
SELECT Nom_recette, (avg( Note_qualite ) + avg( Note_justesse ) + avg( Note_respect )) /3 AS Note
FROM Avis, Recette
WHERE Avis.Id_recette = Recette.Id_recette
GROUP BY Nom_recette


select Eleve.Id_eleve,Nom_eleve,Note_qualite,Note_justesse,Note_respect
from Eleve,Avis,Recette
where Eleve.Id_eleve = Avis.Id_eleve and Avis.Id_recette = Recette.Id_recette
group by Eleve.Id_eleve,Nom_eleve;

SELECT Eleve.Id_eleve, Nom_eleve, avg( Note_qualite ) , avg( Note_justesse ) , avg( Note_respect )
FROM Eleve, Avis, Recette
WHERE Eleve.Id_eleve = Avis.Id_eleve
AND Avis.Id_recette = Recette.Id_recette
GROUP BY Eleve.Id_eleve, Nom_eleve



-- afficher par eleve tous ses avis et la moyenne globale des recettes
select Eleve.Id_eleve,Nom_eleve,(Note_qualite+Note_justesse+Note_respect) / 3 as NoteEleve
from Eleve,Avis,Recette
where Eleve.Id_eleve = Avis.Id_eleve and Avis.Id_recette = Recette.Id_recette

