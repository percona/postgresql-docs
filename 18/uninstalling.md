> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/18/llms.txt).

# Uninstalling Percona Distribution for PostgreSQL

To uninstall Percona Distribution for PostgreSQL, remove all the installed packages and data / configuration files.

Note

Should you need the data files later, back up your data before uninstalling Percona Distribution for PostgreSQL.

**On Debian and Ubuntu using apt**

To uninstall Percona Distribution for PostgreSQL on platforms that use **apt** package manager such as Debian or Ubuntu, complete the following steps.

Run all commands as root or via **sudo**.

1. Stop the Percona Distribution for PostgreSQL service.

   ```
   $ sudo systemctl stop postgresql.service
   ```

1. Remove the **percona-postgresql** packages.

   ```
   $ sudo apt remove percona-postgresql-18* percona-patroni percona-pgbackrest  percona-pgbadger percona-pgbouncer
   ```

1. Remove configuration and data files.

   ```
   $ rm -rf /etc/postgresql/18/main
   ```

**On Red Hat Enterprise Linux and derivatives using yum**

To uninstall Percona Distribution for PostgreSQL on platforms that use **yum** package manager such as Red Hat Enterprise Linux or CentOS, complete the following steps.

Run all commands as root or via **sudo**.

1. Stop the Percona Distribution for PostgreSQL service.

   ```
   $ sudo systemctl stop postgresql-18
   ```

1. Remove the **percona-postgresql** packages

   ```
   $ sudo yum remove percona-postgresql18* percona-pgbadger
   ```

1. Remove configuration and data files

   ```
   $ rm -rf /var/lib/pgsql/18/data
   ```

## Uninstall from tarballs

If you [installed Percona Distribution for PostgreSQL from binary tarballs](https://docs.percona.com/postgresql/18/tarball.html), stop the PostgreSQL server and remove the folder with the binary tarballs.

1. Stop the `postgres` server:

   ```
   $ /path/to/tarballs/percona-postgresql18/bin/pg_ctl -D path/to/datadir -l logfile stop
   ```

   Sample output

   ```
   waiting for server to shut down.... done
   server stopped
   ```

1. Remove the directory with extracted tarballs

   ```
   $ sudo rm -rf /path/to/tarballs/
   ```
