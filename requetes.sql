-- OK suppression Eleve -> recette associée id_eleve = null 
--
--
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



ALTER TABLE Recette DROP FOREIGN KEY fk_parent;
ALTER TABLE Recette ADD CONSTRAINT fk_parent
	FOREIGN KEY (id_parent)
	REFERENCES parent(id)
	ON DELETE SET NULL
	ON UPDATE SET NULL;


insert into Commenter (Id_eleve,Id_recette, Commentaire, Date_commentaire) values (1,1,"C'est de la balle !","2014-01-01");

insert into Commenter (Id_eleve,Id_recette, COmmentaire, Date_commentaire) values (1,1,"et puis c'est bon !","2014-02-02");

select Eleve.Nom_eleve
from Eleve
natural join Commenter,
natural join Recette
group by Eleve.Nom_eleve;


SET FOREIGN_KEY_CHECKS=0;
delete from Eleve;
SET FOREIGN_KEY_CHECKS=1;

-- moyenne des prix des recettes proposées par un élève donné



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
