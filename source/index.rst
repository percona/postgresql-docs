.. _pdp.index:


|pdp| |version| Documentation
********************************************************************************

|pdp| is a collection of tools to assist you in managing your |postgresql|
database system: it installs |postgres| and complements it by a selection of
extensions that enable solving essential practical tasks efficiently:

- `pg_repack <https://github.com/reorg/pg_repack>`_ rebuilds
  |postgresql| database objects.
- `pgAudit <https://www.pgaudit.org/>`_ provides detailed session or object
  audit logging via the standard |postgresql| logging facility.
- `pgAudit set_user <https://github.com/pgaudit/set_user>`_ - The ``set_user`` part of ``pgAudit`` extension provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.
- `pgBackRest <https://pgbackrest.org/>`_ is a backup and restore solution for
  |postgresql|.
- `Patroni <https://patroni.readthedocs.io/en/latest/>`_ is an :abbr:`HA (High
  Availability)` solution for |postgresql|.
- `pg_stat_monitor <https://github.com/percona/pg_stat_monitor>`_ (Tech Preview Feature [#]_) collects and aggregates statistics for |postgresql| and provides histogram information.
- `PgBouncer <https://www.pgbouncer.org/>`_ - a lightweight connection pooler for PostgreSQL
- `pgBadger <https://github.com/darold/pgbadger>`_ - a fast PostgreSQL Log Analyzer.
- `wal2json <https://github.com/eulerto/wal2json>`_ - a PostgreSQL logical decoding JSON output plugin.
- A collection of `additional PostgreSQL contrib extensions
  <https://www.postgresql.org/docs/13/contrib.html>`_

.. seealso::

   |percona| Blog Posts
      - `pgBackRest - A Great Backup Solution and a Wonderful Year of Growth
        <https://www.percona.com/blog/2019/05/10/pgbackrest-a-great-backup-solution-and-a-wonderful-year-of-growth/>`_
      - `Securing PostgreSQL as an Enterprise-Grade Environment
        <https://www.percona.com/blog/2018/09/21/securing-postgresql-as-an-enterprise-grade-environment/>`_
      - `Announcing pg_stat_monitor Tech Preview: Get Better Insights Into Query Performance in PostgreSQL <https://www.percona.com/blog/2020/10/14/announcing-pg_stat_monitor-tech-preview-get-better-insights-into-query-performance-in-postgresql/>`_
	
|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/13/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_

Installation and Upgrade
*****************************************

.. toctree::
   :maxdepth: 2
   :glob:

   installing
   major-upgrade
   minor-upgrade
   
Extensions
******************************************

.. toctree::
   :maxdepth: 1
   
   pg-stat-monitor

Uninstall |pdp|
******************************************

.. toctree::
   :maxdepth: 2

   uninstalling

Release Notes
******************************************

.. toctree::
   :maxdepth: 2
   :glob:

   release-notes

Reference
********************

.. toctree::
   :maxdepth: 1

   licensing

.. [#] Tech Preview Features are not yet ready for enterprise use and are not included in support via |SLA|. They are included in this release so that users can provide feedback prior to the full release of the feature in a future |GA| release (or removal of the feature if it is deemed not useful). This functionality can change (APIs, CLIs, etc.) from tech preview to GA.
.. [#] https://www.postgresql.org/docs/13/libpq.html

		       
.. include:: .res/replace.txt
