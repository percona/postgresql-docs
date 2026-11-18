> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/17/llms.txt).

# Install Percona Distribution for PostgreSQL on Debian and Ubuntu

This document describes how to install Percona Server for PostgreSQL from Percona repositories on DEB-based distributions such as Debian and Ubuntu. [Read more about Percona repositories](https://docs.percona.com/postgresql/17/repo-overview.html).

## Preconditions

1. Debian and other systems that use the `apt` package manager include the upstream PostgreSQL server package `postgresql-17` by default. The components of Percona Distribution for PostgreSQL 17 can only be installed together with Percona Server for PostgreSQL (`percona-postgresql-17`). If you wish to use Percona Distribution for PostgreSQL, uninstall the `postgresql-17` package provided by your distribution and then install the chosen components from Percona Distribution for PostgreSQL.

1. Install `curl` for [Telemetry](https://docs.percona.com/postgresql/17/telemetry.html). We use it to better understand the use of our products and improve them. To install `curl`, run the following command:

   ```
   $ sudo apt install curl
   ```

## Procedure

Run all the commands in the following sections as root or using the `sudo` command:

### Configure Percona repository

1. Install the `percona-release` repository management tool to subscribe to Percona repositories:

   - Fetch `percona-release` packages from Percona web:

     ```
     $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
     ```

   - Install the downloaded package with `dpkg`:

     ```
     $ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
     ```

   - Refresh the local cache:

     ```
     $ sudo apt update
     ```

1. Enable the repository

Percona provides [two repositories](https://docs.percona.com/postgresql/17/repo-overview.html) for Percona Distribution for PostgreSQL. We recommend enabling the Major release repository to timely receive the latest updates.

```
$ sudo percona-release setup ppg-17
```

### Install packages individually

Run the following commands:

1. Install the PostgreSQL server package:

   ```
   $ sudo apt install percona-postgresql-17
   ```

1. Install the components:

   Install `pg_repack`:

   ```
   $ sudo apt install percona-postgresql-17-repack
   ```

   Install `pgAudit`:

   ```
   $ sudo apt install percona-postgresql-17-pgaudit
   ```

   Install `pgBackRest`:

   ```
   $ sudo apt install percona-pgbackrest
   ```

   Install `Patroni`:

   ```
   $ sudo apt install percona-patroni
   ```

   [Install `pg_stat_monitor`](https://docs.percona.com/pg-stat-monitor/install.html#__tabbed_1_1)

   Install `pgBouncer`:

   ```
   $ sudo apt install percona-pgbouncer
   ```

   Install `pgAudit-set_user`:

   ```
   $ sudo apt install percona-pgaudit17-set-user
   ```

   Install `pgBadger`:

   ```
   $ sudo apt install percona-pgbadger
   ```

   Install `wal2json`:

   ```
   $ sudo apt install percona-postgresql-17-wal2json
   ```

   Install PostgreSQL contrib extensions:

   ```
   $ sudo apt install percona-postgresql-contrib
   ```

   Install HAProxy

   ```
   $ sudo apt install percona-haproxy
   ```

   Install pgpool2

   ```
   $ sudo apt install percona-pgpool2
   ```

   Install `pg_gather`

   ```
   $ sudo apt install percona-pg-gather
   ```

   Install `pgvector`

   ```
   $ sudo apt install percona-postgresql-17-pgvector
   ```

   Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](https://docs.percona.com/postgresql/17/enable-extensions.html).

### Start the service

The installation process automatically initializes and starts the default database. You can check the database status using the following command:

```
$ sudo systemctl status postgresql.service
```

Check the Percona Distribution for PostgreSQL version:

```
$ psql --version
```

Sample output

```
psql (PostgreSQL) 17.12.1 (Percona Server for PostgreSQL) 17.12.1
```

Congratulations! Your Percona Distribution for PostgreSQL is up and running.

## Next steps

[Enable extensions](https://docs.percona.com/postgresql/17/enable-extensions.html)

[Connect to PostgreSQL](https://docs.percona.com/postgresql/17/connect.html)
