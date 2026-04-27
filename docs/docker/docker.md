# Run Percona Distribution for PostgreSQL in a Docker container

Docker images of Percona Distribution for PostgreSQL are hosted publicly on [Docker Hub :octicons-link-external-16:](https://hub.docker.com/r/percona/percona-distribution-postgresql/).

For more information about using Docker, see the [Docker Docs :octicons-link-external-16:](https://docs.docker.com/).

!!! note

    Make sure that you are using [the latest version of Docker :octicons-link-external-16:](https://docs.docker.com/get-docker/). The ones provided via `apt` and `yum` may be outdated and cause errors.

    By default, Docker pulls the image from Docker Hub if it is not available locally.

## 1. Start the container {.power-number}

Start a Percona Distribution for PostgreSQL container as follows:

```{.bash data-prompt="$"}
docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql:{{dockertag}}
```

Where:

* `container-name` is the name you assign to your container
* `POSTGRES_PASSWORD` is the superuser password 
* `{{dockertag}}` is the tag specifying the version you need. Docker identifies the architecture (x86_64 or ARM64) and pulls the respective image. See the [full list of tags :octicons-link-external-16:](https://hub.docker.com/r/percona/percona-distribution-postgresql/tags/).

!!! note

    Some extensions require server startup configuration and must be loaded via `shared_preload_libraries` before PostgreSQL starts.

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

## 2. Enable extensions

Extensions must be explicitly loaded when starting the container using the `shared_preload_libraries` parameter, then enabled per database:

1. Start the container with the extensions you want to load:

    ```{.bash data-prompt="$"}
    docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql:{{dockertag}} -c shared_preload_libraries=example_extension
    ```

2. Connect to the container's interactive terminal:

```{.bash data-prompt="$"}
docker exec -it container-name bash
```

    The `container-name` is the name of the container that you started in the previous step.

3. Create the extension in the desired database:

    ```sql
    CREATE EXTENSION example_extension;
    ```

You can specify multiple extensions as a comma-separated list in `shared_preload_libraries`.

For extension-specific setup, see:

- [Enable pg_stat_monitor](docker-enable-pg-stat-monitor.md)
- [Enable pg_tde](docker-enable-pg-tde.md)

## 3. Update the image

Pull the new tag explicitly:

```bash
docker pull percona/percona-distribution-postgresql:{{dockertag}}
```

Or pull the latest image for a major version:

```bash
docker pull percona/percona-distribution-postgresql:{{pgversion}}
```

## 4. Docker image contents

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
| `percona-pgvector`              |  A vector similarity search for PostgreSQL|

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

where:

* `db-container-name` is the name of your database container
* `container-name` is the name of your container that you will use to connect to the database container using the `psql` command line client
* `{{dockertag}}` is the tag specifying the version you need. Docker identifies the architecture (x86_64 or ARM64) and pulls the respective image.
* `address` is the network address where your database container is running. Use 127.0.0.1, if the database container is running on the local machine/host.
