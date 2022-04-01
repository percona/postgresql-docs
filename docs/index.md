# Percona Distribution for PostgreSQL 12 Documentation

Percona Distribution for PostgreSQL is a collection of tools to assist you in managing your PostgreSQL
database system: it installs PostgreSQL and complements it by a selection of
extensions that enable solving essential practical tasks efficiently:


* [pg_repack](https://github.com/reorg/pg_repack) rebuilds
PostgreSQL database objects


* [pgAudit](https://www.pgaudit.org/) provides detailed session or object
audit logging via the standard PostgreSQL logging facility


* [pgAudit set_user](https://github.com/pgaudit/set_user) - The `set_user` part of `pgAudit` extension provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.


* [pgBackRest](https://pgbackrest.org/) is a backup and restore solution for
PostgreSQL


* [Patroni](https://patroni.readthedocs.io/en/latest/) is an HA (High Availability) solution for PostgreSQL.


* [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) collects and aggregates statistics for PostgreSQL and provides histogram information.


* [PgBouncer](https://www.pgbouncer.org/) - a lightweight connection pooler for PostgreSQL


* [pgBadger](https://github.com/darold/pgbadger) - a fast PostgreSQL Log Analyzer.


* [wal2json](https://github.com/eulerto/wal2json) - a PostgreSQL logical decoding JSON output plugin.


* A collection of [additional PostgreSQL contrib extensions](https://www.postgresql.org/docs/12/contrib.html)

!!! seealso

    Blog Posts

    - [pgBackRest - A Great Backup Solution and a Wonderful Year of
      Growth](https://www.percona.com/blog/2019/05/10/pgbackrest-a-great-backup-solution-and-a-wonderful-year-of-growth/)
    - [Securing PostgreSQL as an Enterprise-Grade
      Environment](https://www.percona.com/blog/2018/09/21/securing-postgresql-as-an-enterprise-grade-environment/)

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/12/libpq.html) library. It contains “a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.” [^1]


## Installation and Upgrade


- [Installing Percona Distribution for PostgreSQL](installing.md)
- [Upgrading Percona Distribution for PostgreSQL from 11 to 12](major-upgrade.md)
- [Minor Upgrade of Percona Distribution for PostgreSQL](minor-upgrade.md)
 
## Extensions


[pg_stat_monitor](pg-stat-monitor.md)

## Solutions

* [High Availability in PostgreSQL with Patroni](solutions/high-availability.md)

    * [Deploying high-availability on Debian and Ubuntu](solutions/ha-setup-apt.md)
    * [Deploying high-availability on RHEL and CentOS](solutions/ha-setup-yum.md)
    * [Testing the Patroni PostgreSQL Cluster](solutions/ha-test.md)

* [Backup and disaster recovery with pgBackRest](solutions/backup-recovery.md)

    * [Deploying backup and disaster recovery solution in Percona Distribution for PostgreSQL](solutions/dr-pgbackrest-setup.md)

## Uninstall Percona Distribution for PostgreSQL


[Uninstalling Percona Distribution for PostgreSQL](uninstalling.md)

## Release notes 

[Release notes](release-notes.md)


## Reference

[Licensing](licensing.md)


[^1]: https://www.postgresql.org/docs/12/libpq.html

