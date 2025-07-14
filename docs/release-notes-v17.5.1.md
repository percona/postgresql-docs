# Percona Distribution for PostgreSQL 17.5.1 ({{date.17_5_1}})

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 17.5.1 - a binary compatible, open source drop in replacement of [PostgreSQL Community 17.5](https://www.postgresql.org/docs/17/release-17-5.html).

## Release Highlights

### A new version of `pg_tde`

Percona Distribution for PostgreSQL includes the Release Candidate 2 (RC2) of `pg_tde` extension that brings in Transparent Data Encryption. This version of `pg_tde` provides a bunch of improvements, among which is WAL encryption now supporting Vault, automatic WAL internal key generation at server startup, new visibility and verification functions for default principal keys, and more. Learn about these features in the [`pg_tde` release notes :octicons-link-external-16:](https://docs.percona.com/pg-tde/release-notes/rc2.html).  

### Updated Major upgrade topic in documentation

The [Upgrading Percona Distribution for PostgreSQL from 16 to 17](major-upgrade.md) guide has been updated with revised steps for the [On Debian and Ubuntu using `apt`](major-upgrade.md/#on-debian-and-ubuntu-using-apt) section, improving clarity and reliability of the upgrade process.

| Extension                                                                            | Version   | Description                                                                                                          |
|--------------------------------------------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------|
| [etcd :octicons-link-external-16:](https://etcd.io/)                                                             | 3.5.21    | A distributed, reliable key-value store for setting up high available Patroni clusters                              |
| [HAProxy :octicons-link-external-16:](http://www.haproxy.org/)                       | 2.8.15    | A high-availability and load-balancing solution                                                                     |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/)     | 4.0.5     | A HA (High Availability) solution for PostgreSQL                                                                    |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/)                      | 17.1      | Provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL          |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user)  | 4.1.0     | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance.     |
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/)                    | 2.55.0    | A backup and restore solution for PostgreSQL                                                                        |
| [pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger)           | 13.1      | A fast PostgreSQL Log Analyzer                                                                                      |
| [PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/)                  | 1.24.1    | A lightweight connection pooler for PostgreSQL                                                                      |
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather)        | v30       | An SQL script for running the diagnostics of the health of a PostgreSQL cluster                                     |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.6.0 | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing      |
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack)          | 1.5.2     | Rebuilds PostgreSQL database objects                                                                                |
| [pgvector :octicons-link-external-16:](https://github.com/pgvector/pgvector)         | v0.8.0    | A vector similarity search for PostgreSQL                                                                           |
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis)            | 3.3.8     | A spatial extension for PostgreSQL                                                                                  |
| [PostgreSQL Common :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common) | 277 | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously              |
| [wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json)          | 2.6       | A PostgreSQL logical decoding JSON output plugin                                                                    |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries."
