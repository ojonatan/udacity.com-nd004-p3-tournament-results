-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE tournament (
	t_id serial PRIMARY KEY,
	title varchar(250),
	ts timestamp
);

CREATE TABLE player (
	p_id serial PRIMARY KEY,
	t_id integer REFERENCES tournament ON DELETE CASCADE,
	name varchar(250),
	ts timestamp
);

CREATE TABLE match (
	m_id serial PRIMARY KEY,
	t_id integer REFERENCES tournament ON DELETE CASCADE,
	winner integer REFERENCES player ON DELETE CASCADE,
	ts timestamp
);

CREATE TABLE match_player (
	m_id integer REFERENCES match ON DELETE CASCADE,
	p_id integer REFERENCES player ON DELETE CASCADE,
	win smallint,
	ts timestamp
);
