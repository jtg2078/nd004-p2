-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- reset everything
drop table IF EXISTS matches CASCADE;
drop table IF EXISTS tournament_players CASCADE;
drop table IF EXISTS tournaments CASCADE;
drop table IF EXISTS players CASCADE;
drop function IF EXISTS opponent_match_wins(winner_id text);

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
  wins integer DEFAULT 0,
  matches integer DEFAULT 0,
  had_bye boolean default false,
  player integer references players(id) ON DELETE CASCADE,
  tournament integer references tournaments(id) ON DELETE CASCADE
);

-- matches
create table matches(
  id serial primary key,
  tournament integer references tournaments(id) ON DELETE CASCADE,
  winner text references tournament_players(id) ON DELETE CASCADE,
  p1 text references tournament_players(id) ON DELETE CASCADE,
  p2 text references tournament_players(id) ON DELETE CASCADE,
  loser text references tournament_players(id) ON DELETE CASCADE
);


-- functions
CREATE OR REPLACE FUNCTION opponent_match_wins(winner_id TEXT) RETURNS BIGINT AS $$
  SELECT
    COALESCE(sum(wins), 0)
  FROM
    tournament_players
    JOIN
    (
      SELECT
        loser
      FROM
        matches
      WHERE
        winner = winner_id
    ) AS opponents
    ON
      tournament_players.id = opponents.loser
$$ LANGUAGE SQL;


