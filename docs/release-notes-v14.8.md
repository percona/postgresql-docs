# Percona Distribution for PostgreSQL 14.8 (2023-06-28)


| Release date:     | June 28, 2023        |
|:------------------|:-----------------------|
| **Installation**: | [Installing Percona Distribution for PostgreSQL](installing.md) |

Percona Distribution for PostgreSQL is a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 14.8](https://www.postgresql.org/docs/14/release-14-8.html). 

## Release Highlights

* Percona Distribution for PostgreSQL components now include [PostGIS](https://postgis.net/) - the open source extension that allows storing and manipulating spatial data in PostgreSQL.

------------------------------------------------------------------------------

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
|[HAProxy](https://www.haproxy.org/) | 2.6.13 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 3.0.2 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/)             | 1.6.2   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 4.0.1 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.44    | a backup and restore solution for PostgreSQL       |
|[pgBadger](https://github.com/darold/pgbadger)   | 12.1     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer](https://www.pgbouncer.org/)          |1.19.1    | a lightweight connection pooler for PostgreSQL|
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.4.3 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.8   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)|2.0.1 | collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostGIS](https://github.com/postgis/postgis) | 3.3.3 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common)| 250 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters may be maintained at one time.|
|[wal2json](https://github.com/eulerto/wal2json)  |2.5       | a PostgreSQL logical decoding JSON output plugin|


Percona Distribution for PostgreSQL also includes the following packages:

* `llvm` 12.0.1 packages for Red Hat Enterprise Linux 8 and derivatives. This fixes compatibility issues with LLVM from upstream.
* supplemental `etcd` packages which can be used for setting up Patroni clusters. These packages are available for the following operating systems:

|  Operating system  | Package              | Version | Description        |
| ------------------ | ---------------------| --------| ------------------ |
| RHEL 7              |`python3-python-etcd` | 0.4.3   | A Python client for etcd     |
| RHEL 8             | `etcd`               | 3.3.11  | A consistent, distributed key-value store |
|                    | `python3-python-etcd`| 0.4.3   | A Python client for etcd |
                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/14/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
