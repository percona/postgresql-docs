# Upgrading Percona Distribution for PostgreSQL from 14 to 15

This document describes the in-place upgrade of Percona Distribution for PostgreSQL using the `pg_upgrade` tool.

To ensure a smooth upgrade path, follow these steps:

* Upgrade to the latest minor version within your current major version (e.g., from 14.17 to 14.18).
* Then, perform the major upgrade to your desired version (e.g., from 14.18 to 15.13).

!!! note

    When running a major upgrade on **RHEL 8 and compatible derivatives**, consider the following:

    Percona Distribution for PostgreSQL 16.3, 15.7, 14.12, 13.15 and 12.18 include `llvm` packages 16.0.6, while its previous versions 16.2, 15.6, 14.11, 13.14, and 12.17 include `llvm` 12.0.1. Since `llvm` libraries differ and are not compatible, the direct major version upgrade from 15.6 to 16.3 may cause issues. 

The in-place upgrade means installing a new version without removing the old version and keeping the data files on the server.

!!! admonition "See also"

    [`pg_upgrade` Documentation](https://www.postgresql.org/docs/15/pgupgrade.html)

Similar to installing, we recommend you to upgrade Percona Distribution for PostgreSQL from Percona repositories.

!!! important

    A major upgrade is a risky process because of many changes between versions and issues that might occur during or after the upgrade. Therefore, make sure to back up your data first. The backup tools are out of scope of this document. Use the backup tool of your choice.

The general in-place upgrade flow for Percona Distribution for PostgreSQL is the following:

1. Install Percona Distribution for PostgreSQL 15 packages.

2. Stop the PostgreSQL service.

3. Check the upgrade without modifying the data.

4. Upgrade Percona Distribution for PostgreSQL.

5. Start PostgreSQL service.

6. Execute the  **analyze_new_cluster.sh** script to generate statistics
so the system is usable.

7. Delete old packages and configuration files.

The exact steps may differ depending on the package manager of your operating system.

## On Debian and Ubuntu using `apt`

Run **all** commands as root or via **sudo**:
{.power-number}

1. Install Percona Distribution for PostgreSQL 15 packages.

    !!! note
        When installing version 15, if prompted via a pop-up to upgrade to the latest available version, select **No**.

    * [Install percona-release :octicons-link-external-15:](https://docs.percona.com/percona-software-repositories/installing.html). If you have installed it before, [update it to the latest version](https://docs.percona.com/percona-software-repositories/updating.html)

    * Enable Percona repository

      ```{.bash data-prompt="$"}
      $ sudo percona-release setup ppg-15
      ```

    * Install Percona Distribution for PostgreSQL 15 package

      ```{.bash data-prompt="$"}
      $ sudo apt install percona-postgresql-15
      ```

2. Stop the `postgresql` service.

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop postgresql.service
    ```

    This stops both Percona Distribution for PostgreSQL 14 and 15.

3. Run the database upgrade.

    * Log in as the `postgres` user

    ```{.bash data-prompt="$"}
    $ sudo su postgres
    ```

    * Check if you can upgrade Percona Distribution for PostgreSQL from 14 to 15

    ```{.bash data-prompt="$"}
    $ pg_upgradecluster 14 main --check
    # Sample output: pg_upgradecluster pre-upgrade checks ok
    ```

    The `--check` flag here instructs `pg_upgrade` to only check the upgrade without changing any data.

    * Upgrade the Percona Distribution for PostgreSQL

    ```{.bash data-prompt="$"}
    $ pg_upgradecluster 14 main
    ```

      <details>
        <summary>Sample output (click to expand)</summary>
        ```bash
        Upgrading cluster 14/main to 15/main ...
        Stopping old cluster...
        Restarting old cluster with restricted connections...
        ...
        Success. Please check that the upgraded cluster works. If it does,
        you can remove the old cluster with:
            pg_dropcluster 14 main

        Ver Cluster Port Status Owner    Data directory              Log file
        15  main    5432 online postgres /var/lib/postgresql/15/main /var/log/postgresql/postgresql-15-main.log

        Sample output:
        Upgrading cluster 14/main to 15/main ...
        Stopping old cluster...
        Restarting old cluster with restricted connections...
        Notice: extra pg_ctl/postgres options given, bypassing systemctl for start operation
        Creating new PostgreSQL cluster 15/main ...
        /usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/15/main --auth-local peer --auth-host scram-sha-256 --no-instructions --encoding UTF8 --lc-collate C.UTF-8 --lc-ctype C.UTF-8 --locale-provider libc
        The files belonging to this database system will be owned by user "postgres".
        This user must also own the server process.

        The database cluster will be initialized with locale "C.UTF-8".
        The default text search configuration will be set to "english".

        Data page checksums are disabled.

        fixing permissions on existing directory /var/lib/postgresql/15/main ... ok
        creating subdirectories ... ok
        selecting dynamic shared memory implementation ... posix
        selecting default max_connections ... 100
        selecting default shared_buffers ... 128MB
        selecting default time zone ... Etc/UTC
        creating configuration files ... ok
        running bootstrap script ... ok
        performing post-bootstrap initialization ... ok
        syncing data to disk ... ok

        Copying old configuration files...
        Copying old start.conf...
        Copying old pg_ctl.conf...
        Starting new cluster...
        Notice: extra pg_ctl/postgres options given, bypassing systemctl for start operation
        Running init phase upgrade hook scripts ...

        Roles, databases, schemas, ACLs...
        set_config
        ------------

        (1 row)

        set_config
        ------------

        (1 row)

        Fixing hardcoded library paths for stored procedures...
        Upgrading database template1...
        Fixing hardcoded library paths for stored procedures...
        Upgrading database postgres...
        Stopping target cluster...
        Stopping old cluster...
        Disabling automatic startup of old cluster...
        Starting upgraded cluster on port 5432...
        Running finish phase upgrade hook scripts ...
        vacuumdb: processing database "postgres": Generating minimal optimizer statistics (1 target)
        vacuumdb: processing database "template1": Generating minimal optimizer statistics (1 target)
        vacuumdb: processing database "postgres": Generating medium optimizer statistics (10 targets)
        vacuumdb: processing database "template1": Generating medium optimizer statistics (10 targets)
        vacuumdb: processing database "postgres": Generating default (full) optimizer statistics
        vacuumdb: processing database "template1": Generating default (full) optimizer statistics

        Success. Please check that the upgraded cluster works. If it does,
        you can remove the old cluster with
            pg_dropcluster 14 main

        Ver Cluster Port Status Owner    Data directory              Log file
        14  main    5433 down   postgres /var/lib/postgresql/14/main /var/log/postgresql/postgresql-14-main.log
        Ver Cluster Port Status Owner    Data directory              Log file
        15  main    5432 online postgres /var/lib/postgresql/15/main /var/log/postgresql/postgresql-15-main.log
        ```
      </details>

4. Start the `postgreqsl` service.

    ```{.bash data-prompt="$"}
    $ sudo systemctl start postgresql.service
    ```

5. Check the `postgresql` version.

    * Log in as a postgres user

       ```{.bash data-prompt="$"}
       $ sudo su postgres
       ```

    * Check the database version

       ```{.bash data-prompt="$"}
       $ psql -c "SELECT version();"
       ```

6. Delete the old cluster's data files.

    !!! note
        Before deleting the old cluster, verify that the newly upgraded cluster is fully operational. Keeping the old cluster does not negatively affect the functionality or performance of your upgraded cluster.

    ```{.bash data-prompt="$"}
    $ pg_dropcluster 14 main
    ```

## On Red Hat Enterprise Linux and CentOS using `yum`

Run **all** commands as root or via **sudo**:
{.power-number}

1. Install Percona Distribution for PostgreSQL 15 packages

    * [Install percona-release :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/installing.html)

    * Enable Percona repository:

       ```{.bash data-prompt="$"}
       $ sudo percona-release setup ppg-15
       ```

    * Install Percona Distribution for PostgreSQL 15:

       ```{.bash data-prompt="$"}
       $ sudo yum install percona-postgresql15-server
       ```

2. Set up Percona Distribution for PostgreSQL 15 cluster

   * Log is as the postgres user

      ```{.bash data-prompt="$"}
      $ sudo su postgres
      ```

   * Set up locale settings

      ```
      export LC_ALL="en_US.UTF-8"
      export LC_CTYPE="en_US.UTF-8"
      ```

   * Initialize cluster with the new data directory

      ```{.bash data-prompt="$"}
      $ /usr/pgsql-15/bin/initdb -D /var/lib/pgsql/15/data
      ```

3. Stop the `postgresql` 14 service

    ```{.bash data-prompt="$"}
    $ systemctl stop postgresql-14
    ```

4. Run the database upgrade.

    * Log in as the `postgres` user

       ```{.bash data-prompt="$"}
       $ sudo su postgres
       ```

    * Check the ability to upgrade Percona Distribution for PostgreSQL from 14 to 15:

       ```{.bash data-prompt="$"}
       $ /usr/pgsql-15/bin/pg_upgrade \
       --old-bindir /usr/pgsql-14/bin \
       --new-bindir /usr/pgsql-15/bin  \
       --old-datadir /var/lib/pgsql/14/data \
       --new-datadir /var/lib/pgsql/15/data \
       --check
       ```

       The `--check` flag here instructs `pg_upgrade` to only check the upgrade without changing any data.

       **Sample output**

       ```
       Performing Consistency Checks
       -----------------------------
       Checking cluster versions                                   ok
       Checking database user is the install user                  ok
       Checking database connection settings                       ok
       Checking for prepared transactions                          ok
       Checking for reg* data types in user tables                 ok
       Checking for contrib/isn with bigint-passing mismatch       ok
       Checking for tables WITH OIDS                               ok
       Checking for invalid "sql_identifier" user columns          ok
       Checking for presence of required libraries                 ok
       Checking database user is the install user                  ok
       Checking for prepared transactions                          ok

       *Clusters are compatible*
       ```

    * Upgrade the Percona Distribution for PostgreSQL

       ```{.bash data-prompt="$"}
       $ /usr/pgsql-15/bin/pg_upgrade \
       --old-bindir /usr/pgsql-14/bin \
       --new-bindir /usr/pgsql-15/bin  \
       --old-datadir /var/lib/pgsql/14/data \
       --new-datadir /var/lib/pgsql/15/data \
       --link 
       ```

       The  `--link` flag creates hard links to the files on the old version cluster so you don’t need to copy data.
       If you don’t wish to use the `--link` option, make sure that you have enough disk space to store 2 copies of files for both old version and new version clusters.

5. Start the `postgresql` 15 service.

    ```{.bash data-prompt="$"}
    $ systemctl start postgresql-15
    ```

6. Check postgresql status

    ```{.bash data-prompt="$"}
    $ systemctl status postgresql-15
    ```

7. After the upgrade, the Optimizer statistics are not transferred to the new cluster. Run the `vaccumdb` command to analyze the new cluster:

    * Log in as the postgres user

       ```{.bash data-prompt="$"}
       $ sudo su postgres
       ```

    * Run the `vaccumdb` command

       ```{.bash data-prompt="$"}
       $ /usr/pgsql-15/bin/vacuumdb --all --analyze-in-stages
       ```

8. Delete Percona Distribution for PostgreSQL 14 configuration files

    ```{.bash data-prompt="$"}
    $ ./delete_old_cluster.sh
    ```

9. Delete Percona Distribution for PostgreSQL old data files

    ```{.bash data-prompt="$"}
    $ rm -rf /var/lib/pgsql/14/data
    ```

!!! note "Telemetry Agent after upgrading to 15.19 or later"

    Starting with version 15.19, `percona-pg-telemetry` no longer depends on `percona-telemetry-agent`. If your 14.x installation already has the Telemetry Agent installed, the major upgrade does **not** remove it automatically — it keeps running until you remove it. See [Telemetry Agent dependencies and removal considerations](telemetry.md#telemetry-agent-dependencies-and-removal-considerations).

## For major upgrades (RHEL only)

During a major upgrade on RHEL, you may encounter the following error:

```
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.
