# Install Percona Distribution for PostgreSQL

Percona provides installation packages in `DEB` and `RPM` format for 64-bit Linux distributions. Find the full list of supported platforms on the [Percona Software and Platform Lifecycle page](https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql).

Like many other Percona products, we recommend installing Percona Distribution for PostgreSQL from Percona repositories by using the **percona-release** utility. The **percona-release** utility automatically enables the required repository for you so you can easily install and update Percona Distribution for PostgreSQL packages and their dependencies through the package manager of your operating system.

## Package contents

In addition to individual packages for its components, Percona Distribution for PostgreSQL also includes two meta-packages: `percona-ppg-server` and `percona-ppg-server-ha`.

Using a meta-package, you can install all components it contains in one go.

### `percona-ppg-server`

The `percona-ppg-server` meta-package installs the PostgreSQL server with the following packages:

| Package contents | Description                             |  
| ---------------- | --------------------------------------- | 
| `percona-postgresql%{pgmajorversion}-server` | The PostgreSQL server package. |
| `percona-postgresql-common` | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
| `percona-postgresql%{pgmajorversion}-contrib` | A collection of additional PostgreSQLcontrib extensions | 
| `percona-pg-stat-monitor%{pgmajorversion}` | A Query Performance Monitoring tool for PostgreSQL. | 
| `percona-pgaudit` | Provides detailed session or object audit logging via the standard PostgreSQL logging facility. | 
| `percona-pg_repack%{pgmajorversion}`| rebuilds PostgreSQL database objects.| 
| `percona-wal2json%{pgmajorversion}` | a PostgreSQL logical decoding JSON output plugin.|

The `%{pgmajorversion}` variable stands for the major version of PostgreSQL.

### `percona-ppg-server-ha`

The `percona-ppg-server-ha` meta-package installs high-availability components that are recommended by Percona:

| Package contents | Description                             |  
| ---------------- | --------------------------------------- | 
| `percona-patroni`| A high-availability solution for PostgreSQL. | 
| `percona-haproxy`| A high-availability and load-balancing solution |
| `etcd`           | A consistent, distributed key-value store | 
| `python3-python-etcd` | A Python client for ETCD.[^1]

To install Percona Distribution for PostgreSQL, refer to the following tutorials:

* [On Debian and Ubuntu](apt.md)
* [On Red Hat Enterprise Linux and derivatives](yum.md)




[^1]: Is included in repositories for RHEL 8 / CentOS 8 operating systems