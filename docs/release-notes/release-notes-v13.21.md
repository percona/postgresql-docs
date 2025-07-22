# Percona Distribution for PostgreSQL 13.21 ({{date.13_21}})

[Installation](../installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 13.21](https://www.postgresql.org/docs/13/release-13-21.html).

## Release Highlights

### Updated Major upgrade topic in documentation

The [Upgrading Percona Distribution for PostgreSQL from 12 to 13](../major-upgrade.md) guide has been updated with revised steps for the [On Debian and Ubuntu using `apt`](../major-upgrade.md/#on-debian-and-ubuntu-using-apt) section, improving clarity and reliability of the upgrade process.

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension                                                                              | Version   | Description                                                                                                          |
|----------------------------------------------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------|
| [etcd](https://etcd.io/)                                                               | 3.5.21    | A distributed, reliable key-value store for setting up high available Patroni clusters                              |
| [HAProxy](http://www.haproxy.org/)                                                     | 2.8.15    | A high-availability and load-balancing solution                                                                     |
| [Patroni](https://patroni.readthedocs.io/en/latest/)                                   | 4.0.5     | A HA (High Availability) solution for PostgreSQL                                                                    |
| [PgAudit](https://www.pgaudit.org/)                                                    | 1.5.3     | Provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL          |
| [pgAudit set_user](https://github.com/pgaudit/set_user)                                | 4.1.0     | Provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles to perform needed maintenance tasks. |
| [pgBackRest](https://pgbackrest.org/)                                                  | 2.55.0    | A backup and restore solution for PostgreSQL                                                                        |
| [pgBadger](https://github.com/darold/pgbadger)                                         | 13.1      | A fast PostgreSQL Log Analyzer.                                                                                      |
| [PgBouncer](https://www.pgbouncer.org/)                                                | 1.24.1    | A lightweight connection pooler for PostgreSQL                                                                      |
| [pg_gather](https://github.com/jobinau/pg_gather)                                      | v30       | An SQL script for running the diagnostics of the health of PostgreSQL cluster                                       |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary)                  | 4.6.0     | A middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.      |
| [pg_repack](https://github.com/reorg/pg_repack)                                        | 1.5.2     | Rebuilds PostgreSQL database objects                                                                                |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)                          | 2.2.0     | Collects and aggregates statistics for PostgreSQL and provides histogram information.                                |
| [pgvector](https://github.com/pgvector/pgvector)                                       | v0.8.0    | A vector similarity search for PostgreSQL                                                                           |
| [PostGIS](https://github.com/postgis/postgis)                                          | 3.3.8     | A spatial extension for PostgreSQL.                                                                                  |
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common)             | 277       | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time. |
| [wal2json](https://github.com/eulerto/wal2json)                                        | 2.6       | A PostgreSQL logical decoding JSON output plugin                                                                    |

For Red Hat Enterprise Linux 8 and 9 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/13/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries."
