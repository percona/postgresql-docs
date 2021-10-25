# Installing Percona Distribution for PostgreSQL

Percona provides installation packages in `DEB` and `RPM` format for 64-bit Linux distributions. Find the full list of supported platforms on the [Percona Software and Platform Lifecycle page](https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql).

Like many other Percona products, we recommend installing Percona Distribution for PostgreSQL from Percona repositories by using the **percona-release** utility. The **percona-release** utility automatically enables the required repository for you so you can easily install and update Percona Distribution for PostgreSQL packages and their dependencies through the package manager of your operating system.

The installation process includes the following steps:


1. Install **percona-release**


2. Enable the repository


3. Install the packages


4. Start the `postgresql` service


5. Connect to the server

## Repositories overview

There are two repositories available for Percona Distribution for PostgreSQL. We recommend installing Percona Distribution for PostgreSQL  from the *Major Release repository* (e.g. `ppg-11`) as it includes the latest version packages. Whenever a package is updated, the package manager of your operating system detects that and prompts you to update. As long as you update all Distribution packages at the same time, you can ensure that the packages you’re using have been tested and verified by Percona.

The *Minor Release repository* includes a particular minor release of the database and all the packages that were tested and verified to work with that minor release (e.g. `ppg-11.8`). You may choose to install Percona Distribution for PostgreSQL from the Minor Release repository if you have decided to standardize on a particular release which has passed rigorous testing procedures and which has been verified to work with your applications. This allows you to deploy to a new host and ensure that you’ll be using the same version of all the Distribution packages, even if newer releases exist in other repositories.

The disadvantage of using a Minor Release repository is that you are locked in this particular release. When potentially critical fixes are released in a later minor version of the database, you will not be prompted for an upgrade by the package manager of your operating system. You would need to change the configured repository in order to install the upgrade.

## Install **percona-release**

