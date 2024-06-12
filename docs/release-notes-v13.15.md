# Percona Distribution for PostgreSQL 13.15 (2024-06-10)

[Installation](installing.md){.md-button}

Percona Distribution for PostgreSQL is a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Spatial data handling, Observability, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 13.15](https://www.postgresql.org/docs/13/release-13-15.html).

## Release Highlights

* Percona Distribution for PostgreSQL now includes the etcd distributed configuration store version 3.5.x for all supported operating systems. This enhancement simplifies deploying high-availability solutions because you can install all necessary components from a single source, ensuring their seamless compatibility.
* Percona Distribution for PostgreSQL is now available on Ubuntu 24.04 LTS Noble Numbat.
* Percona Distribution for PostgreSQL on Red Hat Enterprise Linux 8 and compatible derivatives is now fully compatible with upstream `llvm` packages and includes the latest version 16.0.6 of them. 

    To ensure a smooth upgrade process, the recommended approach is to  **upgrade to the latest minor version within your current major version before going to the next major version**. For example, if you're currently on 12.18, upgrade to 12.19 first, then you can upgrade to 13.15. This two-step approach avoids any potential conflicts caused by differing `llvm` versions on Red Hat Enterprise Linux 8 and compatible derivatives.


----------------------------------------------------------------------------

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [etcd](https://etcd.io/)| 3.5.13 | A distributed, reliable key-value store for setting up high available Patroni clusters |
|[HAProxy](http://www.haproxy.org/) | 2.8.9 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 3.3.0 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/)             | 1.5.2   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 4.0.1 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.51    | a backup and restore solution for PostgreSQL       |
|[pgBadger](https://github.com/darold/pgbadger)   | 12.4     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer](https://www.pgbouncer.org/)          |1.22.1    | a lightweight connection pooler for PostgreSQL|
| [pg_gather](https://github.com/jobinau/pg_gather)| v26     | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.5.1 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack](https://github.com/reorg/pg_repack) | 1.5.0   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)|{{pgsmversion}} | collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostGIS](https://github.com/postgis/postgis) | 3.3.6 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common)| 259 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[wal2json](https://github.com/eulerto/wal2json)  |2.6       | a PostgreSQL logical decoding JSON output plugin|

Percona Distribution for PostgreSQL on Red Hat Enterprise Linux 8 and compatible derivatives also includes the following packages:

* `llvm` 16.0.6 packages. This fixes compatibility issues with LLVM from upstream.
* supplemental `python3-etcd` packages, which can be used for setting up Patroni clusters. 

                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/13/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
