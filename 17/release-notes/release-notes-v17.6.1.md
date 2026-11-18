> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/17/llms.txt).

# Percona Distribution for PostgreSQL 17.6.1 (2025-09-10)

Percona Distribution for PostgreSQL is a solution that includes PostgreSQL server and the collection of tools from PostgreSQL community. These tools are tested to work together and serve to assist you in deploying and managing PostgreSQL.

The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability, and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 17.6.1 - a binary compatible, open source drop in replacement of [PostgreSQL Community 17.6](https://www.postgresql.org/docs/17/release-17-6.html).

## Release Highlights

### SBOMs available for download

Percona now provides Software Bill of Materials (SBOMs) to support compliance and security audits. SBOM files are available for tarball builds.

See [Software Bill of Materials (SBOMs)](https://docs.percona.com/postgresql/17/sboms.html) for the full list.

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components have new versions:

- LIBXSLT: 1.1.43
- LUA: 5.3.6
- LIBTIFF: 4.7.0
- EXPAT: 2.5.0
- PGPOOL: 4.6.2
- PGBACKREST: 2.56.0
- PATRONI: 4.0.6

See [Install Percona Distribution for PostgreSQL from binary tarballs](https://docs.percona.com/postgresql/17/tarball.html) for the download links.

### Addressed CVEs

This release includes important security measures that address the following CVEs: CVE-2012-0868, CVE-2017-7484, and CVE-2025-8715. For more details, see the [PostgreSQL 17.6 release notes](https://www.postgresql.org/docs/release/17.6/).

## Known Issue

### For minor & major upgrades (RHEL only)

During an upgrade on RHEL, you may encounter the following error:

```
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension                                                                  | Version | Description                                                                                                      |
| -------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------- |
| [etcd](https://etcd.io/)                                                   | 3.5.21  | A distributed, reliable key-value store for setting up highly available Patroni clusters                         |
| [python-etcd](https://python-etcd.readthedocs.io/en/latest/)               | 0.4.5   | A Python client library for interacting with etcd                                                                |
| [HAProxy](http://www.haproxy.org/)                                         | 2.8.15  | A high-availability and load-balancing solution                                                                  |
| [Patroni](https://patroni.readthedocs.io/en/latest/)                       | 4.0.6   | A HA (High Availability) solution for PostgreSQL                                                                 |
| [PgAudit](https://www.pgaudit.org/)                                        | 17.1    | A detailed session or object audit logging via the standard logging facility provided by PostgreSQL              |
| [pgAudit set_user](https://github.com/pgaudit/set_user)                    | 4.1.0   | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance. |
| [pgBackRest](https://pgbackrest.org/)                                      | 2.56.0  | A backup and restore solution for PostgreSQL                                                                     |
| [pgBadger](https://github.com/darold/pgbadger)                             | 13.1    | A fast PostgreSQL Log Analyzer                                                                                   |
| [PgBouncer](https://www.pgbouncer.org/)                                    | 1.24.1  | A lightweight connection pooler for PostgreSQL                                                                   |
| [pg_gather](https://github.com/jobinau/pg_gather)                          | v31     | An SQL script for running the diagnostics of the health of a PostgreSQL cluster                                  |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary)      | 4.6.2   | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing  |
| [pg_repack](https://github.com/reorg/pg_repack)                            | 1.5.2   | Rebuilds PostgreSQL database objects                                                                             |
| [pgvector](https://github.com/pgvector/pgvector)                           | v0.8.0  | A vector similarity search for PostgreSQL                                                                        |
| [PostGIS](https://github.com/postgis/postgis)                              | 3.3.8   | A spatial extension for PostgreSQL                                                                               |
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common) | 280     | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously           |
| [wal2json](https://github.com/eulerto/wal2json)                            | 2.6     | A PostgreSQL logical decoding JSON output plugin                                                                 |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains “a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.”
