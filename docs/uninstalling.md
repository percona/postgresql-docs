# Uninstalling Percona Distribution for PostgreSQL

To uninstall Percona Distribution for PostgreSQL, remove all the installed packages and data / configuration files.

**NOTE**: Should you need the data files later, back up your data before uninstalling Percona Distribution for PostgreSQL.

=== "On Debian and Ubuntu using `apt`"

     Run all commands as root or via **sudo**.
     {.power-number}


     1. Stop the Percona Distribution for PostgreSQL service.

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql.service
         ```


     2. Remove the **percona-postgresql** packages.

         ```{.bash data-prompt="$"}
         $ sudo apt remove percona-postgresql-12* percona-patroni percona-pgbackrest percona-pgbadger percona-pgbouncer
         ```


     3. Remove configuration and data files.
         
         ```{.bash data-prompt="$"}
         $ rm -rf /etc/postgresql/12/main
         ```

=== "On Red Hat Enterprise Linux and derivatives using `yum`"

     Run all commands as root or via **sudo**.
     {.power-number}


     1. Stop the Percona Distribution for PostgreSQL service.

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql-12
         ```


     2. Remove the **percona-postgresql** packages

         ```{.bash data-prompt="$"}
         $ sudo yum remove percona-postgresql12* percona-pgbadger
         ```


     3. Remove configuration and data files

         ```{.bash data-prompt="$"}
         $ rm -rf /var/lib/pgsql/12/data
         ```
