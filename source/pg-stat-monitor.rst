.. _pg_stat-monitor:

pg_stat_monitor 
****************************

.. note::

   This is a technical preview feature and it is subject to further changes.

Overview
============================

``pg_stat_monitor`` is a |postgres| Query Performance Monitoring 
tool. It collects statistics data and writes it in a storage unit called *bucket*. The data is added and stored in a bucket for the defined period – the bucket lifetime. 

You can specify the following:

-	The number of buckets. Together they form a bucket chain.
-	Bucket size. This is the amount of shared memory allocated for buckets. Memory is divided equally among buckets.
-	Bucket lifetime.

When a bucket lifetime expires, ``pg_stat_monitor`` resets all statistics and writes the data in the next bucket in the chain. When the last bucket's lifetime expires, ``pg_stat_monitor`` returns to the first bucket.

.. important::

   The contents of the bucket will be overwritten. In order not to lose the data, make sure to read the bucket before ``pg_stat_monitor`` starts writing new data to it. 

.. _pg_stat-setup:

Setup
===========================

After the :ref:`installation <pdp.installing>`, ``pg_stat_monitor`` requires additional setup in order to use it with |postgres|. The setup steps are the following:

1. Add ``pg_stat_monitor`` in the ``shared_preload_libraries`` configuration parameter.

   The recommended way to modify |postgres| configuration file is using the `ALTER SYSTEM <https://www.postgresql.org/docs/11/sql-altersystem.html>`_ command. :ref:`Connect to psql <server-connect>` and use the following command:

   .. code-block:: bash

      $ ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_monitor';

   The parameter value is written to the :file:`postgresql.auto.conf` file which is read in addition with :file:`postgresql.conf` file.

#. Start or restart the PostgreSQL instance to enable ``pg_stat_monitor``. Use the following command for restart:  

   - On Debian and Ubuntu:

     .. code-block:: bash

        $ sudo systemctl restart postgresql.service

   - On |rhel| and CentOS:
  
     .. code-block:: bash
  
        $ sudo systemctl restart postgresql-11

#. Create the extension. Connect to ``psql`` and use the following command:
    
   .. code-block:: bash
    
      $ CREATE EXTENSION pg_stat_monitor; 

Usage
===================

``pg_stat_monitor`` provides two views:

- ``pg_stat_monitor`` is the view where statistics data is presented.
- ``pg_stat_monitor_settings`` shows available configuration options which you can change. To learn more, see :ref:`change-config`.

Use the following query to view what metrics ``pg_stat_monitor`` can collect:

.. code-block:: bash

   $ \d pg_stat_monitor;

**Output**

.. code-block:: text 

                        View "public.pg_stat_monitor"
          Column        |           Type           | Collation | Nullable | Default
   ---------------------+--------------------------+-----------+----------+---------
    bucket              | integer                  |           |          |
    bucket_start_time   | timestamp with time zone |           |          |
    userid              | oid                      |           |          |
    dbid                | oid                      |           |          |
    client_ip           | inet                     |           |          |
    queryid             | text                     |           |          |
    query               | text                     |           |          |
    application_name    | text                     |           |          |
    relations           | text[]                   |           |          |
    cmd_type            | text[]                   |           |          |
    elevel              | integer                  |           |          |
    sqlcode             | integer                  |           |          |
    message             | text                     |           |          |
    plans               | bigint                   |           |          |
    plan_total_time     | double precision         |           |          |
    plan_min_timei      | double precision         |           |          |
    plan_max_time       | double precision         |           |          |
    plan_mean_time      | double precision         |           |          |
    plan_stddev_time    | double precision         |           |          |
    calls               | bigint                   |           |          |
    total_time          | double precision         |           |          |
    min_time            | double precision         |           |          |
    max_time            | double precision         |           |          |
    mean_time           | double precision         |           |          |
    stddev_time         | double precision         |           |          |
    rows                | bigint                   |           |          |
    shared_blks_hit     | bigint                   |           |          |
    shared_blks_read    | bigint                   |           |          |
    shared_blks_dirtied | bigint                   |           |          |
    shared_blks_written | bigint                   |           |          |
    local_blks_hit      | bigint                   |           |          |
    local_blks_read     | bigint                   |           |          |
    local_blks_dirtied  | bigint                   |           |          |
    local_blks_written  | bigint                   |           |          |
    temp_blks_read      | bigint                   |           |          |
    temp_blks_written   | bigint                   |           |          |
    blk_read_time       | double precision         |           |          |
    blk_write_time      | double precision         |           |          |
    resp_calls          | text[]                   |           |          |
    cpu_user_time       | double precision         |           |          |
    cpu_sys_time        | double precision         |           |          |

