.. _psp.index:


|pdp| Documentation
********************************************************************************

|pdp| is an enhanced drop-in replacement for |postgresql|. This
release is based on |postgresql| 11. It also includes a selection of
extensions that help manage |postgresql| more efficiently:

- `Pg_repack <is a PostgreSQL extension which lets you remove bloat
  from tables and indexes, and optionally restore the physical order
  of clustered indexes>`_ extension to remove bloat from tables and
  indexes and optionally restore the physical order of clustered
  indexes.
- A collection of `additional PostgreSQL contrib extensions
  <https://www.postgresql.org/docs/11/contrib.html>`_
- `Pgaudit <https://www.pgaudit.org/>`_ to provide detailed session or
  object audit logging via the standard logging facility provided by
  |postgresql|
- `pgBackRest <https://pgbackrest.org/>`_ - a backup and restore
  solution for |postgresql|
- `Patroni <https://patroni.readthedocs.io/en/latest/>`_ - an HA
  solution for |postgresql|

|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/11/libpq.html>`_ library. It contains
"a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."[#]


.. toctree::
   
   installing


- [#] https://www.postgresql.org/docs/11/libpq.html
  
.. include:: .res/replace.txt
