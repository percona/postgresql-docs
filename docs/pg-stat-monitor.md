# pg_stat_monitor

!!! note

    This document describes the functionality of pg_stat_monitor {{pgsmversion}}.

## Overview

`pg_stat_monitor` is a  Query Performance Monitoring
tool for PostgreSQL. It collects various statistics data such as query statistics, query plan, SQL comments and other performance insights. The collected data is aggregated and presented in a single view. This allows you to view queries from performance, application and analysis perspectives.

`pg_stat_monitor` groups statistics data and writes it in a storage unit called *bucket*. The data is added and stored in a bucket for the defined period – the bucket lifetime. This allows you to identify performance issues and patterns based on time.

You can specify the following:


* The number of buckets. Together they form a bucket chain.
* Bucket size. This is the amount of shared memory allocated for buckets. Memory is divided equally among buckets.
* Bucket lifetime.

When a bucket lifetime expires, `pg_stat_monitor` resets all statistics and writes the data in the next bucket in the chain. When the last bucket’s lifetime expires, `pg_stat_monitor` returns to the first bucket.

!!! important

    The contents of the bucket will be overwritten. In order not to lose the data, make sure to read the bucket before `pg_stat_monitor` starts writing new data to it.


### Views

#### pg_stat_monitor view

The `pg_stat_monitor` view contains all the statistics collected and aggregated by the extension. This view contains one row for each distinct combination of metrics and whether it is a top-level statement or not (up to the maximum number of distinct statements that the module can track). For details about available metrics, refer to the [`pg_stat_monitor` view reference :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/reference.html).

The following are the primary keys for pg_stat_monitor:

*  `bucket`
*  `userid`
*  `datname`
*  `queryid`
*  `client_ip`
*  `planid`
*  `application_name`

A new row is created for each key in the `pg_stat_monitor` view.

For security reasons, only superusers and members of the `pg_read_all_stats` role are allowed to see the SQL text, `client_ip` and `queryid` of queries executed by other users. Other users can see the statistics, however, if the view has been installed in their database.

#### pg_stat_monitor_settings view (dropped)

Starting with version 2.0.0, the `pg_stat_monitor_settings` view is deprecated and removed. All `pg_stat_monitor` configuration parameters are now available though the `pg_settings` view using the following query: 

```sql
SELECT name, setting, unit, context, vartype, source, min_val, max_val, enumvals, boot_val, reset_val, pending_restart FROM pg_settings WHERE name LIKE '%pg_stat_monitor%';
```

For backward compatibility, you can create the `pg_stat_monitor_settings` view using the following SQL statement:

```sql
CREATE VIEW pg_stat_monitor_settings

AS

SELECT *

FROM pg_settings

WHERE name like 'pg_stat_monitor.%';
```

In `pg_stat_monitor` version 1.1.1 and earlier, the `pg_stat_monitor_settings` view shows one row per `pg_stat_monitor` configuration parameter. It displays configuration parameter name, value, default value, description, minimum and maximum values, and whether a restart is required for a change in value to be effective.

