# Percona Distribution for PostgreSQL 16.11 ({{date.16_11}})

[Installation](../installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 16.11](https://www.postgresql.org/docs/16/release-16-11.html).

## Release Highlights

### Percona Telemetry Extension for PostgreSQL Deprecated

The `percona_pg_telemetry` extension has been deprecated and replaced with a backwards compatibility stub to avoid breaking existing installations.

No telemetry data will be gathered, it will not be maintained going forward and it should not be used in new deployments.

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- pgbouncer: 1.25.0
- pgpool2: 4.6.3
- etcd: 3.5.24
- PostGIS: 3.5.4
- set_user: 4.2.0
- pg_repack: 1.5.3
- pg_stat_monitor: 2.3.1
- pgBackRest: 2.57.0
- Patroni: 4.1.0
- HAProxy: 2.8.16
- pgvector: 0.8.1
- libxml2: 2.12.10

See [Install Percona Distribution for PostgreSQL from binary tarballs](../tarball.md) for the download links.

The [installation preconditions for tarballs](../tarball.md) now include an extra step for RHEL, Rocky Linux, or Oracle Linux 10: installing the `acl` package.

### Addressed CVEs

This release includes important security measures that address the following CVEs: CVE-2025-12817, CVE-2025-12818. For more details, see the PostgreSQL [16.11 release notes](https://www.postgresql.org/docs/17/release-16-11.html).

## Bug Fixes

This release includes several stability fixes introduced in the community PostgreSQL 16.11 update:

- Fix logic related to caching result-relation metadata for triggers when partitions do not share identical physical column sets with their parent tables.
- Fix EvalPlanQual handling for foreign or custom joins where no alternative local join plan exists.
- Fix a use-after-free condition in the relation synchronization cache used by the `pgoutput` logical decoding plugin.
- Fix incorrect message formatting when checking for Windows administrator privilege.
- Fix crash scenarios triggered when PostgreSQL is tested using certain `libsanitizer` options.

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
| [etcd](https://etcd.io/)| 3.5.24 | A distributed, reliable key-value store for setting up high available Patroni clusters |
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/)                       | 0.4.5    | A Python client library for interacting with etcd |
| [HAProxy](http://www.haproxy.org/) | 2.8.16 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 4.1.0 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/) | 16.1 | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 4.2.0 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/) | 2.57.0 | a backup and restore solution for PostgreSQL |
| [pgBadger](https://github.com/darold/pgbadger) | 13.1 | a fast PostgreSQL Log Analyzer. |
| [PgBouncer](https://www.pgbouncer.org/) | 1.25.0 | a lightweight connection pooler for PostgreSQL |
| [pg_gather](https://github.com/jobinau/pg_gather) | v32 | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.6.3 | a middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing. |
| [pg_repack](https://github.com/reorg/pg_repack) | 1.5.3 | rebuilds PostgreSQL database objects |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | 2.3.1 | collects and aggregates statistics for PostgreSQL and provides histogram information. |
| [pg_vector](https://github.com/pgvector/pgvector) | v0.8.1 | A vector similarity search for PostgreSQL |
| [PostGIS](https://github.com/postgis/postgis) | 3.5.4 | a spatial extension for PostgreSQL. |
| [PostgreSQL Commons](https://salsa.debian.org/postgresql/postgresql-common) | 287 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time. |
| [wal2json](https://github.com/eulerto/wal2json) | 2.6 | a PostgreSQL logical decoding JSON output plugin |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/16/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries."
