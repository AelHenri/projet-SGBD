CREATE DATABASE EmpData;

CREATE TABLE User(
 userId INT NOT NULL AUTO_INCREMENT,
 userName VARCHAR(100) NOT NULL,
 password VARCHAR(40) NOT NULL,
 PRIMARY KEY(userId)
 );

 insert into User values('','Admin','admin');