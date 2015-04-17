#Full Stack Web Developer Nanodegree project 2


## How to run

setup vagrant

```
https://docs.google.com/document/u/0/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true
```

getting source code

```
git clone git@github.com:jtg2078/nd004-p2.git

```

run

```
(copy contents of git cloned tournament folder into vagrant's tournament folder)

cd fullstack/vagrant
vagrant up
vagrant ssh
cd /vagrant/tournament
psql
create database tournament;
\c tournament
\i tournament.sql
\q
python tournament_test.py 
```

run extra credit

```
(copy tournament_extra folder into fullstack/vagrant directory)

cd fullstack/vagrant
vagrant up
vagrant ssh
cd /vagrant/tournament_extra
psql
create database tournament_extra;
\c tournament_extra
\i tournament.sql
\q
python tournament_test.py
```

## References / Notes / Credits

* [selkhateeb/hardlink](https://github.com/selkhateeb/hardlink)  
    for getting hard link to work
* [Postgres.app](http://postgresapp.com/)
* [What is the PostgreSQL equivalent for ISNULL()](http://stackoverflow.com/questions/2214525/what-is-the-postgresql-equivalent-for-isnull)
* [MySQL Multiple Left Joins](http://stackoverflow.com/questions/1990352/mysql-multiple-left-joins)
* [SQL Left Join Subquery Alias](http://stackoverflow.com/questions/16776176/sql-left-join-subquery-alias)
* [Postgresql function for last inserted id](http://stackoverflow.com/questions/2944297/postgresql-function-for-last-inserted-id)
* [5.3. Constraints](http://www.postgresql.org/docs/current/interactive/ddl-constraints.html)
* [What is causing ERROR: there is no unique constraint matching given keys for referenced table?](http://stackoverflow.com/questions/11966420/what-is-causing-error-there-is-no-unique-constraint-matching-given-keys-for-ref)
* [Postico app](https://eggerapps.at/postico/)
* [Postgresql function for last inserted id](http://stackoverflow.com/questions/2944297/postgresql-function-for-last-inserted-id)
* [Is SQL or even TSQL Turing Complete?](http://stackoverflow.com/questions/900055/is-sql-or-even-tsql-turing-complete)
* [Swiss-system tournament](http://en.wikipedia.org/wiki/Swiss-system_tournament)
* notes
    * [Intro To Relational Databases](http://jtg2078.github.io/relational-db/elements-of-sql.html)
    * [Python DB-API Quick Reference](http://jtg2078.github.io/relational-db/python-db-api.html)
    * [Normalized Design](http://jtg2078.github.io/relational-db/deeper-into-sql.html)

