CREATE TABLE users (
	id integer PRIMARY KEY AUTOINCREMENT,
	ip varchar
);

CREATE TABLE urls (
	id integer PRIMARY KEY AUTOINCREMENT,
	domain varchar
);

CREATE TABLE block (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id integer,
	url_id integer
);

CREATE TABLE urls_child (
	id integer PRIMARY KEY AUTOINCREMENT,
	url_id integer,
	domain varchar
);
