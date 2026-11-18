> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/17/llms.txt).

# Percona Distribution for PostgreSQL 17.4.1 (2025-03-27)

Percona Distribution for PostgreSQL is a solution that includes PostgreSQL server and the collection of tools from PostgreSQL community. These tools are tested to work together and serve to assist you in deploying and managing PostgreSQL.

The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability, and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 17.4.1 - a binary compatible, open source drop in replacement of [PostgreSQL Community 17.4](https://www.postgresql.org/docs/17/release-17-4.html).

## Release Highlights

This release fixes [CVE-2025-1094](https://www.postgresql.org/support/security/CVE-2025-1094/), which closed a vulnerability in the `libpq` PostgreSQL client library but introduced a regression related to string handling for non-null terminated strings. The error would be visible based on how a PostgreSQL client implemented this behavior. This regression affects versions 17.3, 16.7, 15.11, 14.16, and 13.19. For this reason, version 17.3 was skipped.

### A new version of `pg_tde`

Percona Distribution for PostgreSQL includes the Release Candidate of `pg_tde` extension that brings in Transparent Data Encryption. This version of `pg_tde` provides a bunch of improvements, among which is the redesigned WAL encryption, simplified configuration for single-tenant environments, the ability to change key provider configuration offline, and more. Learn about these features in the [`pg_tde` release notes](https://docs.percona.com/pg-tde/release-notes/rc.html) .

### Improved security and user experience for Docker images

- Percona Distribution for PostgreSQL Docker image is now based on Universal Base Image (UBI) version 9, which includes the latest security fixes. This makes the image compliant with the Red Hat certification and ensures the seamless work of containers on Red Hat OpenShift Container Platform.
- You no longer have to specify the `17.12-multi` tag when you run Percona Distribution for PostgreSQL in Docker. Instead, use the `percona/percona-distribution-postgresql:17.12`. Docker automatically identifies the architecture of your operating system and pulls the corresponding image. Refer to [Run in Docker](https://docs.percona.com/postgresql/17/docker.html) for how to get started.

### PostGIS is included into tarballs

We have extended Percona Distribution for PostgreSQL tarballs with PostGIS - an open-source extension to handle spatial data. This way you can install and run PostgreSQL as a geospatial database on hosts without a direct access to the Internet. Learn more about [installing from tarballs](https://docs.percona.com/postgresql/17/tarball.html) and [Spatial data manipulation](https://docs.percona.com/postgresql/17/solutions/postgis.html).

### Deprecation of meta packages

[Meta-packages for Percona Distribution for PostgreSQL](https://docs.percona.com/postgresql/17/repo-overview.html) are deprecated and will be removed in future releases.

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes. The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension                                                                  | Version | Description                                                                                                      |
| -------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------- |
| [etcd](https://etcd.io/)                                                   | 3.5.18  | A distributed, reliable key-value store for setting up high available Patroni clusters                           |
| [HAProxy](http://www.haproxy.org/)                                         | 2.8.13  | A high-availability and load-balancing solution                                                                  |
| [Patroni](https://patroni.readthedocs.io/en/latest/)                       | 4.0.5   | A HA (High Availability) solution for PostgreSQL                                                                 |
| [PgAudit](https://www.pgaudit.org/)                                        | 17.1    | Provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL       |
| [pgAudit set_user](https://github.com/pgaudit/set_user)                    | 4.1.0   | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance. |
| [pgBackRest](https://pgbackrest.org/)                                      | 2.54.2  | A backup and restore solution for PostgreSQL                                                                     |
| [pgBadger](https://github.com/darold/pgbadger)                             | 13.1    | A fast PostgreSQL Log Analyzer                                                                                   |
| [PgBouncer](https://www.pgbouncer.org/)                                    | 1.24.0  | A lightweight connection pooler for PostgreSQL                                                                   |
| [pg_gather](https://github.com/jobinau/pg_gather)                          | v29     | An SQL script for running the diagnostics of the health of a PostgreSQL cluster                                  |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary)      | 4.5.5   | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing  |
| [pg_repack](https://github.com/reorg/pg_repack)                            | 1.5.2   | Rebuilds PostgreSQL database objects                                                                             |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)              | 2.4.0   | Collects and aggregates statistics for PostgreSQL and provides histogram information                             |
| [pgvector](https://github.com/pgvector/pgvector)                           | v0.8.0  | A vector similarity search for PostgreSQL                                                                        |
| [PostGIS](https://github.com/postgis/postgis)                              | 3.3.8   | A spatial extension for PostgreSQL                                                                               |
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common) | 267     | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously           |
| [wal2json](https://github.com/eulerto/wal2json)                            | 2.6     | A PostgreSQL logical decoding JSON output plugin                                                                 |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains “a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.”
