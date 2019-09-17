.. _pdp.release-notes.v11:

|pdp| |version|
********************************************************************************

|percona| is excited to announce the GA release of |pdp| |version| on |date|.
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
  <https://www.postgresql.org/docs/11/contrib.html>`_

|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/11/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_

This release of |pdp| is based on |postgresql| 11.

.. |version| replace:: 11
.. |date| replace:: September 17, 2019

.. [#] https://www.postgresql.org/docs/11/libpq.html

.. include:: .res/replace.txt
