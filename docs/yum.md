# Install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux and derivatives

This document describes how to install Percona Server for PostgreSQL from Percona repositories on RPM-based distributions such as Red Hat Enterprise Linux and compatible derivatives..

## Platform Specific Notes

If you intend to install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux v8, disable the ``postgresql``  and ``llvm-toolset``modules:

```
$ sudo dnf module disable postgresql llvm-toolset
```

On CentOS 7, you should install the ``epel-release`` package:

```
$ sudo yum -y install epel-release
$ sudo yum repolist
```

## Procedure

Run all the commands in the following sections as root or using the `sudo` command:

### Configure the repository

1. Install the `percona-release` repository management tool to subscribe to Percona repositories:

    ```
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

2. Enable the repository

   Percona provides [two repositories](repo-overview.md) for Percona Distribution for PostgreSQL. We recommend enabling the Major release repository to timely receive the latest updates. 

   To enable a repository, we recommend using the `setup` command: 

   ```
   $ sudo percona-release setup ppg-13
   ```

### Install packages

=== "Install using meta-package"
     
     ```
     $ sudo yum install percona-ppg-server
     ```

=== "Install packages individually"

     1. Install the PostgreSQL server package:

         ```
         $ sudo yum install percona-postgresql13-server
         ```

     2. Install the components:

        Install `pg_repack`:

        ```
        $ sudo yum install percona-pg_repack13
        ```

        Install `pgaudit`:

        ```
        $ sudo yum install percona-pgaudit
        ```

        Install `pgBackRest`:

        ```
        $ sudo yum install percona-pgbackrest
        ```

        Install `Patroni`:

        ```
        $ sudo yum install percona-patroni
        ```

        [Install `pg_stat_monitor`](pg-stat-monitor.md):


        Install `pgBouncer`:

        ```
        $ sudo yum install percona-pgbouncer
        ```

        Install `pgAudit-set_user`:

        ```
        $ sudo yum install percona-pgaudit13_set_user
        ```

        Install `pgBadger`:

        ```
        $ sudo yum install percona-pgbadger
        ```

        Install `wal2json`:

        ```
        $ sudo yum install percona-wal2json13
        ```

        Install PostgreSQL contrib extensions:

        ```
        $ sudo yum install percona-postgresql15-contrib
        ```

        Install HAProxy
        
        ```
        $ sudo yum install percona-haproxy
        ```

        Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](enable-extensions.md).

### Start the service

After the installation, the default database storage is not automatically initialized. To complete the installation and start Percona Distribution for PostgreSQL, initialize the database using the following command:

```
/usr/pgsql-13/bin/postgresql-13-setup initdb
```

Start the PostgreSQL service:

```
$ sudo systemctl start postgresql-13
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
