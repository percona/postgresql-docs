.. _DISTPG-12.4:

================================================================================
*Percona Distribution for PostgreSQL* 12.4
================================================================================

:Date: September 11, 2020
:Installation: `Installing Percona Distribution for PostgreSQL <https://www.percona.com/doc/postgresql/12/installing.html>`_

|pdp| is a collection of tools to assist you in managing |postgresql|. |pdp|
installs |postgresql| and complements it by a selection of extensions that
enable solving essential practical tasks efficiently:

.. list-table::
   :widths: 35 15 50
   :header-rows: 1

   * - Extension
     - Version
     - Description
   * - `Pg_repack <https://github.com/reorg/pg_repack>`_ 
     - 1.4.5
     - rebuilds |postgresql| database objects
   * - `Pgaudit <https://www.pgaudit.org/>`_ 
     - 1.4.0
     - provides detailed session or object audit logging via the standard 
       logging facility provided by |postgresql|
   * - `pgBackRest <https://pgbackrest.org/>`_ 
     - 2.29
     - a backup and restore solution for |postgresql|
   * - `Patroni <https://patroni.readthedocs.io/en/latest/>`_
     - 2.0.0
     - a :abbr:`HA (High Availability)` solution for |postgresql|
   * - `PostgreSQL contrib extensions
       <https://www.postgresql.org/docs/11/contrib.html>`_
     - 12.4
     - a collection of additional extensions for PostgreSQL

|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/12/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_

This release of |pdp| is based on |postgresql| |version|.

.. |version| replace:: 12.4

.. [#] https://www.postgresql.org/docs/12/libpq.html

.. include:: .res/replace.txt
