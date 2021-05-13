# Percona Distribution for PostgreSQL 11.10

<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">December 15, 2020</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/11/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table> 


Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL
installs PostgreSQL and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This release is based on [PostgreSQL 11.10](https://www.postgresql.org/docs/release/11.10/) and includes [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) (Tech Preview Feature ) - a new statistics collection extension for PostgreSQL.

The following is the list of extensions available in Percona Distribution for PostgreSQL.


| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.6   | rebuilds PostgreSQL database objects           |
| [Pgaudit](https://www.pgaudit.org/)             | 1.3.2   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgBackRest](https://pgbackrest.org/)           | 2.30    | a backup and restore solution for PostgreSQL       |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 2.0.1 | a HA (High Availability) solution for PostgreSQL |
| [PostgreSQL contrib extensions](https://www.postgresql.org/docs/11/contrib.html)                             | 11.10   | a collection of additional extensions for PostgreSQL |


Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/11/libpq.html) library. It contains “a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.” [^1]

This release of Percona Distribution for PostgreSQL is based on PostgreSQL 11.10.


[^1]: https://www.postgresql.org/docs/11/libpq.html
