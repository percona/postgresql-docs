> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/18/llms.txt).

# Run Percona Distribution for PostgreSQL in a Docker container

Docker images of Percona Distribution for PostgreSQL are hosted publicly on [Docker Hub](https://hub.docker.com/r/percona/percona-distribution-postgresql/) .

For more information about using Docker, see the [Docker Docs](https://docs.docker.com/) .

Note

Make sure that you are using [the latest version of Docker](https://docs.docker.com/get-docker/) . The ones provided via `apt` and `yum` may be outdated and cause errors.

By default, Docker pulls the image from Docker Hub if it is not available locally.

## 1. Start the container

Start a Percona Distribution for PostgreSQL container as follows:

```
docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql:18.7
```

Where:

- `container-name` is the name you assign to your container
- `POSTGRES_PASSWORD` is the superuser password
- `18.7` is the tag specifying the version you need. Docker identifies the architecture (amd64 or arm64) and pulls the respective image. See the [full list of tags](https://hub.docker.com/r/percona/percona-distribution-postgresql/tags/) .

Tip

You can secure the password by exporting it to the environment file and using that to start the container.

1. Export the password to the environment file:

   ```
   echo "POSTGRES_PASSWORD=secret" > .my-pg.env
   ```

1. Start the container:

   ```
   docker run --name container-name --env-file ./.my-pg.env -d percona/percona-distribution-postgresql:18.7
   ```

Tip

To persist the data even after you remove the container, mount a named volume using the `-v` option:

```
docker run --name container-name -e POSTGRES_PASSWORD=secret -v pg-data:/data/db -d percona/percona-distribution-postgresql:18.7
```

`pg-data` is a volume name of your choice. `/data/db` is the data directory, as provided by this Docker image. To reuse the data, start the new container with the same `-v` option: `-v pg-data:/data/db`.

## 2. Enable extensions

Some extensions require server startup configuration and must be loaded via `shared_preload_libraries` before PostgreSQL starts. You need to explicitly load the extensions when starting the container using the `shared_preload_libraries` parameter, then enabled per database:

1. Start the container with the extensions you want to load:

   ```
   docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql:18.7 -c shared_preload_libraries=example_extension
   ```

1. Connect to the container’s interactive terminal:

   ```
   docker exec -it container-name psql -U postgres
   ```

   The `container-name` is the name of the container that you started in the previous step.

1. Create the extension in the desired database:

   ```
   CREATE EXTENSION example_extension;
   ```

You can specify multiple extensions as a comma-separated list in `shared_preload_libraries`.

For extension-specific setup, see:

- [Enable pg_stat_monitor](https://docs.percona.com/postgresql/18/docker/docker-enable-pg-stat-monitor.html)
- [Enable pg_tde](https://docs.percona.com/postgresql/18/docker/docker-enable-pg-tde.html)

## 3. Update the image

Pull the new tag explicitly:

```
docker pull percona/percona-distribution-postgresql:18.7
```

Or pull the latest image for a major version:

```
docker pull percona/percona-distribution-postgresql:18
```

Note

To upgrade a containerized Percona Distribution for PostgreSQL instance to a new major version, use the dedicated upgrade image. See [Upgrade Percona Distribution for PostgreSQL using the upgrade image](https://docs.percona.com/postgresql/18/docker/docker-upgrade.html).

## 4. Docker image contents

The Docker image of Percona Distribution for PostgreSQL includes the following components:

| Component name                     | Description                                                                                                                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `percona-postgresql18`             | A metapackage that installs the latest version of PostgreSQL                                                                                                                 |
| `percona-postgresql18-server`      | The PostgreSQL server package.                                                                                                                                               |
| `percona-postgresql-common`        | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.   |
| `percona-postgresql-client-common` | The manager for multiple PostgreSQL client versions.                                                                                                                         |
| `percona-postgresql18-contrib`     | A collection of additional PostgreSQLcontrib extensions                                                                                                                      |
| `percona-postgresql18-libs`        | Libraries for use with PostgreSQL.                                                                                                                                           |
| `percona-pg-stat-monitor18`        | A Query Performance Monitoring tool for PostgreSQL.                                                                                                                          |
| `percona-pgaudit18`                | Provides detailed session or object audit logging via the standard PostgreSQL logging facility.                                                                              |
| `percona-pgaudit18_set_user`       | An additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks. |
| `percona-pg_repack18`              | rebuilds PostgreSQL database objects.                                                                                                                                        |
| `percona-wal2json18`               | a PostgreSQL logical decoding JSON output plugin.                                                                                                                            |
| `percona-pgvector`                 | A vector similarity search for PostgreSQL                                                                                                                                    |
| `percona-pg_tde`                   | An extension to provides data-at-rest encryption for PostgreSQL                                                                                                              |

## Connect to Percona Distribution for PostgreSQL from an application in another Docker container

This image exposes the standard PostgreSQL port (`5432`), so container linking makes the instance available to other containers. Start other containers like this in order to link it to the Percona Distribution for PostgreSQL container:

```
docker run --name app-container-name --network container:container-name -d app-that-uses-postgresql
```

where:

- `app-container-name` is the name of the container where your application is running,
- `container name` is the name of your Percona Distribution for PostgreSQL container, and
- `app-that-uses-postgresql` is the name of your PostgreSQL client.

## Connect to Percona Distribution for PostgreSQL from the `psql` command line client

The following command starts another container instance and runs the `psql` command line client against your original container, allowing you to execute SQL statements against your database:

```
docker run -it --network container:db-container-name --name container-name percona/percona-distribution-postgresql:18.7 psql -h address -U postgres
```

where:

- `db-container-name` is the name of your database container
- `container-name` is the name of your container that you will use to connect to the database container using the `psql` command line client
- `18.7` is the tag specifying the version you need. Docker identifies the architecture (x86_64 or ARM64) and pulls the respective image.
- `address` is the network address where your database container is running. Use 127.0.0.1, if the database container is running on the local machine/host.

## Run the PostgreSQL with PostGIS image

The `postgres-gis` image includes everything in the standard Percona Distribution for PostgreSQL image plus the [PostGIS](https://postgis.net/) extension for storing and manipulating spatial data.

Note

PostGIS is licensed under [GNU GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) . Review the license terms before using this image in your environment.

Additional image contents

| Component name    | Description                                   |
| ----------------- | --------------------------------------------- |
| `percona-postgis` | Spatial and geographic objects for PostgreSQL |

Start a `postgres-gis` container as follows:

```
docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql-with-postgis:18.7
```

Where:

- `container-name` is the name you assign to your container
- `POSTGRES_PASSWORD` is the superuser password

For more information on deploying and using PostGIS, see [Spatial data handling](https://docs.percona.com/postgresql/18/solutions/postgis.html).

## Run the PgBouncer image

[PgBouncer](https://www.pgbouncer.org/) is a lightweight connection pooler for PostgreSQL. The Percona PgBouncer image is available separately from the PostgreSQL image and is intended for use alongside it.

Start a PgBouncer container as follows:

```
docker run --name pgbouncer -v /path/to/pgbouncer.ini:/etc/pgbouncer/pgbouncer.ini -d percona/percona-pgbouncer:1.26.1
```

Where:

- `pgbouncer.ini` is your PgBouncer configuration file, mounted into the container. It defines the connection settings to your PostgreSQL instance.
- The image tag specifies the PgBouncer version. See the [full list of tags](https://hub.docker.com/r/percona/percona-pgbouncer/tags/) .

For more information on configuring PgBouncer, see the [PgBouncer documentation](https://www.pgbouncer.org/config.html) .

## Run the pgBackRest image

[pgBackRest](https://pgbackrest.org/) is a backup and restore solution for PostgreSQL, supporting full, differential, and incremental backups as well as point-in-time recovery. The Percona pgBackRest image is available separately from the PostgreSQL image.

Start a pgBackRest container as follows:

```
docker run --name pgbackrest -v /path/to/pgbackrest.conf:/etc/pgbackrest/pgbackrest.conf -d percona/percona-pgbackrest:2.60.0
```

Where:

- `pgbackrest.conf` is your pgBackRest configuration file, mounted into the container. It defines the connection to your PostgreSQL instance and your backup repository settings.
- The image tag specifies the pgBackRest version. See the [full list of tags](https://hub.docker.com/r/percona/percona-pgbackrest/tags/) .

For more information on configuring pgBackRest with Percona Distribution for PostgreSQL, see [Backup and disaster recovery](https://docs.percona.com/postgresql/18/solutions/backup-recovery.html).

## Run the UBI8-based image

The UBI8 image is a variant of the standard Percona Distribution for PostgreSQL image built on Red Hat Universal Base Image 8. It is intended for environments that require UBI8-based containers.

UBI8 images use the same PostgreSQL version and components as the standard image and can be identified by the `-ubi8` suffix in their tags.

```
docker run --name container-name -e POSTGRES_PASSWORD=secret -d percona/percona-distribution-postgresql:18.7-ubi8
```

Where:

- `container-name` is the name you assign to your container
- `POSTGRES_PASSWORD` is the superuser password

See the [full list of tags](https://hub.docker.com/r/percona/percona-distribution-postgresql/tags/) and filter for `ubi8`.
