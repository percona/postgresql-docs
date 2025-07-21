# Percona Distribution for PostgreSQL 13.5 Update (2021-02-12)

<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">December 2, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/13/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table> 

Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL installs PostgreSQL and complements it by a selection of extensions that enable solving essential practical tasks efficiently.

This update of Percona Distribution for PostgreSQL fixes the inability of a user to upgrade the `postgresql-common` package during the major upgrade to version 13.5 on DEB-based systems. 

## Bugs Fixed

* [DISTPG-358](https://jira.percona.com/browse/DISTPG-358): "Device or resource busy" error during the major upgrade of PostgreSQL on Ubuntu