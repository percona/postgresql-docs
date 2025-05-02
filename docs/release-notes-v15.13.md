# Percona Distribution for PostgreSQL 15.13 ({{date.15_13}})

[Installation](installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 15.11](https://www.postgresql.org/docs/current/release-15-11.html) and [PostgreSQL 15.12](https://www.postgresql.org/docs/current/release-15-12.html).

## Release Highlights

This release fixes [CVE-2025-1094](https://www.postgresql.org/support/security/CVE-2025-1094/), which closed a vulnerability in the `libpq` PostgreSQL client library but introduced a regression related to string handling for non-null terminated strings. The error would be visible based on how a PostgreSQL client implemented this behavior. This regression affects versions 17.3, 16.7, 15.11, 14.16, and 13.19. For this reason, version 15.11 was skipped.

### Improved security and user experience for Docker images

* Percona Distribution for PostgreSQL Docker image is now based on Universal Base Image (UBI) version 9, which includes the latest security fixes. This makes the image compliant with the Red Hat certification and ensures the seamless work of containers on Red Hat OpenShift Container Platform.

* You no longer have to specify the `{{dockertag}}-multi` tag when you run Percona Distribution for PostgreSQL in Docker. Instead, use the `percona/percona-distribution-postgresql:{{dockertag}}`. Docker automatically identifies the architecture of your operating system and pulls the corresponding image. Refer to [Run in Docker](docker.md) for how to get started.

### PostGIS is included into tarballs

We have extended Percona Distribution for PostgreSQL tarballs with PostGIS - an open-source extension to handle spacial data. This way you can install and run PostgreSQL as a geospatial database on hosts without a direct access to the Internet. Learn more about [installing from tarballs](tarball.md) and [Spacial data manipulation](solutions/postgis.md).

## Deprecation of meta packages

[Meta-packages for Percona Distribution for PostgreSQL](repo-overview.md#repository-contents) are deprecated and will be removed in future releases.

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes. The following is the list of extensions available in Percona Distribution for PostgreSQL.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [etcd :octicons-link-external-16:](https://etcd.io/) | 3.5.18 | A distributed, reliable key-value store for setting up high available Patroni clusters |
| [HAProxy :octicons-link-external-16:](http://www.haproxy.org/) | 2.8.13 | a high-availability and load-balancing solution |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) | 4.0.4 | a HA (High Availability) solution for PostgreSQL |
| [pgaudit :octicons-link-external-16:](https://www.pgaudit.org/) | 1.7.0 | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL |
| [pgaudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user) | 4.1.0 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks. |
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/) | 2.54.2 | a backup and restore solution for PostgreSQL |
| [pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger) | 13.0 | a fast PostgreSQL Log Analyzer. |
| [PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/) | 1.24.0 | a lightweight connection pooler for PostgreSQL |
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather) | v29 | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.5.5 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing. |
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) | 1.5.2 | rebuilds PostgreSQL database objects |
| [pg_stat_monitor :octicons-link-external-16:](https://github.com/percona/pg_stat_monitor) | {{pgsmversion}} | collects and aggregates statistics for PostgreSQL and provides histogram information. |
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis) | 3.3.8 | a spatial extension for PostgreSQL. |
| [pgvector :octicons-link-external-16:](https://github.com/pgvector/pgvector) | v0.8.0 | A vector similarity search for PostgreSQL |
| [PostgreSQL Common :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common) | 267 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time. |
| [wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json) | 2.6 | a PostgreSQL logical decoding JSON output plugin |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/15/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries."
