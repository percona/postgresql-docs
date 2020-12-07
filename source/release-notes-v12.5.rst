.. _DISTPG-12.5:

================================================================================
*Percona Distribution for PostgreSQL* 12.5
================================================================================

:Date: December 7, 2020
:Installation: `Installing Percona Distribution for PostgreSQL <https://www.percona.com/doc/postgresql/12/installing.html>`_

|pdp| is a collection of tools to assist you in managing |postgresql|. |pdp|
installs |postgresql| and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This release of |pdp| is based on `PostgreSQL 12.5 <https://www.postgresql.org/docs/release/12.5/>`_.

The following is the list of extensions available in |pdp|.

.. list-table::
  :widths: 35 15 50
  :header-rows: 1

  * - Extension
    - Version
    - Description
  * - `pg_repack <https://github.com/reorg/pg_repack>`_ 
    - 1.4.6
    - rebuilds |postgresql| database objects
  * - `Pgaudit <https://www.pgaudit.org/>`_ 
    - 1.4.1
    - provides detailed session or object audit logging via the standard 
      logging facility provided by |postgresql|
  * - `pgBackRest <https://pgbackrest.org/>`_ 
    - 2.30
    - a backup and restore solution for |postgresql|
  * - `Patroni <https://patroni.readthedocs.io/en/latest/>`_
    - 2.0.1
    - a :abbr:`HA (High Availability)` solution for |postgresql|
  * - `pg_stat_monitor <https://github.com/percona/pg_stat_monitor>`_ (Tech Preview Feature [#]_)
    - 0.6.0
    - collects and aggregates statistics for |postgresql| and provides histogram information.
  * - `PostgreSQL contrib extensions <https://www.postgresql.org/docs/13/contrib.html>`_
    - 12.5
    - a collection of additional extensions for PostgreSQL

|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/12/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_

.. [#] Tech Preview Features are not yet ready for enterprise use and are not included in support via |SLA|. They are included in this release so that users can provide feedback prior to the full release of the feature in a future |GA| release (or removal of the feature if it is deemed not useful). This functionality can change (APIs, CLIs, etc.) from tech preview to GA.
.. [#] https://www.postgresql.org/docs/12/libpq.html

.. include:: .res/replace.txt

