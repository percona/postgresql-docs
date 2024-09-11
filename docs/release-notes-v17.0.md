# Percona Distribution for PostgreSQL 17.0 ({{date.17_0}})

[Installation](installing.md){.md-button}
[Upgrade](major-upgrade.md){.md-button}
 

We are pleased to announce the launch of Percona Distribution for PostgreSQL 17.0 - a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on **Percona Server for PostgreSQL 17** - a binary compatible drop in replacement of [PostgreSQL 17 :octicons-link-external-16:](https://www.postgresql.org/docs/17/release-17.html). Percona Server for PostgreSQL 17 extends the Storage Manager API to hook in custom storage managers and introduce the encryption of indexes (experimental feature) as part of the Transparent Data Encryption (TDE) solution. 

Both Percona Server for PostgreSQL 17 and PostgreSQL Community 17 function identically enabling you to migrate from one to another. However, index-level encryption is available only with Percona Server for PostgreSQL. So if you encrypted indexes, you cannot switch to the upstream PostgreSQL without losing this data.

## Release Highlights

Percona Distribution for PostgreSQL 17 features a lot of new functionalities and enhancements to performance, replication, monitoring, developer experience and more. Among them are the following:




!!! admonition "See also"

    * [PostgreSQL 17 release notes :octicons-link-external-16:](https://www.postgresql.org/docs/17/release-17.html)


The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
|[HAProxy :octicons-link-external-16:](http://www.haproxy.org/) | 2.8.2 | a high-availability and load-balancing solution |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) | 3.1.0 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/)             | 16.0   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user)| 4.0.1 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/)           | 2.47    | a backup and restore solution for PostgreSQL       |
|[pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger)   | 12.2     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/)          |1.20.1    | a lightweight connection pooler for PostgreSQL|
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather)| v22     | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.4.4 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) | 1.4.8   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor :octicons-link-external-16:](https://github.com/percona/pg_stat_monitor)|2.0.2 | collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis) | 3.3.4 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common)| 253 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json)  |2.5       | a PostgreSQL logical decoding JSON output plugin|

Percona Distribution for PostgreSQL on Red Hat Enterprise Linux 8 and compatible derivatives also includes the following packages:

* `llvm` 17.0.6 packages. This fixes compatibility issues with LLVM from upstream.
* supplemental `python3-etcd` packages, which can be used for setting up Patroni clusters. 

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 