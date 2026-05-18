# Run Percona Distribution for PostgreSQL in a Docker container

Docker images of Percona Distribution for PostgreSQL are hosted publicly on [Docker Hub :octicons-link-external-16:](https://hub.docker.com/r/percona/percona-distribution-postgresql/).

For more information about using Docker, see the [Docker Docs :octicons-link-external-16:](https://docs.docker.com/).

!!! note
    Make sure that you are using [the latest version of Docker :octicons-link-external-16:](https://docs.docker.com/get-docker/). The ones provided via `apt` and `yum` may be outdated and cause errors.

    By default, Docker pulls the image from Docker Hub if it is not available locally.

???+ admonition "Docker image contents"

    The Docker image of Percona Distribution for PostgreSQL includes the following components:    

    | Component name                | Description                          |
    |-------------------------------|--------------------------------------|  
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
    | `percona-pgvector`              |  A vector similarity search for PostgreSQL|

## Start the container {.power-number}

1. Start a Percona Distribution for PostgreSQL container as follows:

    ```{.bash data-prompt="$"}
    docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql:{{dockertag}}
    ```

    Where:

    * `container-name` is the name you assign to your container
    * `POSTGRES_PASSWORD` is the superuser password 
    * `{{dockertag}}` is the tag specifying the version you need. Docker identifies the architecture (x86_64 or ARM64) and pulls the respective image. See the [full list of tags :octicons-link-external-16:](https://hub.docker.com/r/percona/percona-distribution-postgresql/tags/).

    !!! tip
        You can secure the password by exporting it to the environment file and using that to start the container.

        1. Export the password to the environment file:    

            ```{.bash data-prompt="$"}
            echo "POSTGRES_PASSWORD=secret" > .my-pg.env
            ```     

        2. Start the container:       

            ```{.bash data-prompt="$"}
            docker run --name container-name --env-file ./.my-pg.env -d percona/percona-distribution-postgresql:{{dockertag}}
            ```

2. Connect to the container's interactive terminal:

    ```{.bash data-prompt="$"}
    docker exec -it container-name bash
    ```

    The `container-name` is the name of the container that you started in the previous step.

## Connect to Percona Distribution for PostgreSQL from an application in another Docker container

This image exposes the standard PostgreSQL port (`5432`), so container linking makes the instance available to other containers. Start other containers like this in order to link it to the Percona Distribution for PostgreSQL container:

```{.bash data-prompt="$"}
docker run --name app-container-name --network container:container-name -d app-that-uses-postgresql 
```

where:

* `app-container-name` is the name of the container where your application is running,
* `container name` is the name of your Percona Distribution for PostgreSQL container, and
* `app-that-uses-postgresql` is the name of your PostgreSQL client.

## Connect to Percona Distribution for PostgreSQL from the `psql` command line client

The following command starts another container instance and runs the `psql` command line client against your original container, allowing you to execute SQL statements against your database:

```{.bash data-prompt="$"}
docker run -it --network container:db-container-name --name container-name percona/percona-distribution-postgresql:{{dockertag}} psql -h address -U postgres
```

Where:

* `db-container-name` is the name of your database container
* `container-name` is the name of your container that you will use to connect to the database container using the `psql` command line client
* `{{dockertag}}` is the tag specifying the version you need. Docker identifies the architecture (x86_64 or ARM64) and pulls the respective image.
* `address` is the network address where your database container is running. Use 127.0.0.1, if the database container is running on the local machine/host.

## Enable encryption

Percona Distribution for PostgreSQL Docker image includes the `pg_tde` extension to provide data encryption. You must explicitly enable it when you start the container. For more information, see the [pg_tde documentation :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html).

Follow these steps to enable `pg_tde`:
{.power-number}

1. Start the container with `pg_tde` added to `shared_preload_libraries`:

    ```{.bash data-prompt="$"}
    docker run --name container-name -e POSTGRES_PASSWORD=sUpers3cRet -d percona/percona-distribution-postgresql:{{dockertag}} -c 'shared_preload_libraries=pg_tde'
    ```

    where:

    * `container-name` is the name you assign to your container
    * `shared_preload_libraries=pg_tde` enables the `pg_tde` extension and its custom storage manager
    * `POSTGRES_PASSWORD` is the superuser password

    !!! note
        Available starting with version 17.9. For earlier versions, use `-e ENABLE_PG_TDE=1` instead.

2. Connect to the container and start the interactive `psql` session:

    ```{.bash data-prompt="$"}
    docker exec -it container-name psql
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        psql ({{pgsubversion}} - Percona Server for PostgreSQL {{dockertag}})
        Type "help" for help.

        postgres=#
        ```

3. Create the extension in the database where you want to encrypt data. This requires superuser privileges.

    ```sql
    CREATE EXTENSION pg_tde;
    ```

4. Add the key provider by using a keyring file. This setup is intended for development and stores the keys unencrypted in the specified data file. The below sample configuration is intended for testing and development purposes only.

    !!! note
         For production use, we **strongly recommend** setting up an external key management store and configure an external key provider. Refer to the [Setup :octicons-link-external-16:](https://docs.percona.com/pg-tde/setup.html#key-provider-configuration) topic in the `pg_tde` documentation.

    <i warning>:material-information: Warning:</i> This example is for testing purposes only:

	```sql
	SELECT pg_tde_add_database_key_provider_file('file-vault', '/tmp/pg_tde_test_001_basic.per');
    ```

5. Create the key:

    ```sql
    SELECT pg_tde_create_key_using_database_key_provider('test-db-key', 'file-vault');
    ```

5. Set the principal key:

    ```sql
    SELECT pg_tde_set_key_using_database_key_provider('test-db-key', 'file-vault');
    ```

6. Create a table with encryption enabled. Pass the `USING tde_heap` clause to the `CREATE TABLE` command:

    ```sql
    CREATE TABLE <table_name> (<field> <datatype>) USING tde_heap;
    ```

    ??? example "CREATE TABLE example"

        ```{.sql .no-copy}
        CREATE TABLE test_users (
            user_id INT,
            username VARCHAR(50),
            email VARCHAR(100),
            signup_date DATE
        ) USING tde_heap;
        ```

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

!!! note
     The `pg_stat_monitor` view is available only for the databases where you enabled it. If you create a new database, make sure to create the view for it to see its statistics data.
