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
mkdir -p ~/pgupgrade/pg{{pgversionprev}}olddata/postgres
mkdir -p ~/pgupgrade/pg{{pgversion}}newdata/postgres
```

## 2. Start the PostgreSQL {{pgversionprev}} container

```{.bash data-prompt="$"}
docker run -d
  --name pg{{pgversionprev}}
  -e POSTGRES_PASSWORD=password
  -v ~/pgupgrade/pg{{pgversionprev}}olddata/postgres:/data/db
  percona/percona-distribution-postgresql:{{pgversionprev}}
```

## 3. Wait until PostgreSQL finishes initialization

```{.bash data-prompt="$"}
docker logs pg{{pgversionprev}}
```

## 4. Connect to PostgreSQL

```{.bash data-prompt="$"}
docker exec -it pg{{pgversionprev}} psql -U postgres
```

## 5. Create a test database and add data

```sql
CREATE DATABASE testdb;
\c testdb
CREATE TABLE t1(a int);
INSERT INTO t1 VALUES (100);
```

## 6. Stop the PostgreSQL {{pgversionprev}} container

```{.bash data-prompt="$"}
docker stop pg{{pgversionprev}}
```

## 7. Pull the upgrade image

```{.bash data-prompt="$"}
docker pull percona/percona-distribution-postgresql-upgrade:{{dockerupgradetag}}
```

The tag encodes all bundled versions; here it covers PostgreSQL 14 through 19.

## 8. Run the upgrade

```{.bash data-prompt="$"}
docker run --rm
  --name ppg_upgrade_{{pgversionprev}}_{{pgversion}}
  -e OLD_VERSION={{pgversionprev}}
  -e NEW_VERSION={{pgversion}}
  -e OLD_DATABASE_NAME=postgres
  -e NEW_DATABASE_NAME=postgres
  -v ~/pgupgrade/pg{{pgversionprev}}olddata:/pgolddata
  -v ~/pgupgrade/pg{{pgversion}}newdata:/pgnewdata
  percona/percona-distribution-postgresql-upgrade:{{dockerupgradetag}}
```

Where:

* `OLD_VERSION` / `NEW_VERSION` are the major versions you're upgrading from and to
* `OLD_DATABASE_NAME` / `NEW_DATABASE_NAME` are the database directory names under your old and new data mounts
* the volumes mount the parent directories (`pg{{pgversionprev}}olddata`, `pg{{pgversion}}newdata`), **not** the `postgres` subdirectory directly

## 9. Start PostgreSQL {{pgversion}} using the upgraded data directory

```{.bash data-prompt="$"}
docker run -d
  --name pg{{pgversion}}
  -e POSTGRES_PASSWORD=password
  -v ~/pgupgrade/pg{{pgversion}}newdata/postgres:/data/db
  percona/percona-distribution-postgresql:{{pgversion}}
```

## 10. Verify PostgreSQL {{pgversion}} starts successfully

```{.bash data-prompt="$"}
docker logs -f pg{{pgversion}}
```

## 11. Connect to the upgraded cluster

```{.bash data-prompt="$"}
docker exec -it pg{{pgversion}} psql -U postgres testdb
```

## 12. Verify the upgraded data

```sql
SELECT version();
SELECT * FROM t1;
```

Once you've confirmed the upgraded container is healthy, you can remove `pg{{pgversionprev}}olddata`.

## Next steps

[Enable `pg_tde` for securing data at rest :material-arrow-right:](docker-enable-pg-tde.md){.md-button}
