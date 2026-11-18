> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/18/llms.txt).

# Install Percona Distribution for PostgreSQL from binary tarballs

You can download the tarballs using the links below.

Note

Unlike package managers, a tarball installation does **not** provide mechanisms to ensure that all dependencies are resolved to the correct library versions. There is no built-in method to verify that required libraries are present or to prevent them from being removed. As a result, unresolved or broken dependencies may lead to errors, crashes, or even data corruption.

For this reason, tarball installations are **not recommended** for environments where safety, security, reliability, or mission-critical stability are required.

The following tarballs are available for the x86_64 and ARM64 architectures:

- [percona-postgresql-18.7-ssl1.1-linux-aarch64.tar.gz](https://downloads.percona.com/downloads/postgresql-distribution-18/18.7/binary/tarball/percona-postgresql-18.7-ssl1.1-linux-aarch64.tar.gz) - for operating systems on ARM64 architecture that run OpenSSL version 1.x
- [percona-postgresql-18.7-ssl1.1-linux-x86_64.tar.gz](https://downloads.percona.com/downloads/postgresql-distribution-18/18.7/binary/tarball/percona-postgresql-18.7-ssl1.1-linux-x86_64.tar.gz) - for operating systems on x86_64 architecture that run OpenSSL version 1.x
- [percona-postgresql-18.7-ssl3-linux-aarch64.tar.gz](https://downloads.percona.com/downloads/postgresql-distribution-18/18.7/binary/tarball/percona-postgresql-18.7-ssl3-linux-aarch64.tar.gz) - for operating systems on ARM64 architecture that run OpenSSL version 3.1.x
- [percona-postgresql-18.7-ssl3-linux-x86_64.tar.gz](https://downloads.percona.com/downloads/postgresql-distribution-18/18.7/binary/tarball/percona-postgresql-18.7-ssl3-linux-x86_64.tar.gz) - for operating systems on x86_64 architecture that run OpenSSL version 3.1.x
- [percona-postgresql-18.7-ssl3.5-linux-aarch64.tar.gz](https://downloads.percona.com/downloads/postgresql-distribution-18/18.7/binary/tarball/percona-postgresql-18.7-ssl3.5-linux-aarch64.tar.gz) - for operating systems on ARM64 architecture that run OpenSSL version 3.5.x
- [percona-postgresql-18.7-ssl3.5-linux-x86_64.tar.gz](https://downloads.percona.com/downloads/postgresql-distribution-18/18.7/binary/tarball/percona-postgresql-18.7-ssl3.5-linux-x86_64.tar.gz) - for operating systems on x86_64 architecture that run OpenSSL version 3.5.x

To check what OpenSSL version you have, run the following command:

```
$ openssl version
```

## Tarball contents

The tarballs include the following components:

| Component            | Description                                                                                                                                                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| percona-postgresql18 | The latest version of PostgreSQL server and the following extensions: - `pgaudit` - `pgAudit_set_user` - `credcheck` - `pg_repack` - `pg_stat_monitor` - `pg_gather` - `wal2json` - `postGIS` - the set of [contrib extensions](https://docs.percona.com/postgresql/18/contrib.html) |
| percona-haproxy      | A high-availability solution and load-balancing solution                                                                                                                                                                                                                             |
| percona-patroni      | A high-availability solution for PostgreSQL                                                                                                                                                                                                                                          |
| percona-pgbackrest   | A backup and restore tool                                                                                                                                                                                                                                                            |
| percona-pgbadger     | PostgreSQL log analyzer with fully detailed reports and graphs                                                                                                                                                                                                                       |
| percona-pgbouncer    | Lightweight connection pooler for PostgreSQL                                                                                                                                                                                                                                         |
| percona-pgpool-II    | A middleware between PostgreSQL server and client for high availability, connection pooling and load balancing                                                                                                                                                                       |
| percona-perl         | A Perl module required to create the `plperl` extension - a procedural language handler for PostgreSQL that allows writing functions in the Perl programming language                                                                                                                |
| percona-python3      | A Python3 module required to create `plpython` extension - a procedural language handler for PostgreSQL that allows writing functions in the Python programming language. Python is also required by Patroni                                                                         |
| percona-tcl          | Tcl development libraries required to create the `pltcl` extension - a loadable procedural language for the PostgreSQL database system that enables the creation of functions and trigger procedures in the Tcl language                                                             |
| percona-etcd         | A key-value distributed store that stores the state of the PostgreSQL cluster                                                                                                                                                                                                        |

## Preconditions

**Debian and Ubuntu**

1. Uninstall the upstream PostgreSQL package.

1. Ensure that the `libreadline` is installed on the system, as it is **required** for tarballs to work correctly:

   ```
   $ sudo apt install -y libreadline-dev
   ```

1. Create the user to own the PostgreSQL process. For example, `mypguser`. Run the following command:

   ```
   $ sudo useradd -m mypguser
   ```

   Set the password for the user:

   ```
   $ sudo passwd mypguser
   ```

**RHEL and derivatives**

On RHEL, Rocky Linux, or Oracle Linux 10, install the `acl` package. This package is **required** for correct permission handling when using tarball-based installations:

```
$ sudo dnf install -y acl
```

Ensure that the `libreadline` is installed on the system, as it is **required** for tarballs to work correctly:

```
$ sudo yum install -y readline-devel
```

Create the user to own the PostgreSQL process. For example, `mypguser`. Run the following command:

```
$ sudo useradd mypguser -m
```

Set the password for the user:

```
$ sudo passwd mypguser
```

## Procedure

The steps below install the tarballs for OpenSSL 3.x on x86_64 architecture. Use another tarball if your operating system has OpenSSL version 1.x and / or has the ARM64 architecture.

1. Create the directory where you will store the binaries. For example, `/opt/pgdistro`

1. Grant access to this directory for the `mypguser` user.

   ```
   $ sudo chown mypguser:mypguser /opt/pgdistro/
   ```

1. Fetch the binary tarball.

   ```
   $ wget https://downloads.percona.com/downloads/postgresql-distribution-18/18.7/binary/tarball/percona-postgresql-18.7-ssl3-linux-x86_64.tar.gz
   ```

1. Extract the tarball to the directory for binaries that you created on step 1.

   ```
   $ sudo tar -xvf percona-postgresql-18.7-ssl3-linux-x86_64.tar.gz -C /opt/pgdistro/
   ```

1. If you extracted the tarball in a directory other than `/opt`, copy `percona-python3`, `percona-tcl` and `percona-perl` to the `/opt` directory. This is required for the correct run of libraries that require those modules.

   ```
   $ sudo cp <path_to>/percona-perl <path_to>/percona-python3 <path_to>/percona-tcl /opt/
   ```

1. Add the location of the binaries to the PATH variable:

   ```
   $ export PATH=:/opt/pgdistro/percona-haproxy/sbin/:/opt/pgdistro/percona-patroni/bin/:/opt/pgdistro/percona-pgbackrest/bin/:/opt/pgdistro/percona-pgbadger/:/opt/pgdistro/percona-pgbouncer/bin/:/opt/pgdistro/percona-pgpool-II/bin/:/opt/pgdistro/percona-postgresql18/bin/:/opt/pgdistro/percona-etcd/bin/:/opt/percona-perl/bin/:/opt/percona-tcl/bin/:/opt/percona-python3/bin/:$PATH
   ```

1. Create the data directory for PostgreSQL server. For example, `/usr/local/pgsql/data`.

1. Grant access to this directory for the `mypguser` user.

   ```
   $ sudo chown mypguser:mypguser /usr/local/pgsql/data
   ```

1. Switch to the user that owns the Postgres process. In our example, `mypguser`:

   ```
   $ su - mypguser
   ```

1. Initiate the PostgreSQL data directory:

   ```
   $ /opt/pgdistro/percona-postgresql18/bin/initdb -D /usr/local/pgsql/data
   ```

   Sample output

   ```
   Success. You can now start the database server using:

   /opt/pgdistro/percona-postgresql18/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
   ```

1. Start the PostgreSQL server:

   ```
   $ /opt/pgdistro/percona-postgresql18/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
   ```

   Sample output

   ```
   waiting for server to start.... done
   server started
   ```

1. Connect to `psql`

   ```
   $ /opt/pgdistro/percona-postgresql18/bin/psql -d postgres
   ```

   Sample output

   ```
   psql (18.7.1 (Percona Server for PostgreSQL), server 18.7.1 (Percona Server for PostgreSQL))
   Type "help" for help.

   postgres=#
   ```

### Start the components

After you unpacked the tarball and added the location of the components’ binaries to the `$PATH` variable, the components are available for use. You can invoke a component by running its command-line tool.

For example, to check HAProxy version, type:

```
$ haproxy version
```

Some components require additional setup. Check the [Enabling extensions](https://docs.percona.com/postgresql/18/enable-extensions.html) page for details.
