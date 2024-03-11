# Run Percona Distribution for PostgreSQL in a Docker container

Docker images of Percona Distribution for PostgreSQL are hosted publicly on [Docker Hub](https://hub.docker.com/r/percona/percona-distribution-postgresql/).

For more information about using Docker, see the [Docker Docs](https://docs.docker.com/).

!!! note ""

    Make sure that you are using the latest version of Docker. The ones provided via `apt` and `yum` may be outdated and cause errors.

    By default, Docker pulls the image from Docker Hub if it is not available locally.

???+ admonition "Docker image contents"

    The Docker image of Percona Distribution for PostgreSQL includes the following components:    

    | Component name                | Description                          |
    |-------------------------------|--------------------------------------|  
    | `percona-postgresql{{pgversion}}`| A metapackage that installs the latest version of PostgreSQL|
     | `percona-postgresql{{pgversion}}-server` | The PostgreSQL server package. |
    | `percona-postgresql-common` | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
    | `percona-postgresql-client-common`| The manager for multiple PostgreSQL client versions.|
    | `percona-postgresql{{pgversion}}-contrib` | A collection of additional PostgreSQLcontrib extensions | 
    | `percona-postgresql{{pgversion}}-libs`| Libraries for use with PostgreSQL.|
    | `percona-pg-stat-monitor{{pgversion}}` | A Query Performance Monitoring tool for PostgreSQL. | 
    | `percona-pgaudit{{pgversion}}` | Provides detailed session or object audit logging via the standard PostgreSQL logging facility. | 
    | `percona-pgaudit{{pgversion}}_set_user`| An additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.|
    | `percona-pg_repack{{pgversion}}`| rebuilds PostgreSQL database objects.| 
    | `percona-wal2json{{pgversion}}` | a PostgreSQL logical decoding JSON output plugin.|

## Start the container

1. Start a Percona Distribution for PostgreSQL container as follows:

    ```{.bash data-prompt="$"}
    $ docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql:<tag>-multi
    ```    

    Where:    

    * `container-name` is the name you assign to your container
    * `POSTGRES_PASSWORD` is the superuser password 
    * `tag-multi` is the tag specifying the version you need. For example, `{{dockertag}}-multi`. The `multi` part of the tag serves to identify the architecture (x86_64 or ARM64) and pull the respective image. See the [full list of tags](https://hub.docker.com/r/percona/percona-distribution-postgresql/tags/).    
    

    !!! tip     

        You can secure the password by exporting it to the environment file and using that to start the container.    

        1. Export the password to the environment file:    

            ```{.bash data-prompt="$"}
            $ echo "POSTGRES_PASSWORD=secret" > .my-pg.env
            ```     

        2. Start the container:       

            ```{.bash data-prompt="$"}
            $ docker run --name container-name --env-file ./.my-pg.env -d percona/percona-distribution-postgresql:<tag>-multi
            ```

2. Connect to the container's interactive terminal: 

    ```{.bash data-prompt="$"}
    $ docker exec -it container-name bash
    ```

    The `container-name` is the name of the container that you started in the previous step.


## Connect to Percona Distribution for PostgreSQL from an application in another Docker container

This image exposes the standard PostgreSQL port (`5432`), so container linking makes the instance available to other containers. Start other containers like this in order to link it to the Percona Distribution for PostgreSQL container:

```{.bash data-prompt="$"}
$ docker run --name app-container-name --network container:container-name -d app-that-uses-postgresql 
```

where:

* `app-container-name` is the name of the container where your application is running, 
* `container name` is the name of your Percona Distribution for PostgreSQL container, and 
* `app-that-uses-postgresql` is the name of your PostgreSQL client.

## Connect to Percona Distribution for PostgreSQL from the `psql` command line client

The following command starts another container instance and runs the `psql` command line client against your original container, allowing you to execute SQL statements against your database:

```{.bash data-prompt="$"}
$ docker run -it --network container:db-container-name --name container-name percona/percona-distribution-postgresql:<tag>-multi psql -h address -U postgres
```

Where:

* `db-container-name` is the name of your database container
* `container-name` is the name of your container that you will use to connect to the database container using the `psql` command line client
* `tag-multi` is the tag specifying the version you need. For example, `{{dockertag}}-multi`. The `multi` part of the tag serves to identify the architecture (x86_64 or ARM64) and pull the respective image. 
* `address` is the network address where your database container is running. Use 127.0.0.1, if the database container is running on the local machine/host.   
## Enable `pg_stat_monitor`

To enable the `pg_stat_monitor` extension after launching the container, do the following:

* connect to the server, 
* select the desired database and enable the `pg_stat_monitor` view for that database:

   ```sql
   create extension pg_stat_monitor;
   ```

* to ensure that everything is set up correctly, run:

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

Note that the `pg_stat_monitor` view is available only for the databases where you enabled it. If you create a new database, make sure to create the view for it to see its statistics data.


