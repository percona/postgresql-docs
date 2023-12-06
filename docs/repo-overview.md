# Repositories overview

| Major release repository | Minor release repository | 
| ------------------------ | ------------------------ | 
|*Major Release repository* (e.g. `ppg-13`) includes the latest version packages. Whenever a package is updated, the package manager of your operating system detects that and prompts you to update. As long as you update all Distribution packages at the same time, you can ensure that the packages you’re using have been tested and verified by Percona. <br><br> We recommend installing Percona Distribution for PostgreSQL from the *Major Release repository* |*Minor Release repository* includes a particular minor release of the database and all of the packages that were tested and verified to work with that minor release (e.g. `ppg-13.6`). You may choose to install Percona Distribution for PostgreSQL from the Minor Release repository if you have decided to standardize on a particular release which has passed rigorous testing procedures and which has been verified to work with your applications. This allows you to deploy to a new host and ensure that you’ll be using the same version of all the Distribution packages, even if newer releases exist in other repositories.<br> <br> The disadvantage of using a Minor Release repository is that you are locked in this particular release. When potentially critical fixes are released in a later minor version of the database, you will not be prompted for an upgrade by the package manager of your operating system. You would need to change the configured repository in order to install the upgrade.|

## Repository contents

Percona Distribution for PostgreSQL provides individual packages for its components. It also includes two meta-packages: `percona-ppg-server` and `percona-ppg-server-ha`.

Using a meta-package, you can install all components it contains in one go.

### `percona-ppg-server`

=== "Package name on Debian/Ubuntu"

     `percona-ppg-server-{{pgversion}}`

=== "Package name on RHEL/derivatives"

     `percona-ppg-server{{pgversion}}`

The `percona-ppg-server` meta-package installs the PostgreSQL server with the following packages:

| Package contents | Description                             |  
| ---------------- | --------------------------------------- | 
| `percona-postgresql{{pgversion}}-server` | The PostgreSQL server package. |
| `percona-postgresql-common` | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
| `percona-postgresql{{pgversion}}-contrib` | A collection of additional PostgreSQLcontrib extensions | 
| `percona-pg-stat-monitor{{pgversion}}` | A Query Performance Monitoring tool for PostgreSQL. | 
| `percona-pgaudit` | Provides detailed session or object audit logging via the standard PostgreSQL logging facility. | 
| `percona-pg_repack{{pgversion}}`| rebuilds PostgreSQL database objects.| 
| `percona-wal2json{{pgversion}}` | a PostgreSQL logical decoding JSON output plugin.|


### `percona-ppg-server-ha`

=== "Package name on Debian/Ubuntu"

     `percona-ppg-server-ha-{{pgversion}}`

=== "Package name on RHEL/derivatives"

     `percona-ppg-server-{{pgversion}}`

The `percona-ppg-server-ha` meta-package installs high-availability components that are recommended by Percona:

| Package contents | Description                             |  
| ---------------- | --------------------------------------- | 
| `percona-patroni`| A high-availability solution for PostgreSQL. | 
| `percona-haproxy`| A high-availability and load-balancing solution |
| `etcd`           | A consistent, distributed key-value store | 
| `python3-python-etcd` | A Python client for ETCD.[^1] |
| `etcd-client`, `etcd-server` | The client/server of the distributed key-value store. [^2]| 



[^1]: Is included in repositories for RHEL 8 / CentOS 8 operating systems
[^2]: Are included in repositories for Debian 12 operating system
