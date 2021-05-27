# Percona Distribution for PostgreSQL 11.12 


<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">March 24, 2021</td>
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


This release is based on [PostgreSQL
11.12](https://www.postgresql.org/docs/release/11.12/) and includes the
extended set of extensions supplied with Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [pg_repack](https://github.com/reorg/pg_repack) | 1.4.6   | rebuilds PostgreSQL database objects           |
| [PgAudit](https://www.pgaudit.org/)             | 1.3.2   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 2.0.0|provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.33    | a backup and restore solution for PostgreSQL       |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 2.0.2 | a HA (High Availability) solution for PostgreSQL |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) (Tech Preview Feature [^1])|                                         |0.9.1 |collects and aggregates statistics for PostgreSQL and provides histogram information.|
|[pgBadger](https://github.com/darold/pgbadger)   | 11.5     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer](https://www.pgbouncer.org/)          |1.15.0    | a lightweight connection pooler for PostgreSQL|
|[wal2json](https://github.com/eulerto/wal2json)  |2.3       | a PostgreSQL logical decoding JSON output plugin|
| [PostgreSQL contrib extensions](https://www.postgresql.org/docs/11/contrib.html)                             | 11.11   | a collection of additional extensions for PostgreSQL |

Percona Distribution for PostgreSQL is also shipped with the
[libpq](https://www.postgresql.org/docs/11/libpq.html) library. It
contains "a set of library functions that allow client programs to pass
queries to the PostgreSQL backend server and to receive the results of
these queries."[^2]

[^1]: Tech Preview Features are not yet ready for enterprise use and are
    not included in support via . They are included in this release, so
    that users can provide feedback prior to the full release of the
    feature in a future release (or removal of the feature if it is
    deemed not useful). This functionality can change (APIs, CLIs, etc.)
    from tech preview to GA.

[^2]: <https://www.postgresql.org/docs/11/libpq.html>
