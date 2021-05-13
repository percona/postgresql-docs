# Percona Distribution for PostgreSQL 11.6

Percona is happy to announce the release of Percona Distribution for PostgreSQL 11.6 on January 23, 2020.
Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL
installs PostgreSQL and complements it by a selection of extensions that
enable solving essential practical tasks efficiently:


* [Pg_repack](https://github.com/reorg/pg_repack) rebuilds PostgreSQL
database objects.


* [Pgaudit](https://www.pgaudit.org/) provides detailed session or object
audit logging via the standard logging facility provided by PostgreSQL


* [pgBackRest](https://pgbackrest.org/) - a backup and restore solution for
PostgreSQL


* [Patroni](https://patroni.readthedocs.io/en/latest/) - an HA (High Availability) solution for
PostgreSQL


* A collection of [additional PostgreSQL contrib extensions](https://www.postgresql.org/docs/11/contrib.html)

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/11/libpq.html) library. It contains “a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.” [^1]

This release of Percona Distribution for PostgreSQL is based on PostgreSQL 11.6.

> <b>Important</b>: 

> On Debian and other systems that use the `apt` package manager, such as Ubuntu, components of Percona Distribution for PostgreSQL 11 can only be installed together with the server shipped by Percona (`percona-postgresql-11`). If you wish to use Percona Distribution for PostgreSQL, uninstall the PostgreSQL package provided by your distribution (postgresql-11) and then install the chosen components from Percona Distribution for PostgreSQL.

## Bugs Fixed


* [DISTPG-34](https://jira.percona.com/browse/DISTPG-34): Components shipped with Percona Distribution for PostgreSQL could not be
installed alongside PostgreSQL.

[^1]: https://www.postgresql.org/docs/11/libpq.html