[Install **percona-release**](https://www.percona.com/doc/percona-repo-config/installing.html) utility. If you have installed it before, [update](https://www.percona.com/doc/percona-repo-config/updating.html) it to the latest version.

## Enable the repository

As soon as **percona-release** is installed or up-to-date, enable the repository for Percona Distribution for PostgreSQL (`ppg-11`). We recommend using the *setup* command as it enables the specified repository and updates the platform’s package manager database.

To install the *latest* version of Percona Distribution for PostgreSQL, enable the Major release repository using the following command:

```
$ sudo percona-release setup ppg-11
```

To install a *specific minor version* of Percona Distribution for PostgreSQL, enable the Minor release repository. For example, to install Percona Distribution for PostgreSQL 11.10, enable the `ppg-11.10`  repository using the following command:

```
$ sudo percona-release setup ppg-11.10
```

## Install Percona Distribution for PostgreSQL packages

After you’ve [installed percona-release](#install-percona-release) and [enabled the desired repository](#enable-the-repository), install Percona Distribution for PostgreSQL using the commands of your package manager (the procedure differs
depending on the package manager of your operating system).

!!! important
   
    Run all the commands in the following sections as root or using the **sudo** command.

### On Debian and Ubuntu using `apt`

!!! note

    On Debian and other systems that use the `apt` package manager, such as Ubuntu, components of Percona Distribution for PostgreSQL 11 can only be installed together with the server shipped by Percona (percona-postgresql-11). If you wish to use Percona Distribution for PostgreSQL, uninstall the PostgreSQL package provided by your distribution (postgresql-11) and then install the chosen components from Percona Distribution for PostgreSQL.



Install the **percona-postgresql-11** package using the following command.

```
$ sudo apt install percona-postgresql-11
```

Note that this package will not install the components. Use the following commands to install components’ packages:

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

Install `pg_stat_monitor`:

```
$ sudo apt install percona-pg-stat-monitor11
```

!!! note
   
    You need to set up `pg_stat_monitor` in order to use it with Percona Distribution for PostgreSQL. Refer to [Setup](pg-stat-monitor.md#setup) for configuration guidelines.

Install `PgBouncer`:

```
$ sudo apt install percona-pgbouncer
```

Install `pgAudit-set_user`:

```
$ sudo apt install percona-pgaudit11-set-user
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

Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](#enabling-extensions).

####Starting the service

The installation process automatically initializes the default database. Thus, to start Percona Distribution for PostgreSQL, use the following command:

```
$ sudo pg_ctlcluster 11 main start
```

Next steps: [connect to PostgreSQL](#connect-to-the-postgresql-server).

### On Red Hat Enterprise Linux and CentOS using `yum`

####Platform Specific Notes


>If you intend to install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux v8 / CentOS 8, disable the ``postgresql``  and ``llvm-toolset``modules:


>```
>$ sudo dnf module disable postgresql llvm-toolset
>```


>On CentOS 7, you should install the ``epel-release`` package:


>```
>$ sudo yum -y install epel-release
>$ sudo yum repolist
>```

Install the **percona-postgresql-11** package using **yum install**.

```
$ sudo yum install percona-postgresql11-server
```

Note that this package will not install the components. Use the following commands to install components’ packages:

Install `pg_repack`:

```
$ sudo yum install percona-pg_repack11
```

Install `pgAudit`:

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

Install `pg_stat_monitor`:

```
$ sudo yum install percona-pg-stat-monitor11
```

!!! note

    You need to set up `pg_stat_monitor` in order to use it with Percona Distribution for PostgreSQL. Refer to [Setup](pg-stat-monitor.md#setup) for configuration guidelines.

Install `PgBouncer`:

```
$ sudo yum install percona-pgbouncer
```

Install `pgAudit-set_user`:

```
$ sudo yum install percona-pgaudit11_set_user
```

Install `pgBadger`:

```
$ sudo yum install percona-pgbadger
```

Install `wal2json`:

```
$ sudo yum install percona-wal2json11
```

Install PostgreSQL contrib extensions:

```
$ sudo yum install percona-postgresql11-contrib
```

Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](#enabling-extensions).

####Starting the service

After the installation, the default database storage is not automatically initialized. To complete the installation and start Percona Distribution for PostgreSQL, initialize the database using the following command:

```
/usr/pgsql-11/bin/postgresql-11-setup initdb
```

Start the PostgreSQL service:

```
$ sudo systemctl start postgresql-11
```

## Enabling extensions

Some extensions require additional configuration before using them with |pdp|. This section provides configuration instructions per extension.

**Patroni**

While setting up a high availability PostgreSQL cluster with Patroni, you will need the following:

- Configure Patroni on every ``postresql`` instance. The configuration file is supplied with `percona-patroni` package and is available at the following path:

    - `/etc/postgresql.yml` for Debian and Ubuntu
    - `/usr/share/doc/percona-patroni/postgres0.yml` for Red Hat Enterprise Linux and CentOS

- Install and configure Distributed Configuration Store (DCS). Patroni supports such DCSs as ETCD, zookeeper, Kubernetes though [ETCD](https://etcd.io/) is the most popular one. It is available upstream as DEB packages for Debian 10 and Ubuntu 18.04, 20.04.  

     For Debian 9 ("stretch"), a DEB package for ETCD is available within Percona Distribution for PostreSQL.  You can install it using the following command: 

     ```
     $ apt install etcd
     ```

     For CentOS 8, RPM packages for ETCD is available within Percona Distribution for PostreSQL.  You can install it using the following command: 

     ```
     $ yum install etcd python3-python-etcd
     
     ```
  
- Install and configure [HAProxy](http://www.haproxy.org/).

!!! seealso

    - [Patroni documentation](https://patroni.readthedocs.io/en/latest/SETTINGS.html#settings)

    - Percona Blog: 

        - [PostgreSQL HA with Patroni: Your Turn to Test Failure Scenarios](https://www.percona.com/blog/2021/06/11/postgresql-ha-with-patroni-your-turn-to-test-failure-scenarios/) 

**pgBadger**

Enable the following options in `postgresql.conf` configuration file before starting the service:

```
log_min_duration_statement = 0
log_line_prefix = '%t [%p]: '
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

For details about each option, see [pdBadger documentation](https://github.com/darold/pgbadger/#POSTGRESQL-CONFIGURATION>).

**pgAudit set-user**

Add the `set-user` to `shared_preload_libraries` in `postgresql.conf`. The recommended way is to  use the [ALTER SYSTEM](https://www.postgresql.org/docs/11/sql-altersystem.html) command. [Connect to psql](#connect-to-the-postgresql-server) and use the following command:

```
$ ALTER SYSTEM SET shared_preload_libraries = 'set-user';
```

Start/restart the server to apply the configuration.

You can fine-tune user behavior with the [custom parameters](https://github.com/pgaudit/set_user#configuration-options) supplied with the extension.

**wal2json**

After the installation, enable the following option in `postgresql.conf` configuration file before starting the service:

```
wal_level = logical
```


## Connect to the PostgreSQL server

By default, `postgres` user and `postgres` database are created in PostgreSQL upon its installation and initialization. This allows you to connect to the database as the `postgres` user.

```
$ sudo su postgres
```

Open the PostgreSQL interactive terminal:

```
$ psql
```

To exit the `psql` terminal, use the following command:

```
$ \q
```

!!! hint

    You can connect to psql as the postgres user in one go:

    ```
    $ sudo su postgres psql
    ```