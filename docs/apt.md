# Install Percona Distribution for PostgreSQL on Debian and Ubuntu

This document describes how to install Percona Server for PostgreSQL from Percona repositories on DEB-based distributions such as Debian and Ubuntu.

## Preconditions

Debian and other systems that use the apt package manager include the upstream PostgreSQL server package (`postgresql-12`) by default. The components of Percona Distribution for PostgreSQL 12 can only be installed together with the PostgreSQL server shipped by Percona (`percona-postgresql-12`). If you wish to use Percona Distribution for PostgreSQL, uninstall the `postgresql-12` and then install the chosen components from Percona Distribution for PostgreSQL.

## Procedure

Run all the commands in the following sections as root or using the `sudo` command:

### Configure Percona repository

1. Install the `percona-release` repository management tool to subscribe to Percona repositories:
 
     * Fetch `percona-release` packages from Percona web:

        ```{.bash data-prompt="$"}
        $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
        ```

     * Install the downloaded package with `dpkg`:

        ```{.bash data-prompt="$"}
        $ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
        ```

     * Refresh the local cache:

        ```{.bash data-prompt="$"}
        $ sudo apt update
        ```

2. Enable the repository

   Percona provides [two repositories](repo-overview.md) for Percona Distribution for PostgreSQL. We recommend enabling the Major release repository to timely receive the latest updates. 

   To enable a repository, we recommend using the `setup` command: 

   ```{.bash data-prompt="$"}
   $ sudo percona-release setup ppg-12
   ```

### Install packages

=== "Install using meta-package"
     
     ```{.bash data-prompt="$"}
     $ sudo apt install percona-ppg-server-12
     ```

=== "Install packages individually"

     1. Install the PostgreSQL server package:

         ```{.bash data-prompt="$"}
         $ sudo apt install percona-postgresql-12
         ```

     2. Install the components:

          Install `pg_repack`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-12-repack
          ```

          Install `pgAudit`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-12-pgaudit
          ```

          Install `pgBackRest`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-pgbackrest
          ```

          Install `Patroni`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-patroni
          ```

          [Install `pg_stat_monitor`](pg-stat-monitor.md)


          Install `pgBouncer`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-pgbouncer
          ```

          Install `pgAudit-set_user`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-pgaudit12-set-user
          ```

          Install `pgBadger`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-pgbadger
          ```

          Install `wal2json`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-12-wal2json
          ```

          Install PostgreSQL contrib extensions:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-contrib
          ```

          Install HAProxy

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-haproxy
          ```
          
          Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](enable-extensions.md).

### Start the service

The installation process automatically initializes and starts the default database. You can check the database status using the following command:

```{.bash data-prompt="$"}
$ sudo systemctl status postgresql.service
```

### Connect to the PostgreSQL server

By default, `postgres` user and `postgres` database are created in PostgreSQL upon its installation and initialization. This allows you to connect to the database as the `postgres` user.

```{.bash data-prompt="$"}
$ sudo su postgres
```

Open the PostgreSQL interactive terminal:

```{.bash data-prompt="$"}
$ psql
```

!!! hint

    You can connect to `psql` as the `postgres` user in one go:

    ```{.bash data-prompt="$"}
    $ sudo su postgres psql
    ```

To exit the `psql` terminal, use the following command:

```{.bash data-prompt="$"}
$ \q
```