To learn more, see the [Changing the configuration](#changing-the-configuration) section.

## Installation

This section describes how to install `pg_stat_monitor` from Percona repositories. To learn about other installation methods, see the [Installation :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/install.html) section in the `pg_stat_monitor` documentation.

**Preconditions**:

To install `pg_stat_monitor` from Percona repositories, you need to subscribe to them. To do this, you must have the [`percona-release` repository management tool :octicons-link-external-16:](https://www.percona.com/doc/percona-repo-config/installing.html) up and running. 

To install `pg_stat_monitor`, run the following commands:

=== "On Debian and Ubuntu"

    1. Enable the repository

        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ppg15
        ```

    2. Install the package:

        ```{.bash data-prompt="$"}
        $ sudo apt-get install percona-pg-stat-monitor15
        ```

=== "On Red Hat Enterprise Linux and derivatives"

    1. Enable the repository

        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ppg15
        ```
    
    2. Install the package:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pg-stat-monitor15
        ```

## Setup

`pg_stat_monitor` requires additional setup in order to use it with PostgreSQL. The setup steps are the following:


1. Add `pg_stat_monitor` in the `shared_preload_libraries` configuration parameter.

    The recommended way to modify PostgreSQL configuration file is using the [ALTER SYSTEM :octicons-link-external-16:](https://www.postgresql.org/docs/15/sql-altersystem.html) command. [Connect to psql](installing.md#connect-to-the-server) and use the following command:

    ```sql
    ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_monitor';
    ```

    The parameter value is written to the `postgresql.auto.conf` file which is read in addition with `postgresql.conf` file.

    !!! note

        To use `pg_stat_monitor` together with `pg_stat_statements`, specify both modules separated by commas for the `ALTER SYSTEM SET` command. 

        The order of modules is important: `pg_stat_monitor` must be specified **after** `pg_stat_statements`: 
       
        ```sql
        ALTER SYSTEM SET shared_preload_libraries = ‘pg_stat_statements, pg_stat_monitor’
        ```

2. Start or restart the `postgresql` instance to enable `pg_stat_monitor`. Use the following command for restart:


    === "On Debian and Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo systemctl restart postgresql.service
         ```


    === "On Red Hat Enterprise Linux and derivatives"

         ```{.bash data-prompt="$"}
         $ sudo systemctl restart postgresql-15
         ```


3. Create the extension. Connect to `psql` and use the following command:

    ```sql
    CREATE EXTENSION pg_stat_monitor;
    ```

    By default, the extension is created against the `postgres` database. You need to create the extension on every database where you want to collect statistics.

!!! tip
  
    To check the version of the extension, run the following command in the `psql` session:

    ```sql
    SELECT pg_stat_monitor_version();
    ``` 

## Usage

For example, to view the IP address of the client application that made the query, run the following command:

```sql
SELECT DISTINCT userid::regrole, pg_stat_monitor.datname, substr(query,0, 50) AS query, calls, bucket, bucket_start_time, queryid, client_ip
FROM pg_stat_monitor, pg_database
WHERE pg_database.oid = oid;
```

Output:

```
  userid  | datname  |                       query                       | calls | bucket |  bucket_start_time  |     queryid      | client_ip
----------+----------+---------------------------------------------------+-------+--------+---------------------+------------------+-----------
 postgres | postgres | SELECT name,description FROM pg_stat_monitor_sett |     1 |      9 | 2022-10-24 07:29:00 | AD536A8DEA7F0C73 | 127.0.0.1
 postgres | postgres | SELECT c.oid,                                    +|     1 |      9 | 2022-10-24 07:29:00 | 34B888E5C844519C | 127.0.0.1
          |          |   n.nspname,                                     +|       |        |                     |                  |
          |          |   c.relname                                      +|       |        |                     |                  |
          |          | FROM pg_ca                                        |       |        |                     |                  |
 postgres | postgres | SELECT DISTINCT userid::regrole, pg_stat_monitor. |     1 |      1 | 2022-10-24 07:31:00 | 6230793895381F1D | 127.0.0.1
 postgres | postgres | SELECT pg_stat_monitor_version()                  |     1 |      9 | 2022-10-24 07:29:00 | B617F5F12931F388 | 127.0.0.1
 postgres | postgres | CREATE EXTENSION pg_stat_monitor                  |     1 |      8 | 2022-10-24 07:28:00 | 14B98AF0776BAF7B | 127.0.0.1
 postgres | postgres | SELECT a.attname,                                +|     1 |      9 | 2022-10-24 07:29:00 | 96F8E4B589EF148F | 127.0.0.1
          |          |   pg_catalog.format_type(a.attt                   |       |        |                     |                  |
 postgres | postgres | SELECT c.relchecks, c.relkind, c.relhasindex, c.r |     1 |      9 | 2022-10-24 07:29:00 | CCC51D018AC96A25 | 127.0.0.1

```


Find more usage examples in the [`pg_stat_monitor` user guide :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/user_guide.html).

## Changing the configuration

Run the following query to list available configuration parameters.

```sql
SELECT name, short_desc FROM pg_settings WHERE name LIKE '%pg_stat_monitor%';
```

**Output**

```
                   name                    |                                                           short_desc
-------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------
 pg_stat_monitor.pgsm_bucket_time          | Sets the time in seconds per bucket.
 pg_stat_monitor.pgsm_enable_overflow      | Enable/Disable pg_stat_monitor to grow beyond shared memory into swap space.
 pg_stat_monitor.pgsm_enable_pgsm_query_id | Enable/disable PGSM specific query id calculation which is very useful in comparing same query across databases and clusters..
 pg_stat_monitor.pgsm_enable_query_plan    | Enable/Disable query plan monitoring.
 pg_stat_monitor.pgsm_extract_comments     | Enable/Disable extracting comments from queries.
 pg_stat_monitor.pgsm_histogram_buckets    | Sets the maximum number of histogram buckets.
 pg_stat_monitor.pgsm_histogram_max        | Sets the time in millisecond.
 pg_stat_monitor.pgsm_histogram_min        | Sets the time in millisecond.
 pg_stat_monitor.pgsm_max                  | Sets the maximum size of shared memory in (MB) used for statement's metadata tracked by pg_stat_monitor.
 pg_stat_monitor.pgsm_max_buckets          | Sets the maximum number of buckets.
 pg_stat_monitor.pgsm_normalized_query     | Selects whether save query in normalized format.
 pg_stat_monitor.pgsm_overflow_target      | Sets the overflow target for pg_stat_monitor. (Deprecated, use pgsm_enable_overflow)
 pg_stat_monitor.pgsm_query_max_len        | Sets the maximum length of query.
 pg_stat_monitor.pgsm_query_shared_buffer  | Sets the maximum size of shared memory in (MB) used for query tracked by pg_stat_monitor.
 pg_stat_monitor.pgsm_track                | Selects which statements are tracked by pg_stat_monitor.
 pg_stat_monitor.pgsm_track_planning       | Selects whether planning statistics are tracked.
 pg_stat_monitor.pgsm_track_utility        | Selects whether utility commands are tracked.
```

You can change a parameter by setting a new value in the configuration file. Some parameters require server restart to apply a new value. For others, configuration reload is enough. Refer to the [configuration parameters :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/configuration.html) of the `pg_stat_monitor` documentation for the parameters’ description, how you can change their values and if the server restart is required to apply them.

As an example, let’s set the bucket lifetime from default 60 seconds to 40 seconds. Use the **ALTER SYSTEM** command:

```sql
ALTER SYSTEM set pg_stat_monitor.pgsm_bucket_time = 40;
```

Restart the server to apply the change:


=== "On Debian and Ubuntu"

     ```{.bash data-prompt="$"}
     $ sudo systemctl restart postgresql.service
     ```

=== "On Red Hat Enterprise Linux and derivatives"

     ```{.bash data-prompt="$"}
     $ sudo systemctl restart postgresql-15
     ```

Verify the updated parameter:

```sql
SELECT name, setting 
FROM pg_settings 
WHERE name = 'pg_stat_monitor.pgsm_bucket_time';

                 name               | setting
  ----------------------------------+---------
   pg_stat_monitor.pgsm_bucket_time |   40
```

!!! admonition "See also"

    [`pg_stat_monitor` Documentation :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/index.html)


    Percona Blog:

    * [pg_stat_monitor: A New Way Of Looking At PostgreSQL Metrics :octicons-link-external-16:](https://www.percona.com/blog/2021/01/19/pg_stat_monitor-a-new-way-of-looking-at-postgresql-metrics/)
    * [Improve PostgreSQL Query Performance Insights with pg_stat_monitor :octicons-link-external-16:](https://www.percona.com/blog/improve-postgresql-query-performance-insights-with-pg_stat_monitor/)
