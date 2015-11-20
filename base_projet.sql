-- ============================================================
--   Nom de la base   :  RECETTE                                
--   Date de creation :  12/11/2015          
-- ============================================================

--drop index ELEVE_PK;
--drop table ELEVE cascade constraints;

--drop index RECETTE_PK;
--drop table RECETTE cascade constraints;

--drop index INGREDIENT_PK;
--drop table INGREDIENT cascade constraints;

--drop index COMPOSER_PK;
--drop table COMPOSER cascade constraints;

--drop index COMMENTER_PK;
--drop table COMMENTER cascade constraints;

--drop index AVIS_PK;
--drop table AVIS cascade constraints;

-- ============================================================
--   Table : ELEVE                                            
-- ============================================================
create table ELEVE
(
    ID_ELEVE	                   INT		              not null,
    NOM_ELEVE                      CHAR(20)               not null,
    PRENOM_ELEVE                   CHAR(20)               not null,
    DATE_INSCRIPTION               DATE                           ,
    constraint pk_eleve primary key (ID_ELEVE)
);

-- ============================================================
--   Table : RECETTE                                            
-- ============================================================
create table RECETTE
(
    ID_RECETTE		               INT		              not null,
    NOM_RECETTE                    CHAR(20)               not null,
    BUDGET		                   NUMBER(3)              not null,
    DIFFICULTE				       INT					  not null,
    TEMPS_PREPARATION		       INT					  not null,
    TEMPS_CUISSON			       INT					  not null,
    ETAPES						   CHAR(1000)			  not null,
    CATEGORIE_RECETTE			   CHAR(20)  			  not null,
    ID_ELEVE					   INT					  not null,
    constraint pk_recette primary key (ID_RECETTE)
);

-- ============================================================
--   Table : INGREDIENT                                            
-- ============================================================
create table INGREDIENT
(
    ID_INGREDIENT                  INT		              not null,
    NOM_INGREDIENT                 CHAR(20)               not null,
    UNITE_MESURE                   CHAR(20)               not null,
    CATEGORIE_INGREDIENT	       CHAR(20)  			  not null,
    constraint pk_ingredient primary key (ID_INGREDIENT)
);

-- ============================================================
--   Table : COMPOSER                                            
-- ============================================================
create table COMPOSER
(
    ID_RECETTE	               	   INT             		  not null,
    ID_INGREDIENT	               INT		              not null,
    QUANTITE	                   NUMBER(3)   	          not null,
    constraint pk_composer primary key (ID_RECETTE, ID_INGREDIENT)
);

-- ============================================================
--   Table : COMMENTER                                            
-- ============================================================
create table COMMENTER
(
    ID_ELEVE	                   INT             		  not null,
    ID_RECETTE	                   INT		              not null,
    COMMENTAIRE	                   CHAR(1000)             not null,
    constraint pk_commenter primary key (ID_ELEVE, ID_RECETTE)
);

-- ============================================================
--   Table : AVIS                                            
-- ============================================================
create table AVIS
(
    ID_ELEVE	                   INT             		  not null,
    ID_RECETTE	                   INT		              not null,
	NOTE_QUALITE				   NUMBER(1)			  not null,
	NOTE_JUSTESSE				   NUMBER(1)			  not null,
	NOTE_RESPECT				   NUMBER(1)			  not null,
    constraint pk_avis primary key (ID_ELEVE, ID_RECETTE)
);


alter table RECETTE
    add constraint fk1_recette foreign key (ID_ELEVE)
       references ELEVE (ID_ELEVE);

alter table COMPOSER
    add constraint fk1_composer foreign key (ID_RECETTE)
       references RECETTE (ID_RECETTE);

alter table COMPOSER
    add constraint fk2_composer foreign key (ID_INGREDIENT)
       references INGREDIENT (ID_INGREDIENT);

alter table COMMENTER
    add constraint fk1_commenter foreign key (ID_ELEVE)
       references ELEVE (ID_ELEVE);

alter table COMMENTER
    add constraint fk2_commenter foreign key (ID_RECETTE)
       references RECETTE (ID_RECETTE);

alter table AVIS
    add constraint fk1_avis foreign key (ID_ELEVE)
       references ELEVE (ID_ELEVE);

alter table AVIS
    add constraint fk2_avis foreign key (ID_RECETTE)
       references RECETTE (ID_RECETTE);





