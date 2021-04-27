.. _DISTPG-12.6-upd2:

================================================================================
*Percona Distribution for PostgreSQL* 12.6 Second Update
================================================================================

:Date: April 27, 2021
:Installation: `Installing Percona Distribution for PostgreSQL <https://www.percona.com/doc/postgresql/13/installing.html>`_

This update of |pdp| includes the set of new extensions which are now supplied with |pdp|:

- `PgBouncer <https://www.pgbouncer.org/>`_ 1.15.0 - lightweight connection pooler for PostgreSQL
- `pgAudit set_user <https://github.com/pgaudit/set_user>`_ 2.0.0 - The PostgreSQL Audit extension (``pgaudit``) provides detailed session and/or object audit logging via the standard PostgreSQL logging facility. The ``set_user`` part of that extension provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.
- `pgBadger <https://github.com/darold/pgbadger>`_ 11.5 - a fast PostgreSQL Log Analyzer.
- `wal2json <https://github.com/eulerto/wal2json>`_ 2.3 - a PostgreSQL logical decoding JSON output plugin.

This update of |pdp| also includes the updated version of `Patroni <https://patroni.readthedocs.io/en/latest/>`_ 2.0.2 - a :abbr:`HA (High Availability)` solution for |postgresql|.


.. include:: .res/replace.txt

