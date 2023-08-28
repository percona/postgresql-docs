# Install Percona Distribution for PostgreSQL

We recommend that you install Percona Distribution for PostgreSQL from Percona repositories using the package manager of your operating system. Find the list of supported Linux distributions on the [Percona Software and Platform Lifecycle page](https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql) page.

Installing Percona Distribution for PostgreSQL from Percona repositories means to subscribe to these repositories. Percona provides the [percona-release](https://www.percona.com/doc/percona-repo-config/index.html) repository management tool for this purpose. It simplifies operating repositories and enables to install and update both Percona Distribution for PostgreSQL packages and required dependencies smoothly.

## Package contents

In addition to individual packages for its components, Percona Distribution for PostgreSQL also includes two meta-packages: `percona-ppg-server` and `percona-ppg-server-ha`.

Using a meta-package, you can install all components it contains in one go.

### `percona-ppg-server`

=== "Package name on Debian/Ubuntu"

     `percona-ppg-server-14`

=== "Package name on RHEL/derivatives"

     `percona-ppg-server14`

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

=== "Package name on Debian/Ubuntu"

     `percona-ppg-server-ha-14`

=== "Package name on RHEL/derivatives"

     `percona-ppg-server-ha14`

The `percona-ppg-server-ha` meta-package installs high-availability components that are recommended by Percona:

| Package contents | Description                             |  
| ---------------- | --------------------------------------- | 
| `percona-patroni`| A high-availability solution for PostgreSQL. | 
| `percona-haproxy`| A high-availability and load-balancing solution |
| `python3-python-etcd` | A Python client for ETCD.[^1] |
| `etcd-client`, `etcd-server` | The client/server of the distributed key-value store. [^2]| 

To install Percona Distribution for PostgreSQL, refer to the following tutorials:

* [On Debian and Ubuntu](apt.md)
* [On Red Hat Enterprise Linux and derivatives](yum.md)




[^1]: Is included in repositories for RHEL 8 / CentOS 8 operating systems
[^2]: Are included in repositories for Debian 12 operating system