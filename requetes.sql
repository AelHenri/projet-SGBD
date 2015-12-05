-- OK	suppression Eleve -> recette associée id_eleve = null 
-- OK	suppression Eleve -> suppression Commentaires et Avis associés
--		suppression Recette -> suppression Images associées
--
--
--
--
--
--


-- insertion
insert into Eleve (Nom_eleve,Prenom_eleve) values ("Gangloff", "Nolwenn");
insert into Eleve (Nom_eleve,Prenom_eleve,Date_inscription) values ("Gruchet", "Seb", "1994-03-13");


insert into Recette (Nom_recette,Budget,Difficulte,Temps_preparation,Temps_cuisson,Etapes,Categorie_recette,Id_eleve)
values ("Tiramisu", 30, 2,15,0,"battez les oeufs, mettez le mascarpone","Dessert",1);



insert into Recette (Nom_recette,Budget,Difficulte,Temps_preparation,Temps_cuisson,Etapes,Categorie_recette,Id_eleve)
values ("Tiramisu", 30, 2,15,0,"battez les oeufs, mettez le mascarpone","Dessert",3);


insert into Commenter (Id_eleve,Id_recette, Commentaire) values (1,1,"C'est de la balle !");
insert into Commenter (Id_eleve,Id_recette, Commentaire) values (1,1,"et puis c'est bon !");


select Eleve.Nom_eleve
from Eleve
natural join Commenter,
natural join Recette
group by Eleve.Nom_eleve;


select *
from Ingredient
natural join Composer
where Ingredient.Id_ingredient = 34;


-- liste des recettes utilisant du poivre
select Nom_recette
from Recette, Composer, Ingredient
where Recette.Id_recette = Composer.Id_recette and Composer.Id_ingredient = Ingredient.Id_ingredient and Nom_ingredient = "poivre";

-- moyenne des prix des recettes proposées par un élève donné
select avg(Budget)
from Recette
where Id_eleve = 1;

-- nombres recettes dispo pour chaque catégorie
select *
from Recette
where Categorie_recette = "Dessert";


-- classement des recettes selon le meilleur rapport qualité/prix
-- (on pourra supposer par exemple qu’une recette non commenté a une note par défaut de 2)



-- classement des desserts les plus rapides à réaliser
select *
from Recette
where Categorie_recette = "Dessert"
order by (Temps_preparation + Temps_cuisson) DESC;


-- classement des plats les plus commentés



-- on souhaite décerner le prix du critique gastronomique le plus fiable :
-- calculer l’élève dont l’écart type des notes à la moyenne de chacun des plats qu’il a commenté est le plus faible
