# Percona Distribution for PostgreSQL 12.7


<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">May 24, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/12/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table>


Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL
installs PostgreSQL and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 12.7](https://www.postgresql.org/docs/release/12.7/).

The following is the list of extensions available in Percona Distribution for PostgreSQL.


| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.6   | rebuilds PostgreSQL database objects           |
| [pgAudit](https://www.pgaudit.org/)             | 1.4.1   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
|[pgAudit set_user](https://github.com/pgaudit/set_user)|2.0.0| provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.33    | a backup and restore solution for PostgreSQL       |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 2.0.2 | a HA (High Availability) solution for PostgreSQL |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) (Tech Preview Feature)                                           | 0.9.1   | collects and aggregates statistics for PostgreSQL and provides histogram information. |
| [PgBouncer](https://www.pgbouncer.org/)          | 1.15.0  | a lightweight connection pooler for PostgreSQL      |
|[pgBadger](https://github.com/darold/pgbadger)    | 11.5    | a fast PostgreSQL Log Analyzer               |
|[wal2json](https://github.com/eulerto/wal2json)   | 2.3     | a PostgreSQL logical decoding JSON output plugin.  |
| [PostgreSQL contrib extensions](https://www.postgresql.org/docs/12/contrib.html)                             | 12.7   | a collection of additional extensions for PostgreSQL |
 

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/12/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries."
