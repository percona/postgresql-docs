# Percona Distribution for PostgreSQL 11 Documentation

Percona Distribution for PostgreSQL is a collection of tools to assist you in managing your PostgreSQL
database system: it installs PostgreSQL and complements it by a selection of
extensions that enable solving essential practical tasks efficiently:


* [HAProxy](http://www.haproxy.org/) - a high-availability and load-balancing solution 

* [Patroni](https://patroni.readthedocs.io/en/latest/) is an HA (High Availability) solution for PostgreSQL.

* [pgAudit](https://www.pgaudit.org/) provides detailed session or object
audit logging via the standard PostgreSQL logging facility

* [pgAudit set_user](https://github.com/pgaudit/set_user) - The `set_user` part of `pgAudit` extension provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.

* [pgBackRest](https://pgbackrest.org/) is a backup and restore solution for
PostgreSQL

* [pgBadger](https://github.com/darold/pgbadger) - a fast PostgreSQL Log Analyzer.

* [PgBouncer](https://www.pgbouncer.org/) - a lightweight connection pooler for PostgreSQL

* [pgpool2](https://www.pgpool.net/mediawiki/index.php/Main_Page) - a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.

* [pg_repack](https://github.com/reorg/pg_repack) rebuilds
PostgreSQL database objects

* [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) collects and aggregates statistics for PostgreSQL and provides histogram information.

* [PostGIS](http://postgis.net/) allows storing and manipulating spacial data in PostgreSQL.

* [wal2json](https://github.com/eulerto/wal2json) - a PostgreSQL logical decoding JSON output plugin.

* A collection of [additional PostgreSQL contrib extensions](https://www.postgresql.org/docs/12/contrib.html)


[Get started](installing.md){ .md-button }
[What's new]({{release}}.md){ .md-button }


!!! admonition "See also"

    Blog Posts

    - [pgBackRest - A Great Backup Solution and a Wonderful Year of
      Growth](https://www.percona.com/blog/2019/05/10/pgbackrest-a-great-backup-solution-and-a-wonderful-year-of-growth/)
    - [Securing PostgreSQL as an Enterprise-Grade
      Environment](https://www.percona.com/blog/2018/09/21/securing-postgresql-as-an-enterprise-grade-environment/)

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/11/libpq.html) library. It contains “a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.” 

