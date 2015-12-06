# SGBD
Install mysql :
===============

sudo apt-get install mysql-server



Install python :
=================

sudo apt-get install python-dev


Setup Flask and mysql-python
============================

sudo apt-get install python-pip
sudo apt-get install libmysqlclient-dev
pip install mysql-python
pip install Flask
python ez_setup.py (optionnel, si la suite ne marche pas)
pip install flask-mysql
pip install flask-login
chmod 700 run.py

Setup mysql
===========
mysql -u root -p
CREATE DATABASE ProjetSGBD;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';
FLUSH PRIVILEGES;
exit;
mysql -u admin -p ProjetSGBD
\. creation_base.sql
\. donnees_etendues.sql
