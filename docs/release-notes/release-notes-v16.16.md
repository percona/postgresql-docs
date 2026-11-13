# Percona Distribution for PostgreSQL 16.16 ({{date.16_16}})

[Installation](../installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 16.16](https://www.postgresql.org/docs/16/release-16-16.html).

## Release Highlights

This release continues to deliver Percona’s open source value-add components for enterprise use cases, see the full component list below for details.

!!! note
    To upgrade from earlier versions (e.g. Percona Distribution for PostgreSQL 15.x), follow the steps in [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md).

### Added `credcheck` extension

Percona Distribution for PostgreSQL now includes the [`credcheck` :octicons-link-external-16:](https://github.com/HexaCluster/credcheck) extension. `credcheck` enforces credential policies when users are created, renamed, or change their passwords. For example, it can set minimum password length, require certain character types, block passwords that contain the username, and prevent password reuse.

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- credcheck: 6.0
- etcd: 3.5.35
- haproxy: 2.8.31
- pgaudit_set_user: 4.3.0
- pgBackRest: 2.60.0
- pgbadger: 13.3
- pgbouncer: 1.26.1
- pgpool2: 4.7.3
- pgvector: 0.8.7
- postgres-common: 294
- wal2json: 2.7

See [Install Percona Distribution for PostgreSQL from binary tarballs](../tarball.md) for the download links.

### Addressed CVEs

This release includes important security measures that address the following CVEs:

- [CVE-2026-6460](https://www.cve.org/CVERecord?id=CVE-2026-6460)
- [CVE-2026-6467](https://www.cve.org/CVERecord?id=CVE-2026-6467)
- [CVE-2026-14661](https://www.cve.org/CVERecord?id=CVE-2026-14661)
- [CVE-2026-16237](https://www.cve.org/CVERecord?id=CVE-2026-16237)
- [CVE-2026-16240](https://www.cve.org/CVERecord?id=CVE-2026-16240)
- [CVE-2026-18447](https://www.cve.org/CVERecord?id=CVE-2026-18447)
- [CVE-2026-116303](https://www.cve.org/CVERecord?id=CVE-2026-116303)
- [CVE-2026-116304](https://www.cve.org/CVERecord?id=CVE-2026-116304)
- [CVE-2026-116306](https://www.cve.org/CVERecord?id=CVE-2026-116306)
- [CVE-2026-116307](https://www.cve.org/CVERecord?id=CVE-2026-116307)
- [CVE-2026-116308](https://www.cve.org/CVERecord?id=CVE-2026-116308)
- [CVE-2026-116309](https://www.cve.org/CVERecord?id=CVE-2026-116309)
- [CVE-2026-116311](https://www.cve.org/CVERecord?id=CVE-2026-116311)
- [CVE-2026-116312](https://www.cve.org/CVERecord?id=CVE-2026-116312)
- [CVE-2026-116314](https://www.cve.org/CVERecord?id=CVE-2026-116314)
- [CVE-2026-116315](https://www.cve.org/CVERecord?id=CVE-2026-116315)
- [CVE-2026-116316](https://www.cve.org/CVERecord?id=CVE-2026-116316)
- [CVE-2026-116317](https://www.cve.org/CVERecord?id=CVE-2026-116317)
- [CVE-2026-116319](https://www.cve.org/CVERecord?id=CVE-2026-116319)
- [CVE-2026-116320](https://www.cve.org/CVERecord?id=CVE-2026-116320)
- [CVE-2026-116321](https://www.cve.org/CVERecord?id=CVE-2026-116321)
- [CVE-2026-116323](https://www.cve.org/CVERecord?id=CVE-2026-116323)
- [CVE-2026-116326](https://www.cve.org/CVERecord?id=CVE-2026-116326)
- [CVE-2026-116327](https://www.cve.org/CVERecord?id=CVE-2026-116327)
- [CVE-2026-116328](https://www.cve.org/CVERecord?id=CVE-2026-116328)
- [CVE-2026-116330](https://www.cve.org/CVERecord?id=CVE-2026-116330)
- [CVE-2026-116331](https://www.cve.org/CVERecord?id=CVE-2026-116331)
- [CVE-2026-116332](https://www.cve.org/CVERecord?id=CVE-2026-116332)
- [CVE-2026-116335](https://www.cve.org/CVERecord?id=CVE-2026-116335)
- [CVE-2026-116336](https://www.cve.org/CVERecord?id=CVE-2026-116336)
- [CVE-2026-120139](https://www.cve.org/CVERecord?id=CVE-2026-120139)
- [CVE-2026-120141](https://www.cve.org/CVERecord?id=CVE-2026-120141)
- [CVE-2026-120143](https://www.cve.org/CVERecord?id=CVE-2026-120143)
- [CVE-2026-120145](https://www.cve.org/CVERecord?id=CVE-2026-120145)
- [CVE-2026-120146](https://www.cve.org/CVERecord?id=CVE-2026-120146)
- [CVE-2026-120147](https://www.cve.org/CVERecord?id=CVE-2026-120147)
- [CVE-2026-120148](https://www.cve.org/CVERecord?id=CVE-2026-120148)
- [CVE-2026-120149](https://www.cve.org/CVERecord?id=CVE-2026-120149)
- [CVE-2026-120150](https://www.cve.org/CVERecord?id=CVE-2026-120150)
- [CVE-2026-120151](https://www.cve.org/CVERecord?id=CVE-2026-120151)
- [CVE-2026-120152](https://www.cve.org/CVERecord?id=CVE-2026-120152)
- [CVE-2026-120153](https://www.cve.org/CVERecord?id=CVE-2026-120153)
- [CVE-2026-120154](https://www.cve.org/CVERecord?id=CVE-2026-120154)

For more details, see the [PostgreSQL 16.16 release notes](https://www.postgresql.org/docs/16/release-16-16.html).

## Known Issue

### For minor & major upgrades (RHEL only)

During an upgrade on RHEL, you may encounter the following error:

```
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

On RHEL 10, some earlier releases may have installed the distribution's PostgreSQL 18 packages, causing the following error:

```
file /lib/systemd/system/postgresql.service from install of percona-postgresql-common conflicts with file from package postgresql18-server
```

!!! warning
    Before you remove anything, make sure your database runs on Percona Distribution for PostgreSQL and not on the
    distribution's PostgreSQL 18.

To resolve this, remove the distribution's PostgreSQL packages before upgrading:

```bash
sudo dnf remove postgresql18-server postgresql18 postgresql18-private-libs
```

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension | Version | Description |
| --- | --- | --- |
| [credcheck :octicons-link-external-16:](https://github.com/HexaCluster/credcheck) | 6.0 | Enforces username and password policies during role creation, renaming, and password changes |
| [etcd :octicons-link-external-16:](https://etcd.io/) | 3.5.35 | A distributed, reliable key-value store for setting up highly available Patroni clusters |
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/) | 0.4.5 | A Python client library for interacting with etcd |
| [HAProxy :octicons-link-external-16:](https://www.haproxy.org/) | 2.8.31 | A high-availability and load-balancing solution |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) | 4.1.5 | A HA (High Availability) solution for PostgreSQL |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/) | 16.1 | A detailed session or object audit logging via the standard logging facility provided by PostgreSQL |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user) | 4.3.0 | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance |
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/) | 2.60.0 | A backup and restore solution for PostgreSQL |
| [pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger) | 13.3 | A fast PostgreSQL log analyzer |
| [PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/) | 1.26.1 | A lightweight connection pooler for PostgreSQL |
| [pg_cron :octicons-link-external-16:](https://github.com/citusdata/pg_cron) | 1.6.8 | A simple cron-based job scheduler for PostgreSQL |
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather) | v33 | An SQL script for running diagnostics on the health of a PostgreSQL cluster |
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) | 1.5.3 | Rebuilds PostgreSQL database objects |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | 2.4.0 | Collects and aggregates statistics for PostgreSQL and provides histogram information |
| [pg_vector](https://github.com/pgvector/pgvector) | v0.8.7 | A vector similarity search extension for PostgreSQL |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.7.3 | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing |
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis) | 3.5.7 | A spatial extension for PostgreSQL |
| [PostgreSQL Commons :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common) | 294 | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously |
| [wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json) | 2.7 | A PostgreSQL logical decoding JSON output plugin |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/16/libpq.html) library. It contains "a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."
