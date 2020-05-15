.. _DISTPG-12.2:

================================================================================
*Percona Distribution for PostgreSQL* 12.2
================================================================================

:Date: May 15, 2020
:Installation: :ref:`pdp.installing`
	       
|pdp| is a collection of tools to assist you in managing |postgresql|. |pdp|
installs |postgresql| and complements it by a selection of extensions that
enable solving essential practical tasks efficiently:

- `Pg_repack <https://github.com/reorg/pg_repack>`_ rebuilds |postgresql|
  database objects.
- `Pgaudit <https://www.pgaudit.org/>`_ provides detailed session or object
  audit logging via the standard logging facility provided by |postgresql|
- `pgBackRest <https://pgbackrest.org/>`_ - a backup and restore solution for
  |postgresql|
- `Patroni <https://patroni.readthedocs.io/en/latest/>`_ - an HA solution for
  |postgresql|
- A collection of `additional PostgreSQL contrib extensions
  <https://www.postgresql.org/docs/12/contrib.html>`_

|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/12/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_

This release of |pdp| is based on |postgresql| |version|.

.. |version| replace:: 12.2

.. [#] https://www.postgresql.org/docs/12/libpq.html

.. include:: .res/replace.txt
