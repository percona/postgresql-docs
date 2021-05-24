.. _DISTPG-11.12:

================================================================================
*Percona Distribution for PostgreSQL* 11.12
================================================================================

:Date: May 24, 2021
:Installation: `Installing Percona Distribution for PostgreSQL <https://www.percona.com/doc/postgresql/11/installing.html>`_


|pdp| is a collection of tools to assist you in managing |postgresql|. |pdp|
installs |postgresql| and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This release is based on `PostgreSQL 11.12 <https://www.postgresql.org/docs/release/11.12/>`_ and includes the extended set of extensions supplied with |pdp|.

.. list-table::
  :widths: 35 15 50
  :header-rows: 1

  * - Extension
    - Version
    - Description
  * - `pg_repack <https://github.com/reorg/pg_repack>`_ 
    - 1.4.6
    - rebuilds |postgresql| database objects
  * - `pgAudit <https://www.pgaudit.org/>`_ 
    - 1.3.2
    - provides detailed session or object audit logging via the standard 
      logging facility provided by |postgresql|
  * - `pgAudit set_user <https://github.com/pgaudit/set_user>`_ 
    - 2.0.0
    - provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.
  * - `pgBackRest <https://pgbackrest.org/>`_ 
    - 2.33
    - a backup and restore solution for |postgresql|
  * - `Patroni <https://patroni.readthedocs.io/en/latest/>`_
    - 2.0.2
    - a :abbr:`HA (High Availability)` solution for |postgresql|
  * - `pg_stat_monitor <https://github.com/percona/pg_stat_monitor>`_ (Tech Preview Feature [#]_)
    - 0.9.1
    - collects and aggregates statistics for |postgresql| and provides histogram information.
  * - `pgBadger <https://github.com/darold/pgbadger>`_ 
    - 11.5
    - a fast PostgreSQL Log Analyzer. 
  * - `PgBouncer <https://www.pgbouncer.org/>`_ 
    - 1.15.0
    - a lightweight connection pooler for PostgreSQL
  * - `wal2json <https://github.com/eulerto/wal2json>`_
    - 2.3
    - a PostgreSQL logical decoding JSON output plugin.
  * - `PostgreSQL contrib extensions <https://www.postgresql.org/docs/11/contrib.html>`_
    - 11.12
    - a collection of additional extensions for PostgreSQL


|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/11/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_


.. [#] Tech Preview Features are not yet ready for enterprise use and are not included in support via |SLA|. They are included in this release, so that users can provide feedback prior to the full release of the feature in a future |GA| release (or removal of the feature if it is deemed not useful). This functionality can change (APIs, CLIs, etc.) from tech preview to GA.
.. [#] https://www.postgresql.org/docs/11/libpq.html


.. include:: .res/replace.txt

