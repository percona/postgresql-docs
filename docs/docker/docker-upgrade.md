# Upgrade Percona Distribution for PostgreSQL

To upgrade Percona Distribution for PostgreSQL in Docker to a new major version, use the dedicated `percona/percona-distribution-postgresql-upgrade` image. It bundles the server binaries for several consecutive major versions, so `pg_upgrade` can run against your old and new data directories.

!!! important
    Back up your data before you start. The backup tool is out of scope for this document. Use the backup tool of your choice.

!!! warning
    If your cluster uses `pg_tde`, do not follow these steps. Using `pg_upgrade` on an encrypted cluster is not supported and will result in data corruption. See [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md) for details.

1. Stop the running container:

    ```{.bash data-prompt="$"}t
    docker stop container-name
    ```

2. Pull the upgrade image tag that covers your source and target versions. The tags encode all bundled versions, for example `18.4-17.10-16.14-15.18-14.23-1` bundles Percona PostgreSQL 14 through 18:

    ```{.bash data-prompt="$"}
    docker pull percona/percona-distribution-postgresql-upgrade: upgrade-tag
    ```

3. Run the upgrade container, mount your existing data volume as the old data directory and an empty volume as the new one:

    ```{.bash data-prompt="$"}
    TO BE ADDED
    ```

4. Start a new container on the target version, using `name of new data vol (TBD)` as its data directory:

    ```{.bash data-prompt="$"}
    docker run --name container-name \
      -v new-data-volume:/var/lib/postgresql/data \
      -d percona/percona-distribution-postgresql:{{dockertag}}
    ```
