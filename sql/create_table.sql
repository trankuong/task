CREATE TABLE User (

	username VARCHAR(20) NOT NULL, 
	firstname VARCHAR(20), 
	lastname VARCHAR(20), 
	password VARCHAR(256), 
	email VARCHAR(40), 
	PRIMARY KEY(username));

CREATE TABLE Activities (
	activityid INT NOT NULL AUTO_INCREMENT, 
	username VARCHAR(20) NOT NULL, 
	activity_time DATETIME, 
	activity VARCHAR(20) NOT NULL,
	details VARCHAR(256), 
	PRIMARY KEY (activityid));