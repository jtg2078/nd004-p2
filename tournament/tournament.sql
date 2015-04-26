-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- switch to correct db (not sure if this syntax works)
\c tournament

-- reset everything
drop table IF EXISTS players CASCADE;
drop table IF EXISTS matches CASCADE;
drop view IF EXISTS winners;
drop view IF EXISTS losers;

-- player table
create table players(
  id serial primary key,
  name varchar (50)
);

-- matches
create table matches(
  id serial primary key,
  winner integer references players(id),
  loser integer references players(id)
);

-- views
CREATE VIEW winners AS
  select
    winner, count(winner) as wins
  from
    matches
  group by
    winner;

CREATE VIEW losers AS
  select
    loser, count(loser) as losses
  from
    matches
  group by
    loser;


