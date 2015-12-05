-- ============================================================
--   Nom de la base   :  RECETTE                                
--   Date de creation :  12/11/2015          
-- ============================================================

-- ============================================================
--   Table : ELEVE                                            
-- ============================================================
CREATE TABLE IF NOT EXISTS Eleve
(
    Id_eleve			int				not null AUTO_INCREMENT,
    Nom_eleve			varchar(20)		not null,
    Prenom_eleve		varchar(20)		not null,
    Date_inscription	TIMESTAMP		not null default CURRENT_TIMESTAMP,
    PRIMARY KEY (Id_eleve)
);

-- ============================================================
--   Table : RECETTE                                            
-- ============================================================
CREATE TABLE IF NOT EXISTS Recette
(
    Id_recette			int				not null AUTO_INCREMENT,
    Nom_recette			varchar(100)	not null,
    Budget				float			not null,
    Difficulte			int				not null,
    Temps_preparation	int				not null,
    Temps_cuisson		int				not null,
    Nb_personnes		int				not null,
    Etapes				varchar(5000)	not null,
    Categorie_recette	varchar(30)		not null,
    Id_eleve			int,
    Date_recette		TIMESTAMP		not null default CURRENT_TIMESTAMP,
    Derniere_consult	TIMESTAMP		default 0,
 	Url_image			varchar(200)	default null,
	Alt_image			varchar(200)	,
	PRIMARY KEY (Id_recette),
    FOREIGN KEY (Id_eleve) REFERENCES Eleve(Id_eleve)
		ON DELETE SET NULL
		ON UPDATE CASCADE
);

-- ============================================================
--   Table : INGREDIENT                                            
-- ============================================================
CREATE TABLE IF NOT EXISTS Ingredient
(
    Id_ingredient 		int				not null AUTO_INCREMENT,
    Nom_ingredient		varchar(30)		not null,
    Unite_mesure		varchar(20)		not null,
    PRIMARY KEY (Id_ingredient)
);

-- ============================================================
--   Table : COMPOSER                                            
-- ============================================================
CREATE TABLE IF NOT EXISTS Composer
(
    Id_recette			int				not null,
    Id_ingredient		int				not null,
    Quantite			float			not null,
    Categorie_recette	varchar(30)		not null,
    PRIMARY KEY (Id_recette, Id_ingredient),
    FOREIGN KEY (Id_recette) REFERENCES Recette(Id_recette)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
    FOREIGN KEY (Id_ingredient) REFERENCES Ingredient(Id_ingredient)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

-- ============================================================
--   Table : COMMENTER                                            
-- ============================================================
CREATE TABLE IF NOT EXISTS Commenter
(
    Id_eleve			int				not null,
    Id_recette			int				not null,
    Commentaire			varchar(1000)   not null,
    Date_commentaire	TIMESTAMP		not null default CURRENT_TIMESTAMP,
    PRIMARY KEY (Id_eleve, Id_recette, Date_commentaire),
    FOREIGN KEY (Id_eleve) REFERENCES Eleve(Id_eleve)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
    FOREIGN KEY (Id_recette) REFERENCES Recette(Id_recette)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

-- ============================================================
--   Table : AVIS                                            
-- ============================================================
CREATE TABLE IF NOT EXISTS Avis
(
    Id_eleve			int				not null,
    Id_recette			int				not null,
	Note_qualite		TINYINT			not null,
	Note_justesse		TINYINT			not null,
	Note_respect		TINYINT			not null,
	Date_avis			TIMESTAMP		not null default CURRENT_TIMESTAMP,
	Avis_recette		varchar(1000)	not null,
    PRIMARY KEY (Id_eleve, Id_recette),
    FOREIGN KEY (Id_eleve) REFERENCES Eleve(Id_eleve)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
    FOREIGN KEY (Id_recette) REFERENCES Recette(Id_recette)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);
