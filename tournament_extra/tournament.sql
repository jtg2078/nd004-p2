-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- reset everything
drop table matches CASCADE;
drop table tournament_players CASCADE;
drop table tournaments CASCADE;
drop table players CASCADE;

-- player table
create table players(
  id serial primary key,
  name text
);

-- tournament table
create table tournaments(
  id serial primary key,
  name text
);

-- tournament players
create table tournament_players(
  id text primary key,
  player integer references players(id) ON DELETE CASCADE,
  tournament integer references tournaments(id) ON DELETE CASCADE
);

-- matches
create table matches(
  id serial primary key,
  tournament integer references tournaments(id) ON DELETE CASCADE,
  winner text references tournament_players(id) ON DELETE CASCADE,
  loser text references tournament_players(id) ON DELETE CASCADE
);


