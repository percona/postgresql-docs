# Uninstalling Percona Distribution for PostgreSQL

To uninstall Percona Distribution for PostgreSQL, remove all the installed packages and data / configuration files.

**NOTE**: Should you need the data files later, back up your data before uninstalling Percona Distribution for PostgreSQL.

## On Debian and Ubuntu using `apt`

To uninstall Percona Distribution for PostgreSQL on platforms that use **apt** package manager such as Debian
or Ubuntu, complete the following steps.

Run all commands as root or via **sudo**.


1. Stop the Percona Distribution for PostgreSQL service.

    ```
    $ sudo systemctl stop postgresql.service
    ```


2. Remove the **percona-postgresql** packages.

    ```
    $ sudo apt-get remove percona-postgresql-13* percona-pgbackrest percona-patroni percona-pg-stat-monitor13
    ```


3. Remove configuration and data files.

    ```
    $ rm -rf /etc/postgresql/13/main
    ```

## On Red Hat Enterprise Linux and CentOS using `yum`

To uninstall Percona Distribution for PostgreSQL on platforms that use **yum** package manager such as
Red Hat Enterprise Linux or CentOS, complete the following steps.

Run all commands as root or via **sudo**.


1. Stop the Percona Distribution for PostgreSQL service.
   
    ```
    $ sudo systemctl stop postgresql-13
    ```


2. Remove the **percona-postgresql** packages

    ```
    $ sudo yum remove percona-postgresql13*
    ```


3. Remove configuration and data files

    ```
    $ rm -rf /var/lib/pgsql/13/data
    ```
