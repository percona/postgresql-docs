# Uninstalling Percona Distribution for PostgreSQL

To uninstall Percona Distribution for PostgreSQL, remove all the installed packages and data / configuration files.

**NOTE**: Should you need the data files later, back up your data before uninstalling Percona Distribution for PostgreSQL.

=== ":material-debian: On Debian and Ubuntu using `apt`"

     To uninstall Percona Distribution for PostgreSQL on platforms that use **apt** package manager such as Debian
     or Ubuntu, complete the following steps.

     Run all commands as root or via **sudo**.
     {.power-number}


     1. Stop the Percona Distribution for PostgreSQL service.

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql.service
         ```

     2. Remove the **percona-postgresql** packages.

         ```{.bash data-prompt="$"}
         $ sudo apt remove percona-postgresql-{{pgversion}}* percona-patroni percona-pgbackrest  percona-pgbadger percona-pgbouncer
         ```


     3. Remove configuration and data files.

         ```{.bash data-prompt="$"}
         $ rm -rf /etc/postgresql/{{pgversion}}/main
         ```

=== ":material-redhat: On Red Hat Enterprise Linux and derivatives using `yum`"

     To uninstall Percona Distribution for PostgreSQL on platforms that use **yum** package manager such as
     Red Hat Enterprise Linux or CentOS, complete the following steps.

     Run all commands as root or via **sudo**.
     {.power-number}


     1. Stop the Percona Distribution for PostgreSQL service.
        
         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql-{{pgversion}}
         ```


     2. Remove the **percona-postgresql** packages

         ```{.bash data-prompt="$"}
         $ sudo yum remove percona-postgresql{{pgversion}}* percona-pgbadger
         ```


     3. Remove configuration and data files

         ```{.bash data-prompt="$"}
         $ rm -rf /var/lib/pgsql/{{pgversion}}/data
         ```

## Uninstall from tarballs

If you [installed Percona Distribution for PostgreSQL from binary tarballs](tarball.md), stop the PostgreSQL server and remove the folder with the binary tarballs.

1. Stop the `postgres` server:

    ```{.bash data-prompt="$"}
    $ /path/to/tarballs/percona-postgresql{{pgversion}}/bin/pg_ctl -D path/to/datadir -l logfile stop
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        waiting for server to shut down.... done
        server stopped
        ```

2. Remove the directory with extracted tarballs

    ```{.bash data-prompt="$"}
    $ sudo rm -rf /path/to/tarballs/
    ```