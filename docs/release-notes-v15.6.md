# Percona Distribution for PostgreSQL 15.6 (2024-02-)

[Installation](installing.md){.md-button}

Percona Distribution for PostgreSQL is a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 15.6](https://www.postgresql.org/docs/current/release-15-6.html). 

## Release Highlights

* A Docker image for Percona Distribution for PostgreSQL is now available for ARM architectures. This improves the user experience with the Distribution for developers with ARM-based workstations.

------------------------------------------------------------------------------

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
|[HAProxy](http://www.haproxy.org/) | 2.8.5 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 3.2.2 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/)             | 1.7.0   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 4.0.1 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.50    | a backup and restore solution for PostgreSQL       |
|[pgBadger](https://github.com/darold/pgbadger)   | 12.4     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer](https://www.pgbouncer.org/)          |1.22.0    | a lightweight connection pooler for PostgreSQL|
| [pg_gather](https://github.com/jobinau/pg_gather)| v25     | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.5.0 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack](https://github.com/reorg/pg_repack) | 1.5.0   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)|2.0.4 | collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostGIS](https://github.com/postgis/postgis) | 3.3.5 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common)| 256 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[wal2json](https://github.com/eulerto/wal2json)  |2.5       | a PostgreSQL logical decoding JSON output plugin|


Percona Distribution for PostgreSQL also includes the following packages:

* `llvm` 12.0.1 packages for Red Hat Enterprise Linux 8 and compatible derivatives. This fixes compatibility issues with LLVM from upstream.
* supplemental `ETCD` packages which can be used for setting up Patroni clusters. These packages are available for the following operating systems:

|  Operating System   | Package              | Version | Description        |
| ------------------- | ---------------------| --------| ------------------ |
| RHEL 8            | `etcd`               | 3.5.12  | A consistent, distributed key-value store|
|                     | `python3-python-etcd`| 0.4.5   | A Python client for ETCD     |

                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/15/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
