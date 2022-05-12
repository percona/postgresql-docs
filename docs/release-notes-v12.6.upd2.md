# Percona Distribution for PostgreSQL 12.6 Second Update (2021-04-27)


<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">April 27, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/12/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table>


This update of Percona Distribution for PostgreSQL includes the set of new extensions which are now supplied with Percona Distribution for PostgreSQL:


* [PgBouncer](https://www.pgbouncer.org/) 1.15.0 - lightweight connection pooler for PostgreSQL


* [pgAudit set_user](https://github.com/pgaudit/set_user) 2.0.0 - The PostgreSQL Audit extension (`pgaudit`) provides detailed session and/or object audit logging via the standard PostgreSQL logging facility. The `set_user` part of that extension provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.


* [pgBadger](https://github.com/darold/pgbadger) 11.5 - a fast PostgreSQL Log Analyzer.


* [wal2json](https://github.com/eulerto/wal2json) 2.3 - a PostgreSQL logical decoding JSON output plugin.

This update of Percona Distribution for PostgreSQL also includes the updated version of [Patroni](https://patroni.readthedocs.io/en/latest/) 2.0.2 - a HA (High Availability) solution for PostgreSQL.
