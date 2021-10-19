# Percona Distribution for PostgreSQL 13.4 Second Update

<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">October 21, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/13/installing.html">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table> 


Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL
installs PostgreSQL and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This update of Percona Distribution for PostgreSQL includes the new version of `pg_stat_monitor <version>` - the Query Performance Monitoring Tool for PostgreSQL.

Also, previous version packages of PostgreSQL from PGDG (PostgreSQL Global Development Group) now remain in a user’s environment during the major upgrade to Percona Distribution for PostgreSQL. 

## Bugs Fixed

* [DISTPG-317](https://jira.percona.com/browse/DISTPG-317): PostgreSQL 13 installation removes PostgreSQL 12 (PGDG) installation