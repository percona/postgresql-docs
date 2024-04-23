# Percona Distribution for PostgreSQL 16.2 (2024-02-27)

[Installation](installing.md){.md-button}

Percona Distribution for PostgreSQL is a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 16.2 :octicons-link-external-16:](https://www.postgresql.org/docs/16/release-16-2.html). 

## Release Highlights

* A Docker image for Percona Distribution for PostgreSQL is now available for ARM architectures. This improves the user experience with the Distribution for developers with ARM-based workstations.


The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
|[HAProxy :octicons-link-external-16:](http://www.haproxy.org/) | 2.8.5 | a high-availability and load-balancing solution |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) | 3.2.2 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/)             | 16   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user)| 4.0.1 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/)           | 2.50    | a backup and restore solution for PostgreSQL       |
|[pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger)   | 12.4     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/)          |1.22.0    | a lightweight connection pooler for PostgreSQL|
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather)| v25     | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.5.0 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) | 1.5.0   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor :octicons-link-external-16:](https://github.com/percona/pg_stat_monitor)|2.0.4 | collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis) | 3.3.5 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common)| 256 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json)  |2.5       | a PostgreSQL logical decoding JSON output plugin|

Percona Distribution for PostgreSQL also includes the following packages:

* `llvm` 12.0.1 packages for Red Hat Enterprise Linux 8 and compatible derivatives. This fixes compatibility issues with LLVM from upstream.
* supplemental `ETCD` packages which can be used for setting up Patroni clusters. These packages are available for the following operating systems:

|  Operating System     | Package              | Version | Description        |
| --------------------- | ---------------------| --------| ------------------ |
| RHEL 8 and derivatives| `etcd`               | 3.5.12  | A consistent, distributed key-value store|
|                       | `python3-etcd`| 0.4.5   | A Python client for ETCD  |


                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq :octicons-link-external-16:](https://www.postgresql.org/docs/16/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
