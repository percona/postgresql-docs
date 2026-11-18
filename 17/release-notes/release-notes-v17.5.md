> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/17/llms.txt).

# Percona Distribution for PostgreSQL 17.5.2 (2025-06-30)

Percona Distribution for PostgreSQL is a solution that includes PostgreSQL server and the collection of tools from PostgreSQL community. These tools are tested to work together and serve to assist you in deploying and managing PostgreSQL.

The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability, and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 17.5.2 - a binary compatible, open source drop in replacement of [PostgreSQL Community 17.5](https://www.postgresql.org/docs/17/release-17-5.html).

## Release Highlights

### General Availability (GA) of pg_tde

Percona Distribution for PostgreSQL now includes the 1.0 GA release of Percona’s Transparent Data Encryption for PostgreSQL.

Learn more in the [`pg_tde` 1.0 release notes](https://docs.percona.com/pg-tde/release-notes/release-notes-v1.0.html) .

### Major documentation update

The `pg_tde` documentation has received significant updates, which include:

- New KMS configuration guides for Fortanix, Vault, KMIP and OpenBAO
- Reorganized and expanded topics for Architecture, GUC, Functions, TDE Operations and FAQ
- Extensive and numerous refinements and clarifications across the entire site

Explore the full documentation [in the official `pg_tde` documentations](https://docs.percona.com/pg-tde/index.html).

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension                                                                  | Version | Description                                                                                                      |
| -------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------- |
| [etcd](https://etcd.io/)                                                   | 3.5.21  | A distributed, reliable key-value store for setting up high available Patroni clusters                           |
| [HAProxy](http://www.haproxy.org/)                                         | 2.8.15  | A high-availability and load-balancing solution                                                                  |
| [Patroni](https://patroni.readthedocs.io/en/latest/)                       | 4.0.5   | A HA (High Availability) solution for PostgreSQL                                                                 |
| [PgAudit](https://www.pgaudit.org/)                                        | 17.1    | Provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL       |
| [pgAudit set_user](https://github.com/pgaudit/set_user)                    | 4.1.0   | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance. |
| [pgBackRest](https://pgbackrest.org/)                                      | 2.55.0  | A backup and restore solution for PostgreSQL                                                                     |
| [pgBadger](https://github.com/darold/pgbadger)                             | 13.1    | A fast PostgreSQL Log Analyzer                                                                                   |
| [PgBouncer](https://www.pgbouncer.org/)                                    | 1.24.1  | A lightweight connection pooler for PostgreSQL                                                                   |
| [pg_gather](https://github.com/jobinau/pg_gather)                          | v30     | An SQL script for running the diagnostics of the health of a PostgreSQL cluster                                  |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary)      | 4.6.0   | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing  |
| [pg_repack](https://github.com/reorg/pg_repack)                            | 1.5.2   | Rebuilds PostgreSQL database objects                                                                             |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)              | 2.2.0   | collects and aggregates statistics for PostgreSQL and provides histogram information.                            |
| [pgvector](https://github.com/pgvector/pgvector)                           | v0.8.0  | A vector similarity search for PostgreSQL                                                                        |
| [PostGIS](https://github.com/postgis/postgis)                              | 3.3.8   | A spatial extension for PostgreSQL                                                                               |
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common) | 277     | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously           |
| [wal2json](https://github.com/eulerto/wal2json)                            | 2.6     | A PostgreSQL logical decoding JSON output plugin                                                                 |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains “a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.”
