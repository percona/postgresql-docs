# Percona Distribution for PostgreSQL 16.0 (2023-09-19)

[Installation](installing.md){.md-button}
[Upgrade](major-upgrade.md){.md-button}
 

We are pleased to announce the launch of Percona Distribution for PostgreSQL 16.0 - a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 16](https://www.postgresql.org/docs/16/release-16.html). 

## Release Highlights

Percona Distribution for PostgreSQL 16 features a lot of new functionalities and enhancements to performance, replication, monitoring, developer experience and more. Among them are the following:

* Performance improvements:

    * The support for CPU acceleration using SIMD (Single Instruction/Multiple Data) computing method for both x86 and ARM architectures 
    * Optimized processing of ASCII and JSON strings and array and subtransaction searches improve query processing performance.
    * The support of concurrent bulk data loading using `COPY` boost performance up to 300%.
    * Load balancing for `libpq` client simplifies scaling read queries.
    * The use of lz4 and zstd compression methods for `pg_dump` results in better compression performance compared to the default gzip compression method.

* Logical replication improvements include the ability to apply large transactions in parallel and the ability to perform logical decoding on standbys. This enables users to distribute their workloads among nodes. 
* Developer experience:

    * The standard for manipulating JSON data now includes the SQL/JSON constructors and the `ANY_VALUE` aggregate function, which returns any arbitrary value from the aggregate set. 
    * Developers can now specify non-decimal integers such as 0xff and 0o777.
    * Added support for the extended query protocol to the  `psql` client.


* Privilege administration improvements:

    * Logical replication subscribers now execute transactions on a table as the table owner, not the superuser.
    * Now only the users that have the ADMIN OPTION for roles can grant privileges in these roles using the `CREATEROLE` function. This allows fine-tuning privileges definition.
    * New predefined role `pg_maintain` enables non-superusers to run VACUUM, ANALYZE, CLUSTER, REFRESH MATERIALIZED VIEW, REINDEX, and LOCK TABLE on all tables.

* Database administrators can now view insights on I/O statistics in a separate `pg_stat_io` view provides. 


!!! admonition "See also"

    * [PostgreSQL 16 release notes](https://www.postgresql.org/docs/16/release-16.html)


The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
|[HAProxy](http://www.haproxy.org/) | 2.8.2 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 3.1.0 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/)             | 16.0   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 4.0.1 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.47    | a backup and restore solution for PostgreSQL       |
|[pgBadger](https://github.com/darold/pgbadger)   | 12.2     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer](https://www.pgbouncer.org/)          |1.20.1    | a lightweight connection pooler for PostgreSQL|
| [pg_gather](https://github.com/jobinau/pg_gather)| v22     | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.4.4 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.8   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)|2.0.2 | collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostGIS](https://github.com/postgis/postgis) | 3.3.4 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common)| 253 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[wal2json](https://github.com/eulerto/wal2json)  |2.5       | a PostgreSQL logical decoding JSON output plugin|

Percona Distribution for PostgreSQL also includes the following packages:

* `llvm` 12.0.1 packages for Red Hat Enterprise Linux 8 / CentOS 8. This fixes compatibility issues with LLVM from upstream.
* supplemental `ETCD` packages which can be used for setting up Patroni clusters. These packages are available for the following operating systems:

|  Operating System   | Package              | Version | Description        |
| ------------------- | ---------------------| --------| ------------------ |
| CentOS 8            | `etcd`               | 3.3.11  | A consistent, distributed key-value store|
|                     | `python3-python-etcd`| 0.4.5   | A Python client for ETCD     |


                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/16/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
