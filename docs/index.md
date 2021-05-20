# Percona Distribution for PostgreSQL 11 Documentation

Percona Distribution for PostgreSQL is a collection of tools to assist you in managing your PostgreSQL
database system: it installs PostgreSQL and complements it by a selection of
extensions that enable solving essential practical tasks efficiently:


* [pg_repack](https://github.com/reorg/pg_repack) rebuilds
PostgreSQL database objects


* [pgAudit](https://www.pgaudit.org/) provides detailed session or object
audit logging via the standard PostgreSQL logging facility


* [pgBackRest](https://pgbackrest.org/) is a backup and restore solution for
PostgreSQL


* [Patroni](https://patroni.readthedocs.io/en/latest/) is a HA (High Availability)  solution for PostgreSQL.


* [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) (Tech Preview Feature [^1]) collects and aggregates statistics for PostgreSQL and provides histogram information.


* A collection of [additional PostgreSQL contrib extensions](https://www.postgresql.org/docs/11/contrib.html)

!!! see "See also"

    Blog Posts

    - [pgBackRest - A Great Backup Solution and a Wonderful Year of
      Growth](https://www.percona.com/blog/2019/05/10/pgbackrest-a-great-backup-solution-and-a-wonderful-year-of-growth/)
    - [Securing PostgreSQL as an Enterprise-Grade
      Environment](https://www.percona.com/blog/2018/09/21/securing-postgresql-as-an-enterprise-grade-environment/)

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/11/libpq.html) library. It contains “a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.” [^2] 

## Installation and Upgrade


* [Installing Percona Distribution for PostgreSQL](installing.md)
* [Minor Upgrade of Percona Distribution for PostgreSQL](minor-upgrade.md)


## Extensions


* [pg_stat_monitor](pg-stat-monitor.md)


## Uninstall Percona Distribution for PostgreSQL


* [Uninstalling Percona Distribution for PostgreSQL](uninstalling.md)


## Release Notes


* [Release Notes](release-notes.md)


## Reference


* [Licensing](licensing.md)


[^1]: Tech Preview Features are not yet ready for enterprise use and are not included in support via . They are included in this release so that users can provide feedback prior to the full release of the feature in a future release (or removal of the feature if it is deemed not useful). This functionality can change (APIs, CLIs, etc.) from tech preview to GA.
[^2]: https://www.postgresql.org/docs/11/libpq.html

