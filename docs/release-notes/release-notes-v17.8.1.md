# Percona Distribution for PostgreSQL 17.8.1 ({{date.17_8_1}})

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 17.8.1 - a binary compatible, open source drop in replacement of [PostgreSQL Community 17.8 :octicons-link-external-16:](https://www.postgresql.org/docs/17/release-17-8.html).

## Release Highlights

This release continues to deliver Percona’s open source value-add components for enterprise use cases, including `pg_stat_monitor` 2.3.2 for advanced query-level observability, `pg_tde` 2.1.2 for Transparent Data Encryption and more. See the full component list below for details.

!!! note
  To upgrade from earlier versions, follow the steps in [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md).

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- pgbouncer: 1.25.1
- pgpool2: 4.7.0
- etcd: 3.5.26
- PostGIS: 3.5.5
- pgBackRest: 2.58.0
- postgresql-common: 289
- pgBadger: 13.2
- HAProxy: 2.8.18
- pgsm: 2.3.2
- pg_tde: 2.1.2
- ydiff: 1.4.2

See [Install Percona Distribution for PostgreSQL from binary tarballs](../tarball.md) for the download links.

### Addressed CVEs

This release includes important security measures that address the following CVEs: CVE-2026-2003, CVE-2026-2004, CVE-2026-2005, CVE-2026-2006. For more details, see the PostgreSQL [17.8 release notes :octicons-link-external-16:](https://www.postgresql.org/docs/17/release-17-8.html).

## Known Issue

### For minor & major upgrades (RHEL only)

During an upgrade on RHEL, you may encounter the following error:

```
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension                                                                            | Version   | Description                                                                                                          |
|--------------------------------------------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------|
| [etcd :octicons-link-external-16:](https://etcd.io/)                                                             | 3.5.26    | A distributed, reliable key-value store for setting up highly available Patroni clusters
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/)                       | 0.4.5    | A Python client library for interacting with etcd                                 |
| [HAProxy :octicons-link-external-16:](http://www.haproxy.org/)                       | 2.8.18    | A high-availability and load-balancing solution                                                                     |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/)     | 4.1.0     | A HA (High Availability) solution for PostgreSQL                                                                    |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/)                      | 17.1      | A detailed session or object audit logging via the standard logging facility provided by PostgreSQL          |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user)  | 4.2.0     | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance.     |
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/)                    | 2.58.0    | A backup and restore solution for PostgreSQL                                                                        |
| [pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger)           | 13.2      | A fast PostgreSQL Log Analyzer                                                                                      |
| [PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/)                  | 1.25.1    | A lightweight connection pooler for PostgreSQL                                                                      |
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather)        | v32       | An SQL script for running the diagnostics of the health of a PostgreSQL cluster                                     |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.7.0 | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing      |
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack)          | 1.5.3     | Rebuilds PostgreSQL database objects
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)                          | 2.3.2     | Collects and aggregates statistics for PostgreSQL and provides histogram information.                                |
| [pgvector :octicons-link-external-16:](https://github.com/pgvector/pgvector)         | v0.8.1    | A vector similarity search for PostgreSQL                                                                           |
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis)            | 3.5.5     | A spatial extension for PostgreSQL                                                                                  |
| [PostgreSQL Common :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common) | 289 | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously              |
| [wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json)          | 2.6       | A PostgreSQL logical decoding JSON output plugin                                                                    |
| [pg_tde :octicons-link-external-16:](https://github.com/percona/pg_tde)          | v2.1.2       | A PostgreSQL extension that provides Transparent Data Encryption (TDE) to protect data at rest                                                                    |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains "a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."
