.. _DISTPG-11.10:

================================================================================
*Percona Distribution for PostgreSQL* 11.10
================================================================================

:Date: December 15, 2020
:Installation: `Installing Percona Distribution for PostgreSQL <https://www.percona.com/doc/postgresql/11/installing.html>`_

|pdp| is a collection of tools to assist you in managing |postgresql|. |pdp|
installs |postgresql| and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This release is based on `PostgreSQL 11.10 <https://www.postgresql.org/docs/release/11.10/>`_ and includes `pg_stat_monitor <https://github.com/percona/pg_stat_monitor>`_ (Tech Preview Feature [#]_) - a new statistics collection extension for PostgreSQL. 

The following is the list of extensions available in |pdp|.

.. list-table::
   :widths: 35 15 50
   :header-rows: 1

   * - Extension
     - Version
     - Description
   * - `Pg_repack <https://github.com/reorg/pg_repack>`_ 
     - 1.4.6
     - rebuilds |postgresql| database objects
   * - `Pgaudit <https://www.pgaudit.org/>`_ 
     - 1.3.2
     - provides detailed session or object audit logging via the standard 
       logging facility provided by |postgresql|
   * - `pgBackRest <https://pgbackrest.org/>`_ 
     - 2.30
     - a backup and restore solution for |postgresql|
   * - `Patroni <https://patroni.readthedocs.io/en/latest/>`_
     - 2.0.1
     - a :abbr:`HA (High Availability)` solution for |postgresql|
   * - `pg_stat_monitor <https://github.com/percona/pg_stat_monitor>`_ (Tech Preview Feature)
     - 0.6.0
     - collects and aggregates statistics for PostgreSQL and provides histogram information.
   * - `PostgreSQL contrib extensions
       <https://www.postgresql.org/docs/11/contrib.html>`_
     - 11.10
     - a collection of additional extensions for PostgreSQL

|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/11/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_

This release of |pdp| is based on |postgresql| |version|.

.. [#] Tech Preview Features are not yet ready for enterprise use and are not included in support via |SLA|. They are included in this release so that users can provide feedback prior to the full release of the feature in a future |GA| release (or removal of the feature if it is deemed not useful). This functionality can change (APIs, CLIs, etc.) from tech preview to GA.
.. [#] https://www.postgresql.org/docs/11/libpq.html

.. |version| replace:: 11.10

.. include:: .res/replace.txt

