-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c postgres

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE tournament (
	t_id serial PRIMARY KEY,
	title varchar(250),
	ts timestamp default CURRENT_TIMESTAMP
);

CREATE TABLE player (
	p_id serial PRIMARY KEY,
	t_id integer REFERENCES tournament ON DELETE CASCADE,
	name varchar(250),
	ts timestamp default CURRENT_TIMESTAMP
);

CREATE TABLE match (
	m_id serial PRIMARY KEY,
	t_id integer REFERENCES tournament ON DELETE CASCADE,
	winner integer REFERENCES player ON DELETE CASCADE,
	ts timestamp default CURRENT_TIMESTAMP
);

CREATE TABLE match_player (
	m_id integer REFERENCES match ON DELETE CASCADE,
	p_id integer REFERENCES player ON DELETE CASCADE,
	win smallint,
	ts timestamp default CURRENT_TIMESTAMP
);


CREATE VIEW standings AS SELECT
    P.p_id AS id,
    P.name,
    COUNT(W.win) AS wins,
    COUNT(M.m_id) AS matches,
    P.t_id AS t_id

FROM
    player AS P

LEFT JOIN
    match AS X ON(
	X.t_id = P.t_id
    )

LEFT JOIN
    match_player AS M ON(
	M.p_id = P.p_id AND
	M.m_id = X.m_id
    )

LEFT JOIN
    match_player AS W ON(
	W.m_id = X.m_id AND
	W.p_id = P.p_id AND
	W.win = 1
    )

GROUP BY
    P.p_id

ORDER BY
    wins DESC;
    