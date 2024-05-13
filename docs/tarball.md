# Install Percona Distribiution for PostgreSQL from binary tarballs

You can find the binary tarballs on the [Percona website](https://www.percona.com/downloads). Select the desired version from a version dropdown and _All_ from the Select Platform dropdown.

There are the following tarballs available: 

* percona-postgresql-{{dockertag}}-ssl1.1-linux-x86_64.tar.gz  - for operating systems that run OpenSSL version 1.1
* percona-postgresql-{{dockertag}}-ssl3-linux-x86_64.tar.gz - for for operating systems that run OpenSSL version 3.0

To check what OpenSSL version you have, run the following command: 

```{.bash data-prompt="$"}
$ openssl version
```

## Tarball contents

The tarballs include the following components:

| Component | Description |
|-----------|-------------|
| percona-postgresql{{pgversion}}| A metapackage that installs the latest version of PostgreSQL|
| percona-haproxy | A high-availability solution and load-balancing solution |
| percona-patroni | A high-availability solution for PostgreSQL |
| percona-pgbackrest| A backup and restore tool |
| percona-pgbadger| PostgreSQL log analyzer with fully detailed reports and graphs |
| percona-pgbouncer| Lightweight connection pooler for PostgreSQL |
| percona-pgpool-II| A middleware between PostgreSQL server and client for high availability, connection pooling and load balancing |

## Preconditions

=== "Debian and Ubuntu"

    1. Uninstall the upstream PostgreSQL package. 
    2. Create the user to own the PostgreSQL process. For example, `mypguser`. Run the following command:

        ```{.bash data-prompt="$"}
        $ sudo useradd -m mypguser
        ```

        Set the password for the user:

        ```{.bash data-prompt="$"}
        $ sudo passwd mypguser
        ```
    
=== "RHEL and derivatives"

    Create the user to own the PostgreSQL process. For example, `mypguser`, Run the following command: 
        
    ```{.bash data-prompt="$"}
    $ sudo useradd mypguser -m 
    ```

    Set the password for the user:

    ```{.bash data-prompt="$"}
    $ sudo passwd mypguser
    ```

## Procedure

The steps below install the tarballs for OpenSSL 3.0. Use another tarball if your operating system has OpenSSL version 1.1.

1. Create the directory where you will store the binaries. For example, `/opt/pgdistro`

2. Grant access to this directory for the `mypguser` user.

    ```{.bash data-prompt="$"}
    $ sudo chown mypguser:mypguser /opt/pgdistro/
    ```

3. Fetch the binary tarball:

    ```{.bash data-prompt="$"}
    $ wget https://downloads.percona.com/downloads/pg_tarballs-{{dockertag}}/percona-postgresql-{{dockertag}}-ssl3-linux-x86_64.tar.gz
    ```

4. Extract the tarball to the directory for binaries that you created on step 1.

    ```{.bash data-prompt="$"}
    $ tar -xfv percona-postgresql-{{dockertag}}-ssl3-linux-x86_64.tar.gz -C /opt/pgdistro/
    ```

5. Add the location of the binaries to the PATH variable:

    ```{.bash data-prompt="$"}
    $ export PATH=:/opt/pgdistro/percona-haproxy/bin/:/opt/pgdistro/percona-patroni/bin/:/opt/pgdistro/percona-pgbackrest/bin/:/opt/pgdistro/percona-pgbadger/bin/:/opt/pgdistro/percona-pgbouncer/bin/:/opt/pgdistro/percona-pgpool-II/bin/:/opt/pgdistro/percona-postgresql{{pgversion}}/bin/:$PATH
    ```

6. Create the data directory. For example, `/usr/local/pgsql/data`.
7. Grant access to this directory for the `mypguser` user.

    ```{.bash data-prompt="$"}
    $ sudo chown mypguser:mypguser /usr/local/pgsql/data
    ```

8. Switch to the user that owns the Postgres process. In our example, `mypguser`:

    ```{.bash data-prompt="$"}
    $ su - mypguser
    ```

9. Initiate the PostgreSQL data directory:
   
    ```{.bash data-prompt="$"}
    $ /opt/pgdistro/percona-postgresql{{pgversion}}/bin/initdb -D /usr/local/pgsql/data
    ```


    ??? example "Sample output"

        ```{.text .no-copy}
        Success. You can now start the database server using:

        /opt/pgdistro/percona-postgresql{{pgversion}}/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
        ```

10. Start the PostgreSQL server:

    ```{.bash data-prompt="$"}
    $ /opt/pgdistro/percona-postgresql{{pgversion}}/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
    ```

    ??? example "Sample output"
       
        ```{.text .no-copy}
        waiting for server to start.... done
        server started
        ```

9. Connect to `psql`
    
    ```{.bash data-prompt="$"}
    $ /opt/pgdistro/percona-postgresql{{pgversion}}/bin/psql
    ```

    ??? example "Sample output"
       
        ```{.text .no-copy}
        psql ({{dockertag}})
        Type "help" for help.

        postgres=#
        ```
   