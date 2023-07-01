# Install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux and derivatives

This document describes how to install Percona Distribution for PostgreSQL from Percona repositories on RPM-based distributions such as Red Hat Enterprise Linux and compatible derivatives.

## Platform specific notes

If you intend to install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux v8, disable the ``postgresql``  and ``llvm-toolset``modules:

```{.bash data-prompt="$"}
$ sudo dnf module disable postgresql llvm-toolset rust-toolset
```

On CentOS 7, you should install the ``epel-release`` package:

```{.bash data-prompt="$"}
$ sudo yum -y install epel-release
$ sudo yum repolist
```

## Procedure

Run all the commands in the following sections as root or using the `sudo` command:

### Configure the repository

1. Install the `percona-release` repository management tool to subscribe to Percona repositories:

    ```{.bash data-prompt="$"}
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

2. Enable the repository

   Percona provides [two repositories](repo-overview.md) for Percona Distribution for PostgreSQL. We recommend enabling the Major release repository to timely receive the latest updates. The Minor repository should only be used if you need to standardize on a minor release, but be aware you may miss some critical updates in later versions. 

   To enable a repository, we recommend using the `setup` command: 

   ```{.bash data-prompt="$"}
   $ sudo percona-release setup ppg-15
   ```

### Install packages

=== "Install using meta-package"
     
     ```{.bash data-prompt="$"}
     $ sudo yum install percona-ppg-server15
     ```

=== "Install packages individually"

     1. Install the PostgreSQL server package:

         ```{.bash data-prompt="$"}
         $ sudo yum install percona-postgresql15-server
         ```

     2. Install the components:

        Install `pg_repack`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pg_repack15
        ```

        Install `pgaudit`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgaudit
        ```

        Install `pgBackRest`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbackrest
        ```

        Install `Patroni`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-patroni
        ```

        [Install `pg_stat_monitor`](pg-stat-monitor.md):


        Install `pgBouncer`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbouncer
        ```

        Install `pgAudit-set_user`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgaudit15_set_user
        ```

        Install `pgBadger`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbadger
        ```

        Install `wal2json`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-wal2json15
        ```

        Install PostgreSQL contrib extensions:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-postgresql15-contrib
        ```

        Install HAProxy
        
        ```{.bash data-prompt="$"}
        $ sudo yum install percona-haproxy
        ```
        
        Install pgpool

        To install `pgpool2` on Red Hat Enterprise Linux and compatible derivatives, enable the codeready builder repository first to resolve dependencies conflict for `pgpool2`. The following examples show steps for Red Hat Enterprise Linux 9. 

        === "RHEL 9"

            1. Enable the codeready builder repository

                ```{.bash data-prompt="$"}
                $ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-9-x86_64-rpms
                ```

            2. Install the extension

                ```{.bash data-prompt="$"}
                $ sudo yum install percona-pgpool-II-pg15
                ```

        === "CentOS 9"

            1. Enable the codeready builder repository

                ```{.bash data-prompt="$"}
                $ sudo dnf config-manager --set-enabled crb
                ```

            2. Install the extension

                ```{.bash data-prompt="$"}
                $ sudo yum install percona-pgpool-II-pg15
                ```

        === "Oracle Linux 9"

            1. Enable the codeready builder repository

                ```{.bash data-prompt="$"}
                $ sudo dnf config-manager --set-enabled ol9_codeready_builder
                ```

            2. Install the extension

                ```{.bash data-prompt="$"}
                $ sudo yum install percona-pgpool-II-pg15
                ```

        For Red Hat Enterprise Linux 8, replace the operating system version in the commands accordingly.


        Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](enable-extensions.md).

### Start the service

After the installation, the default database storage is not automatically initialized. To complete the installation and start Percona Distribution for PostgreSQL, initialize the database using the following command:

```{.bash data-prompt="$"}
$ /usr/pgsql-15/bin/postgresql-15-setup initdb
```

Start the PostgreSQL service:

```{.bash data-prompt="$"}
$ sudo systemctl start postgresql-15
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
