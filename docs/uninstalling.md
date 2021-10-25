# Uninstalling Percona Distribution for PostgreSQL

To uninstall Percona Distribution for PostgreSQL, remove all the installed packages and data / configuration files.

!!! note

    Should you need the data files later, back up your data before uninstalling Percona Distribution for PostgreSQL.

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
    $ sudo apt remove percona-postgresql-11* percona-pgbackrest percona-patroni percona-pgbadger percona-pgbouncer
    ```


3. Remove configuration and data files.

    ```
    $ rm -rf /etc/postgresql/11/main
    ```

## On Red Hat Enterprise Linux and CentOS using `yum`

To uninstall Percona Distribution for PostgreSQL on platforms that use **yum** package manager such as
Red Hat Enterprise Linux or CentOS, complete the following steps.

Run all commands as root or via **sudo**.


1. Stop the Percona Distribution for PostgreSQL service.

    ```
    $ sudo systemctl stop postgresql-11
    ```


2. Remove the **percona-postgresql** packages

    ```
    $ sudo yum remove percona-postgresql11* percona-pgbadger
    ```


3. Remove configuration and data files

    ```
    $ rm -rf /var/lib/pgsql/11/data
    ```
