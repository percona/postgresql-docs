# Percona Distribution for PostgreSQL 15.19 ({{date.15_19}})

[Installation](installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 15.19](https://www.postgresql.org/docs/15/release-15-19.html).

## Release Highlights

This release continues to deliver Percona’s open source value-add components for enterprise use cases, see the full component list below for details.

!!! note
    To upgrade from earlier versions (e.g. Percona Distribution for PostgreSQL 14.x), follow the steps in [Upgrading Percona Distribution for PostgreSQL](major-upgrade.md).

### Removed dependency on percona-telemetry-agent

The hard depencency on `percona-pg-telemetry`, which has been a stub since 1.2.0, has been replaced by a weak one and additionally the `percona-pg-telemetry`package no longer installs the telemertry agent (`percona-telemetry-agent`).

See [Telemetry Agent dependencies and removal considerations](telemetry.md#telemetry-agent-dependencies-and-removal-considerations) for details.

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- etcd: 3.5.33
- haproxy: 2.8.27
- patroni: 4.1.4
- pgBackRest: 2.59.0
- pgpool2: 4.7.2
- pgvector: 0.8.6
- postgis: 3.5.7
- postgres-common: 293

See [Install Percona Distribution for PostgreSQL from binary tarballs](tarball.md) for the download links.

### Addressed CVEs

This release includes important security measures that address the following CVEs:

- CVE-2026-6464
- CVE-2026-6469
- CVE-2026-6470
- CVE-2026-6471
- CVE-2026-14662
- CVE-2026-14663
- CVE-2026-14664
- CVE-2026-14666
- CVE-2026-14668
- CVE-2026-14669
- CVE-2026-14672
- CVE-2026-14679
- CVE-2026-14680
- CVE-2026-14681
- CVE-2026-15741
- CVE-2026-16238
- CVE-2026-16239
- CVE-2026-16241
- CVE-2026-18024

For more details, see the [PostgreSQL 15.19 release notes](https://www.postgresql.org/docs/15/release-15-19.html).

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

| Extension | Version | Description |
| --- | --- | --- |
| [etcd :octicons-link-external-16:](https://etcd.io/) | 3.5.33 | A distributed, reliable key-value store for setting up highly available Patroni clusters |
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/) | 0.4.5 | A Python client library for interacting with etcd |
| [HAProxy :octicons-link-external-16:](https://www.haproxy.org/) | 2.8.27 | A high-availability and load-balancing solution |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) | 4.1.4 | A HA (High Availability) solution for PostgreSQL |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/) | 1.7.1 | A detailed session or object audit logging via the standard logging facility provided by PostgreSQL |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user) | 4.2.0 | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance |
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/) | 2.59.0 | A backup and restore solution for PostgreSQL |
| [pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger) | 13.2 | A fast PostgreSQL log analyzer |
| [PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/) | 1.25.2 | A lightweight connection pooler for PostgreSQL |
| [pg_cron :octicons-link-external-16:](https://github.com/citusdata/pg_cron) | 1.6.7 | A simple cron-based job scheduler for PostgreSQL |
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather) | v33 | An SQL script for running diagnostics on the health of a PostgreSQL cluster |
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) | 1.5.3 | Rebuilds PostgreSQL database objects |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | 2.3.2 | Collects and aggregates statistics for PostgreSQL and provides histogram information |
| [pg_vector](https://github.com/pgvector/pgvector) | v0.8.6 | A vector similarity search extension for PostgreSQL |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.7.2 | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing |
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis) | 3.5.7 | A spatial extension for PostgreSQL |
| [PostgreSQL Commons :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common) | 293 | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously |
| [wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json) | 2.6 | A PostgreSQL logical decoding JSON output plugin |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/15/libpq.html) library. It contains "a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."