For example, to view the IP address of the client application that made the query, run the following command:

.. code-block:: bash

   $ SELECT userid::regrole, datname, substr(query,0, 50) AS query, calls, client_ip
     FROM pg_stat_monitor, pg_database
     WHERE dbid = oid;

     userid  | datname  |                       query                       | calls | client_ip
   ----------+----------+---------------------------------------------------+-------+-----------
    postgres | postgres | select bucket, bucket_start_time, query,calls fro |     1 | 127.0.0.1
    postgres | postgres | SELECT c.relchecks, c.relkind, c.relhasindex, c.r |     1 | 127.0.0.1
    postgres | postgres | SELECT  userid,  total_time, min_time, max_time,  |     1 | 127.0.0.1         

Find more usage examples  in `pg_stat_monitor User Guide <https://github.com/percona/pg_stat_monitor/blob/REL0_8_1/docs/USER_GUIDE.md>`_.

.. _change-config:

Changing the configuration
==================================

Run the following query to list available configuration parameters.

.. code-block:: sh

   $ SELECT name,description FROM pg_stat_monitor_settings;

**Output**

.. code-block:: text

   name                      |                            description
   -----------------------------------------------+-------------------------------------------------------------------
    pg_stat_monitor.pgsm_max                      | Sets the maximum number of statements tracked by pg_stat_monitor.
    pg_stat_monitor.pgsm_query_max_len            | Sets the maximum length of query.
    pg_stat_monitor.pgsm_enable                   | Enable/Disable statistics collector.
    pg_stat_monitor.pgsm_track_utility            | Selects whether utility commands are tracked.
    pg_stat_monitor.pgsm_normalized_query         | Selects whether save query in normalized format.
    pg_stat_monitor.pgsm_max_buckets              | Sets the maximum number of buckets.
    pg_stat_monitor.pgsm_bucket_time              | Sets the time in seconds per bucket.
    pg_stat_monitor.pgsm_object_cache             | Sets the maximum number of object cache
    pg_stat_monitor.pgsm_respose_time_lower_bound | Sets the time in millisecond.
    pg_stat_monitor.pgsm_respose_time_step        | Sets the response time steps in millisecond.
    pg_stat_monitor.pgsm_query_shared_buffer      | Sets the query shared_buffer size.   

You can change a parameter by setting a new value in the configuration file. Some parameters require server restart to apply a new value. For others, configuration reload is enough. Refer to the `configuration section <https://github.com/percona/pg_stat_monitor/blob/REL0_8_1/docs/USER_GUIDE.md#configuration>`_ of the ``pg_stat_monitor`` documentation for the parameters’ description, how you can change their values and if the server restart is required to apply them.

As an example, let's set the bucket lifetime from default 60 seconds to 100 seconds. Use the :command:`ALTER SYSTEM` command:

.. code-block:: bash

   $ ALTER SYSTEM set pg_stat_monitor.pgsm_bucket_time = 100;

Restart the server to apply the change:

- On Debian and Ubuntu

  .. code-block:: bash

     $ sudo systemctl restart restart postgresql.service

- On |rhel| and CentOS:
  
  .. code-block:: bash
  
     $ sudo systemctl restart postgresql-11

Verify the updated parameter:

.. code-block:: bash 

   $ SELECT name, value 
     FROM pg_stat_monitor_settings
     WHERE name = 'pg_stat_monitor.pgsm_bucket_time';

                    name               | value
     ----------------------------------+-------
      pg_stat_monitor.pgsm_bucket_time |   100

.. seealso::

   ``pg_stat_monitor`` Documentation 
       https://github.com/percona/pg_stat_monitor/blob/REL0_8_1/README.md

   Percona Blog: pg_stat_monitor: A New Way Of Looking At PostgreSQL Metrics
       https://www.percona.com/blog/2021/01/19/pg_stat_monitor-a-new-way-of-looking-at-postgresql-metrics/


.. include:: .res/replace.txt