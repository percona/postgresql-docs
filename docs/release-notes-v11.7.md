# Percona Distribution for PostgreSQL 11.7 (2020-04-09)


<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">April 9, 2020</td>
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
enable solving essential practical tasks efficiently:


* [Pg_repack](https://github.com/reorg/pg_repack) rebuilds PostgreSQL
database objects.


* [Pgaudit](https://www.pgaudit.org/) provides detailed session or object
audit logging via the standard logging facility provided by PostgreSQL


* [pgBackRest](https://pgbackrest.org/) - a backup and restore solution for
PostgreSQL


* [Patroni](https://patroni.readthedocs.io/en/latest/) - an HA (High Availability) solution for
PostgreSQL


* A collection of [additional PostgreSQL contrib extensions](https://www.postgresql.org/docs/11/contrib.html)

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/11/libpq.html) library. It contains “a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries.” [^1]

This release of Percona Distribution for PostgreSQL is based on PostgreSQL 11.7.

Starting from May 15, 2020, this release of Percona Distribution for PostgreSQL includes
improvements to simplify the upgrade to the major version of Percona Distribution for PostgreSQL.

[^1]: https://www.postgresql.org/docs/11/libpq.html
