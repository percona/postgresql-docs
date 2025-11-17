# Percona Distribution for PostgreSQL 18.1.1 ({{date.18_1_1}})

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 18.1.1 - a binary compatible, open source drop in replacement of [PostgreSQL Community 18.1](https://www.postgresql.org/docs/18/release-18-1.html).

It introduces several major enhancements, such as:

- **Parallel logical replication** for improved throughput during initial data synchronization
- **Faster in-place upgrades** via `pg_upgrade` performance improvements
- **Enhanced monitoring** with new statistics views for `pg_stat_io` and background writer activity
- **Security improvements**, including expanded SSL/TLS configuration options
- **Performance optimizations** for query execution and index management
- Added support for **asynchronous I/O (AIO)** with PostgreSQL 18.1.1 which is now the default I/O mechanism.

These features make PostgreSQL 18 a major step forward in scalability, observability, and operational efficiency.

## Release Highlights

This release continues to deliver Percona’s open source value-add components for enterprise use cases, including `pg_stat_monitor` 2.3.1 for advanced query-level observability, `pg_tde` 2.1 for Transparent Data Encryption and more. See the full component list below for details.

!!! note
  To upgrade from earlier versions (e.g. Percona Distribution for PostgreSQL 17.x), follow the steps in [Upgrading Percona Distribution for PostgreSQL](major-upgrade.md).

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- LIBXSLT: 1.1.43
- LUA: 5.3.6
- LIBTIFF: 4.7.0
- EXPAT: 2.5.0
- PGPOOL: 4.6.2
- PGBACKREST: 2.56.0
- PATRONI: 4.0.6

See [Install Percona Distribution for PostgreSQL from binary tarballs](../tarball.md) for the download links.

### Addressed CVEs

This release includes important security measures that address the following CVEs: CVE-2025-12817, CVE-2025-12818. For more details, see the [PostgreSQL 18.1 release notes](https://www.postgresql.org/docs/18/release-18-1.html).

## Known Issues

### For minor & major upgrades (RHEL only)

During an upgrade on RHEL, you may encounter the following error:

```bash
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

## MD5 Authentication Deprecated

The md5 password authentication is deprecated now and will be removed in a future release.

## Percona Telemetry Extension for PostgreSQL Deprecated

The `percona_pg_telemetry` has been deprecated and replaced with a backwards compatibility stub.

No telemetry data will be gathered, it will not be maintained going forward and it should not be used in new deployments.

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension                                                                            | Version   | Description                                                                                                          |
|--------------------------------------------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------|
| [etcd :octicons-link-external-16:](https://etcd.io/)                                                             | 3.5.24   | A distributed, reliable key-value store for setting up highly available Patroni clusters    |
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/)                       | 0.4.5    | A Python client library for interacting with etcd                                 |
| [HAProxy :octicons-link-external-16:](http://www.haproxy.org/)                       | 2.8.16    | A high-availability and load-balancing solution                                                                     |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/)     | 4.1.0     | A HA (High Availability) solution for PostgreSQL                                                                    |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/)                      | 18.0      | A detailed session or object audit logging via the standard logging facility provided by PostgreSQL          |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user)  | 4.2.0     | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance.     |
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/)                    | 2.57.0    | A backup and restore solution for PostgreSQL                                                                        |
| [pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger)           | 13.1      | A fast PostgreSQL Log Analyzer                                                                                      |
| [PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/)                  | 1.25.0    | A lightweight connection pooler for PostgreSQL                                                                      |
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather)        | v31       | An SQL script for running the diagnostics of the health of a PostgreSQL cluster                                     |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.6.3 | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing      |
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack)          | 1.5.3     | Rebuilds PostgreSQL database objects                                                                                |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)                          | 2.3.1     | Collects and aggregates statistics for PostgreSQL and provides histogram information.                                |
| [pgvector :octicons-link-external-16:](https://github.com/pgvector/pgvector)         | v0.8.1    | A vector similarity search for PostgreSQL                                                                           |
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis)            | 3.5.4     | A spatial extension for PostgreSQL                                                                                  |
| [PostgreSQL Common :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common) | 287 | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously              |
| [wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json)          | 2.6       | A PostgreSQL logical decoding JSON output plugin                                                                    |
| [pg_tde :octicons-link-external-16:](https://github.com/percona/pg_tde)          | v2.1       | A PostgreSQL extension that provides Transparent Data Encryption (TDE) to protect data at rest                                                                    |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/18/libpq.html) library. It contains "a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."
