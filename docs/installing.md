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

There are two repositories available for Percona Distribution for PostgreSQL. We recommend installing Percona Distribution for PostgreSQL  from the *Major Release repository* (e.g. `ppg-13`) as it includes the latest version packages. Whenever a package is updated, the package manager of your operating system detects that and prompts you to update. As long as you update all Distribution packages at the same time, you can ensure that the packages you’re using have been tested and verified by Percona.

The *Minor Release repository* includes a particular minor release of the database and all of the packages that were tested and verified to work with that minor release (e.g. `ppg-13.1`). You may choose to install Percona Distribution for PostgreSQL from the Minor Release repository if you have decided to standardize on a particular release which has passed rigorous testing procedures and which has been verified to work with your applications. This allows you to deploy to a new host and ensure that you’ll be using the same version of all the Distribution packages, even if newer releases exist in other repositories.

The disadvantage of using a Minor Release repository is that you are locked in this particular release. When potentially critical fixes are released in a later minor version of the database, you will not be prompted for an upgrade by the package manager of your operating system. You would need to change the configured repository in order to install the upgrade.

## Install **percona-release**

Install **percona-release** utility. If you have installed it before, update it to the latest version. Refer to [Percona repositories documentation](https://www.percona.com/doc/percona-repo-config/percona-release.html) for installation / update instructions.

## Enable the repository

As soon as **percona-release** is installed or up-to-date, enable the repository for Percona Distribution for PostgreSQL (`ppg-13`). We recommend using the *set up* command as it enables the specified repository and updates the platform’s package manager database.

To install the *latest* version of Percona Distribution for PostgreSQL, enable the Major Release repository using the following command:

```
$ sudo percona-release setup ppg-13
```

To install a *specific minor version* of Percona Distribution for PostgreSQL, enable the Minor release repository. For example, to install Percona Distribution for PostgreSQL 13.1, enable the `ppg-13.1`  repository using the following command:

```
$ sudo percona-release setup ppg-13.1
```

## Install Percona Distribution for PostgreSQL packages

After you’ve installed percona-release and enabled the desired repository, install Percona Distribution for PostgreSQL using the commands of your package manager (the procedure differs
depending on the package manager of your operating system).

### On Debian and Ubuntu using `apt`

!!! note
    On Debian and other systems that use the `apt` package manager, such as Ubuntu, components of Percona Distribution for PostgreSQL 13 can only be installed together with the server shipped by Percona (percona-postgresql-13). If you wish to use Percona Distribution for PostgreSQL, uninstall the PostgreSQL package provided by your distribution (postgresql-13) and then install the chosen components from Percona Distribution for PostgreSQL.

#### Platform Specific Notes

On Debian 9 (stretch), you need to [enable the llvm repository](https://apt.llvm.org/)

Install the **percona-postgresql-13** package using **apt-get install**.

```
$ sudo apt-get install percona-postgresql-13
```

Note that this package will not install the components. Use the following commands to install components’ packages:

Install `pg_repack`:

```
$ sudo apt-get install percona-postgresql-13-repack
```

Install `pgaudit`:

```
$ sudo apt-get install percona-postgresql-13-pgaudit
```

Install `pgBackRest`:

```
$ sudo apt-get install percona-pgbackrest
```

Install `Patroni`:

```
$ sudo apt-get install percona-patroni
```

Install `pg_stat_monitor`:

```
$ sudo apt-get install percona-pg-stat-monitor13
```

!!! note
    You need to set up `pg_stat_monitor` in order to use it with Percona Distribution for PostgreSQL. Refer to [Setup](pg-stat-monitor.md#setup) for configuration guidelines.

Install PostgreSQL contrib extensions:

```
$ sudo apt-get install percona-postgresql-contrib
```

#### Starting the service

The installation process automatically initializes the default database. Thus, to start Percona Distribution for PostgreSQL, use the following command:

```
$ sudo pg_ctlcluster 13 main start
```

Next steps: [connect to PostgreSQL](#connect-to-the-postgresql-server).

### On Red Hat Enterprise Linux and CentOS using `yum`

#### Platform Specific Notes

If you intend to install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux v8, disable the postgresql module:

```
$ sudo dnf module disable postgresql
```

On CentOS 7, you should install the epel-release package:

```
$ sudo yum -y install epel-release
$ sudo yum repolist
```

Install the **percona-postgresql-13** package using **yum install**.

```
$ sudo yum install percona-postgresql13-server
```

Note that this package will not install the components. Use the following commands to install components’ packages:

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

Install `pg_stat_monitor`:

```
$ sudo yum install percona-pg-stat-monitor13
```

!!! note
    You need to set up `pg_stat_monitor` in order to use it with Percona Distribution for PostgreSQL. Refer to [Setup](pg-stat-monitor.md#setup) for configuration guidelines.

Install PostgreSQL contrib extensions:

```
$ sudo yum install percona-postgresql13-contrib
```

#### Starting the service

After the installation, the default database storage is not automatically initialized. To complete the installation and start Percona Distribution for PostgreSQL, initialize the database using the following command:

```
/usr/pgsql-13/bin/postgresql-13-setup initdb
```

Start the PostgreSQL service:

```
$ sudo systemctl start postgresql-13
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

!!! note
    You can connect to `psql` as the `postgres` user in one go:

```
$ sudo su postgres psql
```

To exit the `psql` terminal, use the following command:

```
$ \q
```
