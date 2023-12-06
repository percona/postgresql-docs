# Install Percona Distribution for PostgreSQL on Debian and Ubuntu

This document describes how to install Percona Distribution for PostgreSQL from Percona repositories on DEB-based distributions such as Debian and Ubuntu.  [Read more about Percona repositories :material-arrow-top-right:](repo-overview.md).

## Preconditions

1. Debian and other systems that use the apt package manager include the upstream PostgreSQL server package (`postgresql-13`) by default. The components of Percona Distribution for PostgreSQL 13 can only be installed together with the PostgreSQL server shipped by Percona (`percona-postgresql-13`). If you wish to use Percona Distribution for PostgreSQL, uninstall the PostgreSQL package provided by your distribution (`postgresql-13`) and then install the chosen components from Percona Distribution for PostgreSQL.
2. Install `curl` for [Telemetry](telemetry.md). We use it to better understand the use of our products and improve them.

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
   $ sudo percona-release setup ppg-{{pgversion}}
   ```

### Install packages

=== "Install using meta-package"
     
     ```{.bash data-prompt="$"}
     $ sudo apt install percona-ppg-server-{{pgversion}}
     ```

=== "Install packages individually"

     1. Install the PostgreSQL server package:

         ```{.bash data-prompt="$"}
         $ sudo apt install percona-postgresql-{{pgversion}}
         ```

     2. Install the components:

          Install `pg_repack`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-{{pgversion}}-repack
          ```

          Install `pgAudit`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-{{pgversion}}-pgaudit
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
          $ sudo apt install percona-pgaudit{{pgversion}}-set-user
          ```

          Install `pgBadger`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-pgbadger
          ```

          Install `wal2json`:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-{{pgversion}}-wal2json
          ```

          Install PostgreSQL contrib extensions:

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgresql-contrib
          ```

          Install `pgpool2`

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-pgpool2
          ```

          Install `pg_gather`

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-pg-gather
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
    $ sudo su - postgres -c psql
    ```

To exit the `psql` terminal, use the following command:

```{.bash data-prompt="$"}
$ \q
```



