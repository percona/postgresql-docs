# Percona Distribution for PostgreSQL 16.10 ({{date.16_10}})

[Installation](../installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 16.10](https://www.postgresql.org/docs/16/release-16-10.html).

## Release Highlights

### Major documentation updates

* Expanded and improved the [High Availability](../solutions/high-availability.md) topic with more information and example deployments.
* Updated the [PostGIS installation commands via yum](../yum.md#for-postgis) topic.

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [etcd](https://etcd.io/)| 3.5.21 | A distributed, reliable key-value store for setting up high available Patroni clusters |
| [HAProxy](http://www.haproxy.org/) | 2.8.15 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 4.0.5 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/) | 16.0 | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 4.1.0 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/) | 2.55.0 | a backup and restore solution for PostgreSQL |
| [pgBadger](https://github.com/darold/pgbadger) | 13.1 | a fast PostgreSQL Log Analyzer. |
| [PgBouncer](https://www.pgbouncer.org/) | 1.24.1 | a lightweight connection pooler for PostgreSQL |
| [pg_gather](https://github.com/jobinau/pg_gather) | v30 | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.6.0 | a middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing. |
| [pg_repack](https://github.com/reorg/pg_repack) | 1.5.2 | rebuilds PostgreSQL database objects |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | 2.1.1 | collects and aggregates statistics for PostgreSQL and provides histogram information. |
| [pgvector](https://github.com/pgvector/pgvector) | v0.8.0 | A vector similarity search for PostgreSQL |
| [PostGIS](https://github.com/postgis/postgis) | 3.3.8 | a spatial extension for PostgreSQL. |
| [PostgreSQL Commons](https://salsa.debian.org/postgresql/postgresql-common) | 277 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time. |
| [wal2json](https://github.com/eulerto/wal2json) | 2.6 | a PostgreSQL logical decoding JSON output plugin |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/16/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries."
