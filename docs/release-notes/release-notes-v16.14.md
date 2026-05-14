# Percona Distribution for PostgreSQL 16.14 ({{date["16_14"] | default("unreleased")}})

[Installation](../installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 16.14](https://www.postgresql.org/docs/16/release-16-14.html).

## Release Highlights

This release continues to deliver Percona’s open source value-add components for enterprise use cases, see the full component list below for details.

!!! note
    To upgrade from earlier versions (e.g. Percona Distribution for PostgreSQL 15.x), follow the steps in [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md).

### Ubuntu 26.04 LTS support added

 Percona Distribution for PostgreSQL is available on Ubuntu 26.04 LTS (Noble Numbat's successor). Packages are provided for AMD64 and ARM64 architectures.

### Added Quick Start guide

Added a Quick Start Guide walking users through setting up Percona Distribution for PostgreSQL with minimal steps and linking to more advanced topics.

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- postgres-common: 290
- pgBouncer: 1.25.2
- etcd: 3.5.30
- pysyncobj: 0.3.15
- haproxy: 2.8.23
- patroni: 4.1.3
- pgpool2: 4.7.1
- postgis: 3.5.6
- pg_gather: 33
- pg_cron: 1.6.7

See [Install Percona Distribution for PostgreSQL from binary tarballs](../tarball.md) for the download links.

### Addressed CVEs

This release includes important security measures that address the following CVEs: CVE-2026-6479, CVE-2026-6473, CVE-2026-6474, CVE-2026-6472, CVE-2026-6478, CVE-2026-6477, CVE-2026-6475, CVE-2026-6637. For more details, see the PostgreSQL [16.14 release notes](https://www.postgresql.org/docs/16/release-16-14.html).

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

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [etcd](https://etcd.io/) | 3.5.30 | A distributed, reliable key-value store for setting up high available Patroni clusters |
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/)                       | 0.4.5    | A Python client library for interacting with etcd |
| [HAProxy](http://www.haproxy.org/) | 2.8.23 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 4.1.3 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/) | 16.1 | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL |
| [pgAudit set_user](https://github.com/pgaudit/set_user) | 4.2.0 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks. |
| [pgBackRest](https://pgbackrest.org/) | 2.58.0 | a backup and restore solution for PostgreSQL |
| [pgBadger](https://github.com/darold/pgbadger) | 13.2 | a fast PostgreSQL Log Analyzer. |
| [PgBouncer](https://www.pgbouncer.org/) | 1.25.2 | a lightweight connection pooler for PostgreSQL |
| [pg_gather](https://github.com/jobinau/pg_gather) | v33 | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.7.1 | a middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing. |
| [pg_repack](https://github.com/reorg/pg_repack) | 1.5.3 | rebuilds PostgreSQL database objects |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | 2.3.2 | collects and aggregates statistics for PostgreSQL and provides histogram information. |
| [pg_vector](https://github.com/pgvector/pgvector) | v0.8.1 | A vector similarity search for PostgreSQL |
| [PostGIS](https://github.com/postgis/postgis) | 3.5.6 | a spatial extension for PostgreSQL. |
| [PostgreSQL Commons](https://salsa.debian.org/postgresql/postgresql-common) | 290 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time. |
| [wal2json](https://github.com/eulerto/wal2json) | 2.6 | a PostgreSQL logical decoding JSON output plugin |
| [pg_cron :octicons-link-external-16:](https://github.com/citusdata/pg_cron) | 1.6.7 | a simple cron-based job scheduler for PostgreSQL |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/16/libpq.html) library. It contains "a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."
