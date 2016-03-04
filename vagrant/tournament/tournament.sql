-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;


--1 Create Players table, where each player has the following information
    --Unique ID - serial
    --Name - string
    --Number of games played - integer
    --Running Score - integer

CREATE TABLE Players(
  P_ID serial PRIMARY KEY,
  Name text,
  Games_Played int,
  Score int
);



--2 Create Matches table, where each game has the following info:
  --Match Unique ID -serial
  --Round Number - integer
  --Player 1 - serial
  --Player 2 - serial
  --Winner - serial
  --Draw - Boolean

CREATE TABLE Matches(
  M_ID serial PRIMARY KEY,
  Round int,
  P1 serial,
  P2 serial,
  Winner serial
);

Create View Player_Match_Count as (select public.players.P_ID, count(public.matches.P1 + public.matches.P2) as Match_Count from public.matches right outer join public.players on (public.matches.P1 = public.players.P_ID or public.matches.P2 = public.players.P_ID) group by public.players.P_ID);

Create View Player_Win_Count as (select public.players.P_ID, count(public.matches.winner) as Win_Count from public.matches right outer join public.players on (public.matches.winner = public.players.P_ID) group by public.players.P_ID);

--3 Create Rounds table, showing all player matchings that take place in a round:
  --Round
  --Game
  --Winner


--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


