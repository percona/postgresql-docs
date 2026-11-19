# Upgrade Percona Distribution for PostgreSQL

To upgrade Percona Distribution for PostgreSQL in Docker to a new major version, use the dedicated `percona/percona-distribution-postgresql-upgrade` image. It bundles the server binaries for several consecutive major versions, so `pg_upgrade` can run against your old and new data directories.

!!! important
    Back up your data before you start. The backup tool is out of scope for this document. Use the backup tool of your choice.

!!! warning
    If your cluster uses `pg_tde`, do not follow these steps. Using `pg_upgrade` on an encrypted cluster is not supported and will result in data corruption. See [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md) for details.

!!! note
    If you're upgrading an existing instance rather than following along with the step 1-5 example, skip those steps and start from step 6 with your own running container and data.

## 1. Create directories for the old and new clusters { .power-number }

```{.bash data-prompt="$"}
mkdir -p ~/pgupgrade/pg18olddata/postgres
mkdir -p ~/pgupgrade/pg19newdata/postgres
```

## 2. Start the PostgreSQL 18 container

```{.bash data-prompt="$"}
docker run -d
  --name pg18
  -e POSTGRES_PASSWORD=password
  -v ~/pgupgrade/pg18olddata/postgres:/data/db
  percona/percona-distribution-postgresql:18
```

## 3. Wait until PostgreSQL finishes initialization

```{.bash data-prompt="$"}
docker logs pg18
```

## 4. Connect to PostgreSQL

```{.bash data-prompt="$"}
docker exec -it pg18 psql -U postgres
```

## 5. Create a test database and add data

```sql
CREATE DATABASE testdb;
\c testdb
CREATE TABLE t1(a int);
INSERT INTO t1 VALUES (100);
```

## 6. Stop the PostgreSQL 18 container

```{.bash data-prompt="$"}
docker stop pg18
```

## 7. Pull the upgrade image

```{.bash data-prompt="$"}
docker pull percona/percona-distribution-postgresql-upgrade:19.0-18.7-17.12-16.16-15.20-14.25-1
```

The tag encodes all bundled versions; here it covers PostgreSQL 14 through 19.

## 8. Run the upgrade

```{.bash data-prompt="$"}
docker run --rm
  --name ppg_upgrade_18_19
  -e OLD_VERSION=18
  -e NEW_VERSION=19
  -e OLD_DATABASE_NAME=postgres
  -e NEW_DATABASE_NAME=postgres
  -v ~/pgupgrade/pg18olddata:/pgolddata
  -v ~/pgupgrade/pg19newdata:/pgnewdata
  percona/percona-distribution-postgresql-upgrade:19.0-18.7-17.12-16.16-15.20-14.25-1
```

Where:

* `OLD_VERSION` / `NEW_VERSION` are the major versions you're upgrading from and to
* `OLD_DATABASE_NAME` / `NEW_DATABASE_NAME` are the database directory names under your old and new data mounts
* the volumes mount the parent directories (`pg18olddata`, `pg19newdata`), **not** the `postgres` subdirectory directly

## 9. Start PostgreSQL 19 using the upgraded data directory

```{.bash data-prompt="$"}
docker run -d
  --name pg19
  -e POSTGRES_PASSWORD=password
  -v ~/pgupgrade/pg19newdata/postgres:/data/db
  percona/percona-distribution-postgresql:19
```

## 10. Verify PostgreSQL 19 starts successfully

```{.bash data-prompt="$"}
docker logs -f pg19
```

## 11. Connect to the upgraded cluster

```{.bash data-prompt="$"}
docker exec -it pg19 psql -U postgres testdb
```

## 12. Verify the upgraded data

```sql
SELECT version();
SELECT * FROM t1;
```

Once you've confirmed the upgraded container is healthy, you can remove `pg18olddata`.

## Next steps

[Enable `pg_tde` for securing data at rest :material-arrow-right:](docker-enable-pg-tde.md){.md-button}
