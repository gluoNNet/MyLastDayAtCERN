Import CSV to postgreSQL
==============================

CREATE TABLE events (
	id int PRIMARY KEY,
	room varchar(100),
	title varchar(100),
	startDate timestamp with time zone,
	endDate timestamp with time zone,
	chairs varchar(100)[],
	creator varchar(100),
	type varchar(100),
	categoryId int, --?
	description varchar(5000),
	url varchar(100)
);

CREATE TABLE people (
	emailHash varchar(100) PRIMARY KEY,
	fullName varchar(100),
	affiliation varchar(100)
);

CREATE TABLE venue (
	room varchar(100),
	location varchar(100)
);

CREATE TABLE categ (
	id int PRIMARY KEY,
	name varchar(100)
);

==============================

COPY events FROM '/Users/williamyam/PycharmProjects/CERNwebfest/data.csv' WITH (FORMAT csv);

SELECT * FROM events;