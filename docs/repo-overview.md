# Repositories overview

Percona provides two repositories for Percona Distribution for PostgreSQL. 

| Major release repository | Minor release repository | 
| ------------------------ | ------------------------ | 
| *Major Release repository* (`ppg-16`) it includes the latest version packages. Whenever a package is updated, the package manager of your operating system detects that and prompts you to update. As long as you update all Distribution packages at the same time, you can ensure that the packages you’re using have been tested and verified by Percona. <br><br> We recommend installing Percona Distribution for PostgreSQL from the *Major Release repository*| *Minor Release repository* includes a particular minor release of the database and all of the packages that were tested and verified to work with that minor release (e.g. `ppg-16.0`). You may choose to install Percona Distribution for PostgreSQL from the Minor Release repository if you have decided to standardize on a particular release which has passed rigorous testing procedures and which has been verified to work with your applications. This allows you to deploy to a new host and ensure that you’ll be using the same version of all the Distribution packages, even if newer releases exist in other repositories. <br> <br> The disadvantage of using a Minor Release repository is that you are locked in this particular release. When potentially critical fixes are released in a later minor version of the database, you will not be prompted for an upgrade by the package manager of your operating system. You would need to change the configured repository in order to install the upgrade.|

## Repository contents

Percona Distribution for PostgreSQL provides individual packages for its components. It also includes two meta-packages: `percona-ppg-server` and `percona-ppg-server-ha`.

Using a meta-package, you can install all components it contains in one go.

!!! note

    Meta packages are deprecated and will be removed in future releases.

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
| `percona-pgaudit{{pgversion}}` | Provides detailed session or object audit logging via the standard PostgreSQL logging facility. | 
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
| `python3-python-etcd` | A Python client for etcd |

## Tech Preview: PSP 16 testing repository

!!! warning "Tech Preview"

    This is a **Tech Preview** feature. Percona doesn't recommend Tech Preview features for production environments. We provide them to give users early access to new functionality and the opportunity to provide feedback while the feature is still under development. There is no commitment to support them long-term, and the feature may change or be removed without notice.

Percona Server for PostgreSQL (PSP) 16.15, built with the [`pg_tde` :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html) extension included natively, is available for evaluation through a dedicated testing repository. This is not a GA release of Percona Distribution for PostgreSQL 16 - it's a separate, experimental build for users who want to try `pg_tde` and the other bundled components ahead of a full release.

Enable the testing repository with the `percona-release` utility:

```{.bash data-prompt="$"}
$ sudo percona-release enable-only psp-16
```

Once the repository is enabled, follow the same package installation steps as [Install via apt](apt.md) or [Install via yum](yum.md), skipping the `percona-release setup ppg-16` step since the testing repository is already enabled.

To enable and use `pg_tde`, follow the steps in the [pg_tde documentation :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html) to configure it.

For the full list of bundled extensions and their versions, see [Percona-authored extensions](percona-ext.md). Docker images for this Tech Preview are also available - see [Run in Docker](docker.md).
