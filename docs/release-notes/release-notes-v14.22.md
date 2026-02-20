# Percona Distribution for PostgreSQL 14.22 ({{date.14_22}})

[Installation](../installing.md){.md-button}

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 14.22](https://www.postgresql.org/docs/14/release-14-22.html).

## Release Highlights

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- pgBouncer: 1.25.1
- etcd: 3.5.26
- haproxy: 2.8.18
- pgBadger: 13.2
- postgresql-common: 288
- pgbackrest: 2.58.0
- pgpool2: 4.7.0
- pg_stat_monitor: 2.3.2
- postgis: 3.5.5
- ydiff: 1.4.2

See [Install Percona Distribution for PostgreSQL from binary tarballs](../tarball.md) for the download links.

### Addressed CVEs

This release includes important security measures that address the following CVEs: CVE-2026-2003, CVE-2026-2004, CVE-2026-2005, CVE-2026-2006. For more details, see the [PostgreSQL 14.22](https://www.postgresql.org/docs/14/release-14-22.html).

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

Review each extension's release notes for What's new, improvements, or bug fixes.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension                                                                              | Version   | Description                                                                                                          |
|----------------------------------------------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------|
| [etcd](https://etcd.io/)                                                               | 3.5.26    | A distributed, reliable key-value store for setting up high available Patroni clusters                              |
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/)                       | 0.4.5    | A Python client library for interacting with etcd                                 |
| [HAProxy](https://www.haproxy.org/)                                                    | 2.8.18    | A high-availability and load-balancing solution                                                                     |
| [Patroni](https://patroni.readthedocs.io/en/latest/)                                   | 4.1.0     | A HA (High Availability) solution for PostgreSQL                                                                    |
| [PgAudit](https://www.pgaudit.org/)                                                    | 1.6.3     | Provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL          |
| [pgAudit set_user](https://github.com/pgaudit/set_user)                                | 4.2.0     | Provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks. |
| [pgBackRest](https://pgbackrest.org/)                                                  | 2.58.0    | A backup and restore solution for PostgreSQL                                                                        |
| [pgBadger](https://github.com/darold/pgbadger)                                         | 13.2      | A fast PostgreSQL Log Analyzer.                                                                                      |
| [PgBouncer](https://www.pgbouncer.org/)                                                | 1.25.1    | A lightweight connection pooler for PostgreSQL                                                                      |
| [pg_gather](https://github.com/jobinau/pg_gather)                                      | v32       | An SQL script for running the diagnostics of the health of PostgreSQL cluster                                       |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary)                  | 4.7.0     | A middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.      |
| [pg_repack](https://github.com/reorg/pg_repack)                                        | 1.5.3     | Rebuilds PostgreSQL database objects                                                                                |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | 2.3.2 | Collects and aggregates statistics for PostgreSQL and provides histogram information. |
| [pgvector](https://github.com/pgvector/pgvector)                                       | v0.8.1    | A vector similarity search for PostgreSQL                                                                           |
| [PostGIS](https://github.com/postgis/postgis)                                          | 3.5.5     | A spatial extension for PostgreSQL.                                                                                  |
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common)             | 289       | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters may be maintained at one time. |
| [wal2json](https://github.com/eulerto/wal2json)                                        | 2.6       | A PostgreSQL logical decoding JSON output plugin                                                                    |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the  supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/14/libpq.html) library. It contains "a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."
