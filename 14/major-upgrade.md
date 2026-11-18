> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/14/llms.txt).

# Upgrading Percona Distribution for PostgreSQL from 13 to 14

This document describes the in-place upgrade of Percona Distribution for PostgreSQL using the `pg_upgrade` tool.

To ensure a smooth upgrade path, follow these steps:

- Upgrade to the latest minor version within your current major version (e.g., from 13.20 to 13.21).
- Then, perform the major upgrade to your desired version (e.g., from 13.21 to 14.18).

Note

When running a major upgrade on **RHEL 8 and compatible derivatives**, consider the following:

Percona Distribution for PostgreSQL 16.3, 15.7, 14.12, 13.15 and 12.18 include `llvm` packages 16.0.6, while its previous versions 16.2, 15.6, 14.11, 13.14, and 12.17 include `llvm` 12.0.1. Since `llvm` libraries differ and are not compatible, the direct major version upgrade from 15.6 to 16.3 may cause issues.

The in-place upgrade means installing a new version without removing the old version and keeping the data files on the server.

See also

[`pg_upgrade` Documentation](https://www.postgresql.org/docs/14/pgupgrade.html)

Similar to installing, we recommend you to upgrade Percona Distribution for PostgreSQL from Percona repositories.

Important

A major upgrade is a risky process because of many changes between versions and issues that might occur during or after the upgrade. Therefore, make sure to back up your data first. The backup tools are out of scope of this document. Use the backup tool of your choice.

The general in-place upgrade flow for Percona Distribution for PostgreSQL is the following:

1. Install Percona Distribution for PostgreSQL 14 packages.
1. Stop the PostgreSQL service.
1. Check the upgrade without modifying the data.
1. Upgrade Percona Distribution for PostgreSQL.
1. Start PostgreSQL service.
1. Execute the **analyze_new_cluster.sh** script to generate statistics so the system is usable.
1. Delete old packages and configuration files.

The exact steps may differ depending on the package manager of your operating system.

## On Debian and Ubuntu using `apt`

Run **all** commands as root or via **sudo**:

1. Install Percona Distribution for PostgreSQL 14 packages.

   Note

   When installing version 14, if prompted via a pop-up to upgrade to the latest available version, select **No**.

   - [Install percona-release :octicons-link-external-14:](https://docs.percona.com/percona-software-repositories/installing.html). If you have installed it before, [update it to the latest version](https://docs.percona.com/percona-software-repositories/updating.html)
   - Enable Percona repository

   ```
   $ sudo percona-release setup ppg-14
   ```

   - Install Percona Distribution for PostgreSQL 14 package

   ```
   $ sudo apt install percona-postgresql-14
   ```

1. Stop the `postgresql` service.

   ```
   $ sudo systemctl stop postgresql.service
   ```

   This stops both Percona Distribution for PostgreSQL 13 and 14.

1. Run the database upgrade.

   - Log in as the `postgres` user

   ```
   $ sudo su postgres
   ```

   - Check if you can upgrade Percona Distribution for PostgreSQL from 13 to 14

   ```
   $ pg_upgradecluster 13 main --check
   # Sample output: pg_upgradecluster pre-upgrade checks ok
   ```

   The `--check` flag here instructs `pg_upgrade` to only check the upgrade without changing any data.

   - Upgrade the Percona Distribution for PostgreSQL

   ```
   $ pg_upgradecluster 13 main
   ```

   Sample output (click to expand)

   ```
   Upgrading cluster 13/main to 14/main ...
   Stopping old cluster...
   Restarting old cluster with restricted connections...
   ...
   Success. Please check that the upgraded cluster works. If it does,
   you can remove the old cluster with:
       pg_dropcluster 13 main

   Ver Cluster Port Status Owner    Data directory              Log file
   14  main    5432 online postgres /var/lib/postgresql/14/main /var/log/postgresql/postgresql-14-main.log

   Sample output:
   Upgrading cluster 13/main to 14/main ...
   Stopping old cluster...
   Restarting old cluster with restricted connections...
   Notice: extra pg_ctl/postgres options given, bypassing systemctl for start operation
   Creating new PostgreSQL cluster 14/main ...
   /usr/lib/postgresql/14/bin/initdb -D /var/lib/postgresql/14/main --auth-local peer --auth-host scram-sha-256 --no-instructions --encoding UTF8 --lc-collate C.UTF-8 --lc-ctype C.UTF-8 --locale-provider libc
   The files belonging to this database system will be owned by user "postgres".
   This user must also own the server process.

   The database cluster will be initialized with locale "C.UTF-8".
   The default text search configuration will be set to "english".

   Data page checksums are disabled.

   fixing permissions on existing directory /var/lib/postgresql/14/main ... ok
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
       pg_dropcluster 13 main

   Ver Cluster Port Status Owner    Data directory              Log file
   13  main    5433 down   postgres /var/lib/postgresql/13/main /var/log/postgresql/postgresql-13-main.log
   Ver Cluster Port Status Owner    Data directory              Log file
   14  main    5432 online postgres /var/lib/postgresql/14/main /var/log/postgresql/postgresql-14-main.log
   ```

1. Start the `postgreqsl` service.

   ```
   $ sudo systemctl start postgresql.service
   ```

1. Check the `postgresql` version.

   - Log in as a postgres user

   ```
   $ sudo su postgres
   ```

   - Check the database version

   ```
   $ psql -c "SELECT version();"
   ```

1. Delete the old cluster’s data files.

   Note

   Before deleting the old cluster, verify that the newly upgraded cluster is fully operational. Keeping the old cluster does not negatively affect the functionality or performance of your upgraded cluster.

   ```
   $ pg_dropcluster 13 main
   ```

## On Red Hat Enterprise Linux and derivatives using `yum`

Run **all** commands as root or via **sudo**:

1. Install Percona Distribution for PostgreSQL 14 packages

   - [Install percona-release](https://docs.percona.com/percona-software-repositories/installing.html)
   - Enable Percona repository:

   ```
   $ sudo percona-release setup ppg-14
   ```

   - Install Percona Distribution for PostgreSQL 14:

   ```
   $ sudo yum install percona-postgresql14-server
   ```

1. Set up Percona Distribution for PostgreSQL 14 cluster

1. Log is as the postgres user

   ```
   sudo su postgres
   ```

1. Set up locale settings

   ```
   export LC_ALL="en_US.UTF-8"
   export LC_CTYPE="en_US.UTF-8"
   ```

1. Initialize cluster with the new data directory

   ```
   $ /usr/pgsql-14/bin/initdb -D /var/lib/pgsql/14/data
   ```

1. Stop the `postgresql` 13 service

   ```
   $ systemctl stop postgresql-13
   ```

1. Run the database upgrade.

   - Log in as the `postgres` user

   ```
   $ sudo su postgres
   ```

   - Check the ability to upgrade Percona Distribution for PostgreSQL from 13 to 14:

   ```
   $ /usr/pgsql-14/bin/pg_upgrade \
   --old-bindir /usr/pgsql-13/bin \
   --new-bindir /usr/pgsql-14/bin  \
   --old-datadir /var/lib/pgsql/13/data \
   --new-datadir /var/lib/pgsql/14/data \
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

   - Upgrade the Percona Distribution for PostgreSQL

   ```
   $ /usr/pgsql-14/bin/pg_upgrade \
   --old-bindir /usr/pgsql-13/bin \
   --new-bindir /usr/pgsql-14/bin  \
   --old-datadir /var/lib/pgsql/13/data \
   --new-datadir /var/lib/pgsql/14/data \
   --link
   ```

   The `--link` flag creates hard links to the files on the old version cluster so you don’t need to copy data. If you don’t wish to use the `--link` option, make sure that you have enough disk space to store 2 copies of files for both old version and new version clusters.

1. Start the `postgresql` 14 service.

   ```
   $ systemctl start postgresql-14
   ```

1. Check `postgresql` status

   ```
   $ systemctl status postgresql-14
   ```

1. After the upgrade, the Optimizer statistics are not transferred to the new cluster. Run the `vaccumdb` command to analyze the new cluster:

   - Log in as the postgres user

   ```
   $ sudo su postgres
   ```

   - Run the `vaccumdb` command

   ```
   $ /usr/pgsql-14/bin/vacuumdb --all --analyze-in-stages
   ```

1. Delete Percona Distribution for PostgreSQL 13 configuration files

   ```
   $ ./delete_old_cluster.sh
   ```

1. Delete Percona Distribution old data files

   ```
   $ rm -rf /var/lib/pgsql/13/data
   ```

Telemetry Agent after upgrading to 14.24 or later

Starting with version 14.24, `percona-pg-telemetry` no longer depends on `percona-telemetry-agent`. If your 13.x installation already has the Telemetry Agent installed, the major upgrade does **not** remove it automatically — it keeps running until you remove it. See [Telemetry Agent dependencies and removal considerations](https://docs.percona.com/postgresql/14/telemetry.html#telemetry-agent-dependencies-and-removal-considerations).

## For major upgrades (RHEL only)

During a major upgrade on RHEL, you may encounter the following error:

```
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.
