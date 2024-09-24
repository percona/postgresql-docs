# Percona Distribution for PostgreSQL 17.0-1 ({{date.17_0}})

[Installation](installing.md){.md-button}
[Upgrade](major-upgrade.md){.md-button}
 

We are pleased to announce the launch of Percona Distribution for PostgreSQL 17.0 - a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on **Percona Server for PostgreSQL 17** - a binary compatible drop in replacement of [PostgreSQL 17 :octicons-link-external-16:](https://www.postgresql.org/docs/17/release-17.html). Percona Server for PostgreSQL 17 extends the Storage Manager API to hook in custom storage managers and introduce the encryption of indexes (experimental feature) as part of the Transparent Data Encryption (TDE) solution. 

Both Percona Server for PostgreSQL 17 and PostgreSQL Community 17 function identically enabling you to migrate from one to another. However, index-level encryption is available only with Percona Server for PostgreSQL. So if you encrypted indexes and wish to migrate to the upstream PostgreSQL, you must first migrate data to the unencrypted table and then proceed with the migration. 

## Release Highlights

### Percona Server for PostgreSQL improvements

* Exposed Storage Manager API to enable PostgreSQL extensions to hook in custom storage managers.
* Extended Write-Ahead Log (WAL) API to hook into WAL read and write functions.

### PostgreSQL Community improvements

PostgreSQL Community 17 features a lot of new functionalities and enhancements to performance, replication, monitoring, developer experience and more. Among them are the following:

#### Incremental base backups

Save time and storage space with the ability to back up only the changes since the last backup using [`pg_basebackup`](https://www.postgresql.org/docs/17/continuous-archiving.html#BACKUP-INCREMENTAL-BACKUP) with the `--incremental` option. The new [`pg_combinebackup`](https://www.postgresql.org/docs/17/app-pgcombinebackup.html) tool allows manipulation of base and incremental file system backups for recovery.

Note that you still require a full backup to derive the increments from and to be used during recovery.

This feature is especially beneficial for organizations with large data sets where a full backup is a time-consuming and resource-intensive operation.  

#### Performance improvements

* Vacuum Process Enhancements: The VACUUM process, responsible for reclaiming storage, now has a new internal data structure, reducing memory usage by up to 20x and improving overall performance.
* The new stream I/O interface can enhance performance during sequential scans and when running the `ANALYZE` command.
* Added support for parallel index builds for `BRIN` indexes, which can significantly speed up index creation. Additionally, this release significantly improves execution time of queries that use the `IN` clause with a B-tree index.

#### Developer experience

* Developers can now transform JSON objects into a standard database table and convert JSON values to different data types directly within SQL statements. This adds flexibility when working with multiple data formats.
* Run bulk upload and export data from PostgreSQL up to 2x faster with improved `COPY` performance. In addition, use the `ON_ERROR` option to proceed with the copy  operation even if there is an error inserting a row.
* The RETURN clause added to the MERGE command enables developers to retrieve and return the rows modified by the MERGE operation in a single step, reducing the need for additional queries and simplifying complex workflows.

#### Replication improvements

* Gain more control for managing PostgreSQL databases in high availability environments with the ability to continue logical replication from a new primary node after the failover. 
* Track inactive and invalid replication slots in the `pg_replication_slots` view. With the  `inactive_since` and `invalidation_reason` columns  added to this view, you can get insights when a slot became inactive as well as the reason for an invalid slot.

#### Security improvements

* Enable users to perform maintenance operations such as ANALYZE, VACUUM, REINDEX, CLUSTER, REFRESH MATERIALIZED VIEW, and LOCK TABLE on all relations by assigning the new predefined `pg_maintain` role to them. In addition, the `search_path` is safe for maintenance operations like VACUUM, ANALYZE, CLUSTER, REFRESH MATERIALIZED VIEW and INDEX.

#### Monitoring improvements

* Get deeper insights about query plans and execution with the new options for the EXPLAIN command: 

   * SERIALIZE shows the amount of time it takes to convert data for network transmission
   * MEMORY reports optimizer memory usage 

* Learn about why an active session is waiting using the `pg_stat_activity` and new `pg_wait_events` views

!!! admonition "See also"

    * [PostgreSQL 17 release notes :octicons-link-external-16:](https://www.postgresql.org/docs/17/release-17.html)
    * Percona Blog: [The Powerful Features Released in PostgreSQL 17 Beta 2](https://www.percona.com/blog/the-powerful-features-released-in-postgresql-17-beta-2/)

### Join Percona Squad

Participate in monthly SWAG raffles, get an early access to new product features and invite-only “ask me anything” sessions with database performance experts. Interested? [Fill in the form](squad.percona.com/mongodb)
---------------------------------------------------------------------------------------------------


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