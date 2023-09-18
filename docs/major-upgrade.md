# Upgrading Percona Distribution for PostgreSQL from 15 to 16

This document describes the in-place upgrade of Percona Distribution for PostgreSQL using the `pg_upgrade` tool.

The in-place upgrade means installing a new version without removing the old version and keeping the data files on the server.

!!! admonition "See also"

    [`pg_upgrade` Documentation](https://www.postgresql.org/docs/15/pgupgrade.html)

Similar to installing, we recommend you to upgrade Percona Distribution for PostgreSQL from Percona repositories.

!!! important

    A major upgrade is a risky process because of many changes between versions and issues that might occur during or after the upgrade. Therefore, make sure to back up your data first. The backup tools are out of scope of this document. Use the backup tool of your choice.

The general in-place upgrade flow for Percona Distribution for PostgreSQL is the following:


1. Install new version of Percona Distribution for PostgreSQL packages.


2. Stop the PostgreSQL service.


3. Check the upgrade without modifying the data.


4. Upgrade Percona Distribution for PostgreSQL.


5. Start PostgreSQL service.


6. Execute the  **analyze_new_cluster.sh** script to generate statistics
so the system is usable.


7. Delete old packages and configuration files.

The exact steps may differ depending on the package manager of your operating system.

## On Debian and Ubuntu using `apt`

!!! important

    Run **all** commands as root or via **sudo**.


1. Install Percona Distribution for PostgreSQL 16 packages.


    * [Install percona-release](https://docs.percona.com/percona-software-repositories/installing.html)
    
    * Enable Percona repository:

      ```{.bash data-prompt="$"}
      $ sudo percona-release setup ppg-16
      ```


    * Install Percona Distribution for PostgreSQL 16 package:

      ```{.bash data-prompt="$"}
      $ sudo apt install percona-postgresql-16
      ```


    * Install the components:

      ```{.bash data-prompt="$"}
      $ sudo apt install percona-postgresql-16-repack \
       percona-postgresql-16-pgaudit \
       percona-pgbackrest \
       percona-patroni \
       percona-pgbadger \
       percona-pgaudit16-set-user \
       percona-pgbadger \
       percona-postgresql-16-wal2json \
       percona-pg-stat-monitor15 \
       percona-postgresql-contrib
       percona-haproxy
       percona-pgpool2
       percona-pg-gather
      ```

2. Stop the `postgresql` service.

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop postgresql.service
    ```

    This stops both Percona Distribution for PostgreSQL 14 and 15.


3. Run the database upgrade.


    * Log in as the `postgres` user.

      ```{.bash data-prompt="$"}
      $ sudo su postgres
      ```


    * Change the current directory to the `tmp` directory where logs and some scripts will be recorded:

      ```{.bash data-prompt="$"}
      $ cd tmp/
      ```


    * Check the ability to upgrade Percona Distribution for PostgreSQL from 15 to 16:

      ```{.bash data-prompt="$"}
      $ /usr/lib/postgresql/16/bin/pg_upgrade
      --old-datadir=/var/lib/postgresql/15/main \
      --new-datadir=/var/lib/postgresql/16/main  \
      --old-bindir=/usr/lib/postgresql/15/bin  \
      --new-bindir=/usr/lib/postgresql/16/bin  \
      --old-options '-c config_file=/etc/postgresql/15/main/postgresql.conf' \
      --new-options '-c config_file=/etc/postgresql/16/main/postgresql.conf' \
      --check
      ```

      The `--check` flag here instructs `pg_upgrade` to only check the upgrade without changing any data.

      **Sample output**

      ```
      Performing Consistency Checks
      -----------------------------
      Checking cluster versions                                   ok
      Checking database user is the install user                  ok
      Checking database connection settings                       ok
      Checking for prepared transactions                          ok
      Checking for reg* data types in user tables                 ok
      Checking for contrib/isn with bigint-passing mismatch       ok
      Checking for tables WITH OIDS                               ok
      Checking for invalid "sql_identifier" user columns          ok
      Checking for presence of required libraries                 ok
      Checking database user is the install user                  ok
      Checking for prepared transactions                          ok

      *Clusters are compatible*
      ```


    * Upgrade the Percona Distribution for PostgreSQL

      ```{.bash data-prompt="$"}
      $ /usr/lib/postgresql/16/bin/pg_upgrade
      --old-datadir=/var/lib/postgresql/15/main \
      --new-datadir=/var/lib/postgresql/16/main  \
      --old-bindir=/usr/lib/postgresql/15/bin  \
      --new-bindir=/usr/lib/postgresql/16/bin  \
      --old-options '-c config_file=/etc/postgresql/15/main/postgresql.conf' \
      --new-options '-c config_file=/etc/postgresql/16/main/postgresql.conf' \
      --link
      ```

      The  `--link` flag creates hard links to the files on the old version cluster so you don’t need to copy data.

      If you don’t wish to use the `--link` option, make sure that you have enough disk space to store 2 copies of files for both old version and new version clusters.


    * Go back to the regular user:

      ```{.bash data-prompt="$"}
      $ exit
      ```


    * The Percona Distribution for PostgreSQL 15 uses the `5432` port while the Percona Distribution for PostgreSQL 16 is set up to use the `5433` port by default. To start the Percona Distribution for PostgreSQL 15, swap ports in the configuration files of both versions.

      ```{.bash data-prompt="$"}
      $ sudo vim /etc/postgresql/16/main/postgresql.conf
      $ port = 5433 # Change to 5432 here
      $ sudo vim /etc/postgresql/15/main/postgresql.conf
      $ port = 5432 # Change to 5433 here
      ```


4. Start the `postgreqsl` service.

    ```{.bash data-prompt="$"}
    $ sudo systemctl start postgresql.service
    ```


5. Check the `postgresql` version.

    * Log in as a postgres user
 
       ```{.bash data-prompt="$"}
       $ sudo su postgres
       ```

    * Check the database version
    
       ```{.bash data-prompt="$"}
       $ psql -c "SELECT version();"
       ```


6. Run the `analyze_new_cluster.sh` script

    ```{.bash data-prompt="$"}
    $ tmp/analyze_new_cluster.sh
    $ #Logout
    $ exit
    ```


7. Delete Percona Distribution for PostgreSQL 15 packages and configuration files

    * Remove packages

       ```{.bash data-prompt="$"}
       $ sudo apt remove percona-postgresql-15* percona-pgbackrest percona-patroni percona-pg-stat-monitor15 percona-pgaudit15-set-user percona-pgbadger percona-pgbouncer percona-postgresql-15-wal2json
       ```

    * Remove old files

       ```{.bash data-prompt="$"}
       $ rm -rf /etc/postgresql/15/main
       ```


## On Red Hat Enterprise Linux and CentOS using `yum`

!!! important

    Run **all** commands as root or via **sudo**.


1. Install Percona Distribution for PostgreSQL 16 packages


    * [Install percona-release](https://docs.percona.com/percona-software-repositories/installing.html)
    
    * Enable Percona repository:

       ```{.bash data-prompt="$"}
       $ sudo percona-release setup ppg-16
       ```


    * Install Percona Distribution for PostgreSQL 16:

       ```{.bash data-prompt="$"}
       $ sudo yum install percona-postgresql16-server
       ```

    * Install components:

       ```{.bash data-prompt="$"}
       $ sudo yum install percona-pgaudit \
       percona-pgbackrest \
       percona-pg_repack16 \
       percona-patroni \
       percona-pg-stat-monitor16 \
       percona-pgbadger \
       percona-pgaudit16_set_user \
       percona-pgbadger \
       percona-wal2json16 \
       percona-postgresql16-contrib
       percona-haproxy
       percona-pgpool-II-pg16
       percona-pg_gather
       ```


2. Set up Percona Distribution for PostgreSQL 16 cluster

   * Log is as the postgres user

      ```{.bash data-prompt="$"}
      $ sudo su postgres
      ```

   * Set up locale settings

      ```
      export LC_ALL="en_US.UTF-8"
      export LC_CTYPE="en_US.UTF-8"
      ```

   * Initialize cluster with the new data directory

      ```{.bash data-prompt="$"}
      $ /usr/pgsql-16/bin/initdb -D /var/lib/pgsql/15/data
      ```


3. Stop the `postgresql` 15 service

    ```{.bash data-prompt="$"}
    $ systemctl stop postgresql-15
    ```


4. Run the database upgrade.


    * Log in as the `postgres` user

       ```{.bash data-prompt="$"}
       $ sudo su postgres
       ```


    * Check the ability to upgrade Percona Distribution for PostgreSQL from 5 to 16:

       ```{.bash data-prompt="$"}
       $ /usr/pgsql-16/bin/pg_upgrade \
       --old-bindir /usr/pgsql-15/bin \
       --new-bindir /usr/pgsql-16/bin  \
       --old-datadir /var/lib/pgsql/15/data \
       --new-datadir /var/lib/pgsql/16/data \
       --check
       ```

       The `--check` flag here instructs `pg_upgrade` to only check the upgrade without changing any data.

       **Sample output**

       ```
       Performing Consistency Checks
       -----------------------------
       Checking cluster versions                                   ok
       Checking database user is the install user                  ok
       Checking database connection settings                       ok
       Checking for prepared transactions                          ok
       Checking for reg* data types in user tables                 ok
       Checking for contrib/isn with bigint-passing mismatch       ok
       Checking for tables WITH OIDS                               ok
       Checking for invalid "sql_identifier" user columns          ok
       Checking for presence of required libraries                 ok
       Checking database user is the install user                  ok
       Checking for prepared transactions                          ok

       *Clusters are compatible*
       ```


    * Upgrade the Percona Distribution for PostgreSQL

       ```{.bash data-prompt="$"}
       $ /usr/pgsql-15/bin/pg_upgrade \
       --old-bindir /usr/pgsql-15/bin \
       --new-bindir /usr/pgsql-16/bin  \
       --old-datadir /var/lib/pgsql/15/data \
       --new-datadir /var/lib/pgsql/16/data \
       --link
       ```

       The  `--link` flag creates hard links to the files on the old version cluster so you don’t need to copy data.
       If you don’t wish to use the `--link` option, make sure that you have enough disk space to store 2 copies of files for both old version and new version clusters.


5. Start the `postgresql` 16 service.

    ```{.bash data-prompt="$"}
    $ systemctl start postgresql-16
    ```

6. Check postgresql status

    ```{.bash data-prompt="$"}
    $ systemctl status postgresql-16
    ```


7. Run the `analyze_new_cluster.sh` script


    * Log in as the postgres user

       ```{.bash data-prompt="$"}
       $ sudo su postgres
       ```

    * Run the script

       ```{.bash data-prompt="$"}
       $ ./analyze_new_cluster.sh
       ```


8. Delete Percona Distribution for PostgreSQL 15 configuration files

    ```{.bash data-prompt="$"}
    $ ./delete_old_cluster.sh
    ```


9. Delete Percona Distribution for PostgreSQL 15 packages

    *  Remove packages

       ```{.bash data-prompt="$"}
       $ sudo yum -y remove percona-postgresql15*
       ```

    * Remove old files

       ```{.bash data-prompt="$"}
       $ rm -rf /var/lib/pgsql/15/data
       ```
