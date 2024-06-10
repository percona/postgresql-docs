# Install Percona Distribiution for PostgreSQL from binary tarballs

You can find the binary tarballs on the [Percona website](https://www.percona.com/downloads). Select the desired version from a version dropdown and _All_ from the Select Platform dropdown.

There are the following tarballs available: 

* percona-postgresql-{{dockertag}}-ssl1.1-linux-x86_64.tar.gz  - for operating systems that run OpenSSL version 1.x
* percona-postgresql-{{dockertag}}-ssl3-linux-x86_64.tar.gz - for for operating systems that run OpenSSL version 3.x

To check what OpenSSL version you have, run the following command: 

```{.bash data-prompt="$"}
$ openssl version
```

## Tarball contents

The tarballs include the following components:

| Component | Description |
|-----------|-------------|
| percona-postgresql{{pgversion}}| A metapackage that installs the latest version of PostgreSQL. It also includes the following extensions: <br> - `pgaudit` <br> - `pgAudit_set_user` <br> - `pg_repack` <br> - `pg_stat_monitor` <br> - `pg_gather` <br> - `wal2json` <br> -  the set of [contrib extensions](contrib.md)|
| percona-haproxy | A high-availability solution and load-balancing solution |
| percona-patroni | A high-availability solution for PostgreSQL |
| percona-pgbackrest| A backup and restore tool |
| percona-pgbadger| PostgreSQL log analyzer with fully detailed reports and graphs |
| percona-pgbouncer| Lightweight connection pooler for PostgreSQL |
| percona-pgpool-II| A middleware between PostgreSQL server and client for high availability, connection pooling and load balancing |
| percona-perl | A Perl module required to create the `plperl` extension - a procedural language handler for PostgreSQL that allows writing functions in the Perl programming language|
| percona-python3 | A Python3 module required to create `plpython` extension - a procedural language handler for PostgreSQL that allows writing functions in the Python programming language. Python is also required by Patroni
| percona-tcl | Tcl development libraries required to create the `pltcl` extension - a loadable procedural language for the PostgreSQL database system that enables the creation of functions and trigger procedures in the Tcl language |
| percona-etcd | A key-value distributed store that stores the state of the PostgreSQL cluster|

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

The steps below install the tarballs for OpenSSL 3.x. Use another tarball if your operating system has OpenSSL version 1.x.

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
    $ sudo tar -xfv percona-postgresql-{{dockertag}}-ssl3-linux-x86_64.tar.gz -C /opt/pgdistro/
    ```

5. If you extracted the tarball somewhere else in your system, copy `percona-python3`, `percona-tcl` and `percona-perl` to the `/opt` directory. This is required for the correct run of libraries that require those modules. 
 
    ```{.bash data-prompt="$"}
    $ sudo cp <path_to>/percona-perl <path_to>/percona-python3 <path_to>/percona-tcl /opt/
    ```
    
6. Add the location of the binaries to the PATH variable:

    ```{.bash data-prompt="$"}
    $ export PATH=:/opt/pgdistro/percona-haproxy/sbin/:/opt/pgdistro/percona-patroni/bin/:/opt/pgdistro/percona-pgbackrest/bin/:/opt/pgdistro/percona-pgbadger/:/opt/pgdistro/percona-pgbouncer/bin/:/opt/pgdistro/percona-pgpool-II/bin/:/opt/pgdistro/percona-postgresql{{pgversion}}/bin/:/opt/pgdistro/percona-etcd/bin/:/opt/percona-perl/bin/:/opt/percona-tcl/bin/:/opt/percona-python3/bin/:$PATH
    ```

6. Create the data directory for PostgreSQL server. For example, `/usr/local/pgsql/data`.
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
   
### Start the components

After you unpacked the tarball and added the location of the components' binaries to the $PATH variable, the components are available for use. You can invoke a component by running its command-line tool. For example, to check HAProxy version, type:

```{.bash data-prompt="$"}
$ haproxy version
```

Some components require additional setup. Check the [Enabling extensions](enable-extensions.md) page for details.