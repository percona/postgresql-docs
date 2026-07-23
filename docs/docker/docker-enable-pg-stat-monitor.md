# Enable `pg_stat_monitor` for performance statistics

`pg_stat_monitor` is a query performance monitoring tool for PostgreSQL which aggregates collected performance statistics.

For more information on this extension, see [pg_stat_monitor :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/).

## Enable pg_stat_monitor {.power-number}

1. Start the container as shown in [Run in Docker](docker.md#start-container), adding the following option to the `docker run` command:

    ```{.bash data-prompt="$"}
    -c shared_preload_libraries=pg_stat_monitor
    ```

2. Connect to the container and start the interactive `psql` session:

    ```{.bash data-prompt="$"}
    docker exec -it container-name psql -U postgres
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        psql ({{pgsubversion}} - Percona Server for PostgreSQL {{dockertag}})
        Type "help" for help.

        postgres=#
        ```

3. Create the extension in the desired database:

    ```sql
    CREATE EXTENSION pg_stat_monitor;
    ```

    ??? example "Sample output"

            ```{.text .no-copy}
            postgres=# CREATE EXTENSION pg_stat_monitor;
            CREATE EXTENSION
            ```

4. Verify the setup:

    ```sql
    \d pg_stat_monitor;
    ```

??? example "Output"

    ```
                             View "public.pg_stat_monitor"
          Column        |           Type           | Collation | Nullable | Default
    ---------------------+--------------------------+-----------+----------+---------
    bucket              | integer                  |           |          |
    bucket_start_time   | timestamp with time zone |           |          |
    userid              | oid                      |           |          |
    dbid                | oid                      |           |          |
    queryid             | text                     |           |          |
    query               | text                     |           |          |
    plan_calls          | bigint                   |           |          |
    plan_total_time     | numeric                  |           |          |
    plan_min_timei      | numeric                  |           |          |
    plan_max_time       | numeric                  |           |          |
    plan_mean_time      | numeric                  |           |          |
    plan_stddev_time    | numeric                  |           |          |
    plan_rows           | bigint                   |           |          |
    calls               | bigint                   |           |          |
    total_time          | numeric                  |           |          |
    min_time            | numeric                  |           |          |
    max_time            | numeric                  |           |          |
    mean_time           | numeric                  |           |          |
    stddev_time         | numeric                  |           |          |
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
    host                | bigint                   |           |          |
    client_ip           | inet                     |           |          |
    resp_calls          | text[]                   |           |          |
    cpu_user_time       | double precision         |           |          |
    cpu_sys_time        | double precision         |           |          |
    tables_names        | text[]                   |           |          |
    wait_event          | text                     |           |          |
    wait_event_type     | text                     |           |          |
    ```

!!! note
     The `pg_stat_monitor` view is available only for the databases where you enabled it. If you create a new database, make sure to create the view for it to see its statistics data.

## Next steps

[Enable Percona Distribution for PostgreSQL components :material-arrow-right:](../enable-extensions.md){.md-button}
