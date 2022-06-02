# Percona Distribution for PostgreSQL 13.4 Update (2021-09-30)

<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">September 30, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/13/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table> 


Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL
installs PostgreSQL and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This update of Percona Distribution for PostgreSQL fixes the inability of a user to upgrade from previous version of PostgreSQL from PGDG (PostgreSQL Global Development Group) to Percona Distribution for PostgreSQL on Ubuntu 

## Bugs Fixed

* [DISTPG-297](https://jira.percona.com/browse/DISTPG-297): Unable to install Percona PostgreSQL packages on Ubuntu where older version from PGDG is present