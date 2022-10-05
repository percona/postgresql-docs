# Install Percona Distribution for PostgreSQL

We recommend that you install Percona Distribution for PostgreSQL from Percona repositories using the package manager of your operating system. Find the list of supported Linux distributions on the [Percona Software and Platform Lifecycle page](https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql) page.

Installing Percona Distribution for PostgreSQL from Percona repositories means to subscribe to these repositories. Percona provides the [percona-release](https://www.percona.com/doc/percona-repo-config/index.html) repository management tool for this purpose. It simplifies operating repositories and enables to install and update both Percona Distribution for PostgreSQL packages and required dependencies smoothly.

## Procedure

### 1. Install **percona-release**

[Install **percona-release**](https://www.percona.com/doc/percona-repo-config/installing.html) utility. If you have installed it before, [update](https://www.percona.com/doc/percona-repo-config/updating.html) it to the latest version.

### 2. Enable the repository

As soon as **percona-release** is installed or up-to-date, enable the repository for Percona Distribution for PostgreSQL (`ppg-11`). We recommend using the *setup* command as it enables the specified repository and updates the platform’s package manager database.

To install the *latest* version of Percona Distribution for PostgreSQL, enable the Major release repository using the following command:

```
$ sudo percona-release setup ppg-11
```

To install a *specific minor version* of Percona Distribution for PostgreSQL, enable the Minor release repository. For example, to install Percona Distribution for PostgreSQL 11.10, enable the `ppg-11.10`  repository using the following command:

```
$ sudo percona-release setup ppg-11.10
```

### 3. Install Percona Distribution for PostgreSQL packages

!!! important
   
    Run all the commands in the following sections as root or using the **sudo** command.

=== "On Debian and Ubuntu using `apt`"

    !!! note

        Debian and other systems that use the `apt` package manager include the upstream PostgreSQL server package (postgresql-11) by default. The components of Percona Distribution for PostgreSQL 11 can only be installed together with the PostgreSQL server shipped by Percona (percona-postgresql-11). If you wish to use Percona Distribution for PostgreSQL, uninstall the PostgreSQL package provided by your distribution (postgresql-11) and then install the chosen components from Percona Distribution for PostgreSQL.


    Install the **percona-postgresql-11** package using the following command.

    ```
    $ sudo apt install percona-postgresql-11
    ```

=== "On Red Hat Enterprise Linux and derivatives using `yum`" 

    #### Platform specific notes


    If you intend to install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux v8, disable the ``postgresql``  and ``llvm-toolset``modules:

    ```
    $ sudo dnf module disable postgresql llvm-toolset
    ```


    On CentOS 7, you should install the ``epel-release`` package:


    ```
    $ sudo yum -y install epel-release
    $ sudo yum repolist
    ```

    Install the **percona-postgresql-11** package using **yum install**.

    ```
    $ sudo yum install percona-postgresql11-server
    ```

### 4. Install the Percona Distribution for PostgreSQL components

Use the following commands to install components’ packages:

=== "On Debian and Ubuntu"

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


=== "On Red Hat Enterprise Linux and derivatives" 

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

    [Install `pg_stat_monitor`](pg-stat-monitor.md):


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

#### Starting the service

=== "Debian and Ubuntu"

    The installation process automatically initializes and starts the default database. To check the status of Percona Distribution for PostgreSQL, use the following command:

    ```
    $ sudo systemctl status postgresql
    ```

=== "RHEL and derivatives"

    After the installation, the default database storage is not automatically initialized. To complete the installation and start Percona Distribution for PostgreSQL, initialize the database using the following command:

    ```
    $ /usr/pgsql-11/bin/postgresql-11-setup initdb
    ```

    Start the PostgreSQL service:

    ```
    $ sudo systemctl start postgresql-11
    ```


## Enabling extensions

Some extensions require additional configuration before using them with Percona Distribution for PostgreSQL. This section provides configuration instructions per extension.

### Patroni

Patroni is the third-party high availability solution for PostgreSQL. The [High Availability in PostgreSQL with Patroni](solutions/high-availability.md) chapter provides details about the solution overview and architecture deployment. 

While setting up a high-availability PostgreSQL cluster with Patroni, you will need the following components:

- Patroni, installed on every ``postresql`` node. 

- Distributed Configuration Store (DCS). Patroni supports such DCSs as ETCD, zookeeper, Kubernetes, though [ETCD](https://etcd.io/) is the most popular one. It is available upstream as DEB packages for Debian 10 and Ubuntu 18.04, 20.04.

  For CentOS 8, RPM packages for ETCD is available within Percona Distribution for PostreSQL.  You can install it using the following command: 

  ```sh
  $ yum install etcd python3-python-etcd
     
  ```
  
- [HAProxy](http://www.haproxy.org/).

See the configuration guidelines for [Debian and Ubuntu](solutions/ha-setup-apt.md) and [RHEL and CentOS](solutions/ha-setup-yum.md). 

!!! seealso

    - [Patroni documentation](https://patroni.readthedocs.io/en/latest/SETTINGS.html#settings)

    - Percona Blog: 

        - [PostgreSQL HA with Patroni: Your Turn to Test Failure Scenarios](https://www.percona.com/blog/2021/06/11/postgresql-ha-with-patroni-your-turn-to-test-failure-scenarios/) 

### pgBadger

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

### pgAudit set-user

Add the `set-user` to `shared_preload_libraries` in `postgresql.conf`. The recommended way is to  use the [ALTER SYSTEM](https://www.postgresql.org/docs/11/sql-altersystem.html) command. [Connect to psql](#connect-to-the-postgresql-server) and use the following command:

```sql
$ ALTER SYSTEM SET shared_preload_libraries = 'set-user';
```

Start/restart the server to apply the configuration.

You can fine-tune user behavior with the [custom parameters](https://github.com/pgaudit/set_user#configuration-options) supplied with the extension.

### wal2json

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