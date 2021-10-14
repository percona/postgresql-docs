# Percona Distribution for PostgreSQL 14.0

<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">November 10, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/14/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
    <tr class="field-odd field">
      <th class="field-name">Upgrade:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/14/major-upgrade.html#">Upgrading Percona Distribution for PostgreSQL from 13 to 14</a></td>
    </tr>
  </tbody>
</table> 


We are pleased to announce the launch of Percona Distribution for PostgreSQL 14.0 -  a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL
installs PostgreSQL and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 14](https://www.postgresql.org/docs/release/14/).

## Release Highlights

PostgreSQL 14 provides an extensive set of new features and enhancements to security, performance, usability for client applications and more. 

Most notable of them include the following:

* Expired B-tree index entries can now be detected and removed between vacuum runs. This results in lesser number of page splits and reduces the index bloat. 
* The vacuum process now deletes B-tree pages in a single cycle, without marking them as deleted during the first run. This speeds up free space cleanup.
* Support for subscripts in JSON is added to simplify data retrieval using a commonly recognized syntax. 
* Stored procedures can accept OUT parameters.
* The [libpq](https://www.postgresql.org/docs/14/libpq.html) library now supports the pipeline mode. Previously, the client applications waited for a transaction to be completed before sending the next one. The pipeline mode allows the applications to send multiple transactions at the same time thus boosting performance.
* Large transactions are now streamed to subscribers in-progress, thus increasing the performance. This improvement applies to logical replication API as well.
* LZ4 compression is added for [TOAST](https://www.postgresql.org/docs/current/storage-toast.html) operations. This speeds up large data processing.
* SCRAM is made the default authentication mechanism. This mechanism improves security and simplifies regulatory compliance for data security.

!!! seealso

    * [PostgreSQL 14 release notes](https://www.postgresql.org/docs/release/14/)
    * Percona Blog: [PostgreSQL 14 – Performance, Security, Usability, and Observability](https://www.percona.com/blog/postgresql-14-performance-security-usability-and-observability/)
    * [Using the Range and the New Multirange Data Type in PostgreSQL 14](https://www.percona.com/blog/using-the-multirange-data-type-in-postgresql-14/)
    * [Using New JSON Syntax in PostgreSQL 14 – Update](https://www.percona.com/blog/using-new-json-syntax-in-postgresql-14-update/)

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 2.1.0 | a HA (High Availability) solution for PostgreSQL |
| [Pgaudit](https://www.pgaudit.org/)             | 1.6.0 | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
|[`pgAudit set user`](https://github.com/pgaudit/set_user)| 3.0.0|  provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.36    | a backup and restore solution for PostgreSQL       |
|[`pgBadger`](https://github.com/darold/pgbadger) | 11.5       | a fast PostgreSQL Log Analyzer.|
|[`pgBouncer`](https://www.pgbouncer.org/) | 1.16.0 | lightweight connection pooler for PostgreSQL|
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.7   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)| 1.0.0 - Beta2 | collects and aggregates statistics for PostgreSQL and provides histogram information.       |
| [PostgreSQL Common](https://packages.debian.org/sid/percona-postgresql-common)| 226 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[`wal2json`](https://github.com/eulerto/wal2json) |2.3        | a PostgreSQL logical decoding JSON output plugin.|

Percona Distribution for PostgreSQL also includes the following packages:

* `llvm` 11.0.0 packages for Red Hat Enterprise Linux 8 / CentOS 8. This fixes compatibility issues with LLVM from upstream.
* supplemental `ETCD` packages which can be used for setting up Patroni clusters. These packages are available for the following operating systems:

|  Operating System   | Package              | Version | Description        |
| ------------------- | ---------------------| --------| ------------------ |
| CentOS 7            |`python3-python-etcd` | 0.4.3   | A Python client for ETCD     |
| CentOS 8            | `etcd`               | 3.3.11  | A consistent, distributed key-value store|
|                     | `python3-python-etcd`| 0.4.3   | A Python client for ETCD     |
| Debian 9 ('stretch')| `etcd`               | 3.3.11  | A consistent, distributed key-value store|
|                     | `python3-etcd`       | 0.4.5   | A Python client for ETCD     |

                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/14/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
