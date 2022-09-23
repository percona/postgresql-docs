# Percona Distribution for PostgreSQL 15.0 (2022-10-24)

| Release date:     |  October 24, 2022      |
|:------------------|:-----------------------|
| **Installation**: | [Installing Percona Distribution for PostgreSQL](installing.md) |
| **Upgrade**       | [Upgrading Percona Distribution for PostgreSQL from 14 to 15](major-upgrade.md)
 


We are pleased to announce the launch of Percona Distribution for PostgreSQL 15.0 - a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL installs PostgreSQL and complements it by a selection of extensions that are tested to work together and aim to simplify deployment and management of your PostgreSQL environment.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 15](https://www.postgresql.org/docs/15/release-15.html). 

## Release Highlights

Percona Distribution for PostgreSQL 15 features a lot of new functionalities and enhancements to performance, replication, statistics collection, logging and more. Among them are the following:

* Added the [`MERGE`](https://www.postgresql.org/docs/15/sql-merge.html) command, which allows your developers to write conditional SQL statements that can include `INSERT`, `UPDATE`, and `DELETE` actions within a single statement.
* A [view can now be created with the permissions of the caller](https://www.postgresql.org/docs/15/sql-createview.html), instead of the view creator. This adds an additional layer of protection to ensure that view callers have the correct permissions for working with the underlying data.
* Enhanced logical replication management:

    - Row filtering and column lists for publishers lets users choose to replicate a subset of data from a table
    - The ability to skip replaying a conflicting transaction and to automatically disable a subscription if an error is detected simplifies the conflict management. 
    - The ability to use two-phase commit (2PC) with logical replication.

* A new logging format [`jsonlog`](https://www.postgresql.org/docs/15/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-JSONLOG) outputs log data using a defined JSON structure, which allows PostgreSQL logs to be processed in structured logging systems
* Now DBAs can manage the PostgreSQL configuration by granting users permission to alter server-level configuration parameters. Users can also browse the configuration from `psql` using the  `\dconfig` command. 
- [Server-level statistics](https://www.postgresql.org/docs/15/monitoring-stats.html) are now collected in shared memory, eliminating both the statistics collector process and periodically writing this data to disk
- A new built-in extension, [`pg_walinspect`](https://www.postgresql.org/docs/15/pgwalinspect.html), lets users inspect the contents of write-ahead log files directly from a SQL interface.
* Performance optimizations: 

    - Improved performance of window functions such as `rank()`, `row_number()` and `count()`. Read more about performance and benchmarking results in [Introducing Performance Improvement of Window Functions in PostgreSQL 15](https://www.percona.com/blog/introducing-performance-improvement-of-window-functions-in-postgresql-15/).
    - [Parallel execution](https://www.postgresql.org/docs/15/parallel-query.html) of queries using the [`SELECT DISTINCT`](https://www.postgresql.org/docs/15/queries-select-lists.html#QUERIES-DISTINCT) command.
    - The support for LZ4 and zstd compression methods to write-ahead logs (WAL) and backup files improves performance and storage capabilities of your database.



!!! admonition "See also"

    * [PostgreSQL 15 release notes](https://www.postgresql.org/docs/15/release-15.html)
    * Percona Blog: 

        * [A Quick Peek at the PostgreSQL 15 Beta 1](https://www.percona.com/blog/a-quick-peek-at-the-postgresql-15-beta-1/)
        * [PostgreSQL 15 – New Features to Be Excited About](https://www.percona.com/blog/postgresql-15-new-features-to-be-excited-about/)
        * [PostgreSQL 15: Stats Collector Gone? What’s New?](https://www.percona.com/blog/postgresql-15-stats-collector-gone-whats-new/)


The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 2.1.4 | a HA (High Availability) solution for PostgreSQL |
| [pgaudit](https://www.pgaudit.org/)             | 1.7.0 | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
|[`pgAudit set user`](https://github.com/pgaudit/set_user)| 3.0.0|  provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.41    | a backup and restore solution for PostgreSQL       |
|[`pgBadger`](https://github.com/darold/pgbadger) | 12.0       | a fast PostgreSQL Log Analyzer.|
|[`pgBouncer`](https://www.pgbouncer.org/) | 1.17.0 | lightweight connection pooler for PostgreSQL|
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.8   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)| 1.1.1 | collects and aggregates statistics for PostgreSQL and provides histogram information.       |
| [PostgreSQL Common](https://packages.debian.org/sid/percona-postgresql-common)| 241 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[`wal2json`](https://github.com/eulerto/wal2json) |2.5        | a PostgreSQL logical decoding JSON output plugin.|
|[HAProxy](http://www.haproxy.org/) | 2.5.9 | The high-availability and load balancing solution for PostgreSQL|

Percona Distribution for PostgreSQL also includes the following packages:

* `llvm` 12.0.1 packages for Red Hat Enterprise Linux 8 / CentOS 8. This fixes compatibility issues with LLVM from upstream.
* supplemental `ETCD` packages which can be used for setting up Patroni clusters. These packages are available for the following operating systems:

|  Operating System   | Package              | Version | Description        |
| ------------------- | ---------------------| --------| ------------------ |
| CentOS 8            | `etcd`               | 3.3.11  | A consistent, distributed key-value store|
|                     | `python3-python-etcd`| 0.4.3   | A Python client for ETCD     |


                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/15/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
