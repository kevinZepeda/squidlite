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
