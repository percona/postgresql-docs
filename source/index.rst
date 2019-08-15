.. _pdp.index:


|pdp| Documentation
********************************************************************************

|pdp| is a collection of tools to assist you in managing your |postgresql|
database system: it installs |postgres| and complements it by a selectipon of
extensions that enable solving essential practical tasks efficiently:

- `pg_repack <https://github.com/reorg/pg_repack>`_ rebuilds
  |postgresql| database objects
- `pgaudit <https://www.pgaudit.org/>`_ provides detailed session or object
  audit logging via the standard |postgresql| logging facility
- `pgBackRest <https://pgbackrest.org/>`_ is a backup and restore solution for
  |postgresql|
- `Patroni <https://patroni.readthedocs.io/en/latest/>`_ is an :abbr:`HA (High
  Availability)` solution for |postgresql|.
- A collection of `additional PostgreSQL contrib extensions
  <https://www.postgresql.org/docs/11/contrib.html>`_

.. seealso::

   |percona| Blog Posts
      - `pgBackRest – A Great Backup Solution and a Wonderful Year of Growth
        <https://www.percona.com/blog/2019/05/10/pgbackrest-a-great-backup-solution-and-a-wonderful-year-of-growth/>`_
      - `Securing PostgreSQL as an Enterprise-Grade Environment
        <https://www.percona.com/blog/2018/09/21/securing-postgresql-as-an-enterprise-grade-environment/>`_
	
|pdp| is also shipped with the `libpq
<https://www.postgresql.org/docs/11/libpq.html>`_ library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." [#]_

.. toctree::
   :maxdepth: 1

   installing
   release-notes

.. [#] https://www.postgresql.org/docs/11/libpq.html
  
.. include:: .res/replace.txt
