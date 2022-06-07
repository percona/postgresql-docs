# Percona Distribution for PostgreSQL 11.11 (2021-03-08)

<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">March 8, 2021</td>
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

The following is the list of extensions available in Percona Distribution for PostgreSQL.


| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.6   | rebuilds PostgreSQL database objects           |
| [Pgaudit](https://www.pgaudit.org/)             | 1.3.2   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgBackRest](https://pgbackrest.org/)           | 2.32    | a backup and restore solution for PostgreSQL       |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 2.0.1 | a HA (High Availability) solution for PostgreSQL |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) (Tech Preview Feature [^1])|                                         |0.6.0 |collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostgreSQL contrib extensions](https://www.postgresql.org/docs/11/contrib.html)                             | 11.11   | a collection of additional extensions for PostgreSQL |
 
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/11/libpq.html) library. It contains “a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.” [^2]

This release is based on [PostgreSQL 11.11](https://www.postgresql.org/docs/release/11.11/).


[^1]: Tech Preview Features are not yet ready for enterprise use and are not included in support via SLA. They are included in this release, so that users can provide feedback prior to the full release of the feature in a future GA release (or removal of the feature if it is deemed not useful). This functionality can change (APIs, CLIs, etc.) from tech preview to GA.

[^2]: https://www.postgresql.org/docs/11/libpq.html
