CREATE TABLE users (
	id integer PRIMARY KEY AUTOINCREMENT,
	ip varchar
);

CREATE TABLE apps (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar
);

CREATE TABLE block (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id integer,
	domain varchar,
	app_id integer
);

CREATE TABLE apps_urls (
	id integer PRIMARY KEY AUTOINCREMENT,
	app_id integer,
	domain varchar
);
