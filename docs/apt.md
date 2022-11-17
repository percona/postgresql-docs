# Install Percona Distribution for PostgreSQL on Debian and Ubuntu

This document describes how to install Percona Server for PostgreSQL from Percona repositories on DEB-based distributions such as Debian and Ubuntu.

## Preconditions

Debian and other systems that use the apt package manager include the upstream PostgreSQL server package (`postgresql-11)` by default. The components of Percona Distribution for PostgreSQL 11 can only be installed together with the PostgreSQL server shipped by Percona (`percona-postgresql-11`). If you wish to use Percona Distribution for PostgreSQL, uninstall the upstream `postgresql-11` package and then install the chosen components from Percona Distribution for PostgreSQL.

## Procedure

Run all the commands in the following sections as root or using the `sudo` command:

### Configure Percona repository

1. Install the `percona-release` repository management tool to subscribe to Percona repositories:
 
     * Fetch `percona-release` packages from Percona web:

        ```
        $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
        ```

     * Install the downloaded package with `dpkg`:

        ```
        $ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
        ```

     * Refresh the local cache:

        ```
        $ sudo apt update
        ```

2. Enable the repository

   Percona provides [two repositories](repo-overview.md) for Percona Distribution for PostgreSQL. We recommend enabling the Major release repository to timely receive the latest updates. 

   To enable a repository, we recommend using the `setup` command: 

   ```
   $ sudo percona-release setup ppg-11
   ```

### Install packages

=== "Install using meta-package"
     
     ```
     $ sudo apt install percona-ppg-server
     ```

=== "Install packages individually"

     1. Install the PostgreSQL server package:

         ```
         $ sudo apt install percona-postgresql-11
         ```

     2. Install the components:

          Install `pg_repack`:

          ```
          $ sudo apt install percona-postgresql-11-repack
          ```

          Install `pgAudit`:

          ```
          $ sudo apt install percona-postgresql-11-pgaudit
          ```

          Install `pgBackRest`:

          ```
          $ sudo apt install percona-pgbackrest
          ```

          Install `Patroni`:

          ```
          $ sudo apt install percona-patroni
          ```

          [Install `pg_stat_monitor`](pg-stat-monitor.md)


          Install `pgBouncer`:

          ```
          $ sudo apt install percona-pgbouncer
          ```

          Install `pgAudit-set_user`:

          ```
          $ sudo apt install percona-pgaudit15-set-user
          ```

          Install `pgBadger`:

          ```
          $ sudo apt install percona-pgbadger
          ```

          Install `wal2json`:

          ```
          $ sudo apt install percona-postgresql-11-wal2json
          ```

          Install PostgreSQL contrib extensions:

          ```
          $ sudo apt install percona-postgresql-contrib
          ```

          Install HAProxy

          ```
          $ sudo apt install percona-haproxy
          ```
          
          Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](enable-extensions.md).

### Start the service

The installation process automatically initializes and starts the default database. You can check the database status using the following command:

```
$ sudo systemctl status postgresql.service
```

### Connect to the PostgreSQL server

By default, `postgres` user and `postgres` database are created in PostgreSQL upon its installation and initialization. This allows you to connect to the database as the `postgres` user.

```
$ sudo su postgres
```

Open the PostgreSQL interactive terminal:

```
$ psql
```

!!! hint

    You can connect to `psql` as the `postgres` user in one go:

    ```
    $ sudo su postgres psql
    ```

To exit the `psql` terminal, use the following command:

```
$ \q
```



