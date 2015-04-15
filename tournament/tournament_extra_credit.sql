-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- player table
create table players(
  id serial primary key,
  name varchar (50)
);

-- tournament table
create table tournaments(
  id serial primary key
);

-- tournament players
create table tournament_players(
  id serial primary key,
  player_id integer references players(id),
  tournament_id integer references tournaments(id)
);

-- matches
create table matches(
  id serial primary key,
  tournament_id integer references tournaments(id),
  winner_id integer references tournament_players(id),
  loser_id integer references tournament_players(id)
);


