# Enable Percona Distribution for PostgreSQL components

Some components require additional configuration before using them with Percona Distribution for PostgreSQL. This sections provides configuration instructions per extension.

## Patroni

Patroni is the third-party high availability solution for PostgreSQL. The [High Availability in PostgreSQL with Patroni](solutions/high-availability.md) chapter provides details about the solution overview and architecture deployment. 

While setting up a high availability PostgreSQL cluster with Patroni, you will need the following components:

- Patroni installed on every ``postresql`` node. 

- Distributed Configuration Store (DCS). Patroni supports such DCSs as etcd, zookeeper, Kubernetes though [etcd](https://etcd.io/) is the most popular one. It is available within Percona Distribution for PostgreSQL for all supported operating systems.
  
- [HAProxy :octicons-link-external-16:](http://www.haproxy.org/).

See the configuration guidelines for [Debian and Ubuntu](solutions/ha-setup-apt.md) and [RHEL and CentOS](solutions/ha-setup-yum.md). 


!!! admonition "See also"

    - [Patroni documentation :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/SETTINGS.html#settings)

    - Percona Blog: 

        - [PostgreSQL HA with Patroni: Your Turn to Test Failure Scenarios :octicons-link-external-16:](https://www.percona.com/blog/2021/06/11/postgresql-ha-with-patroni-your-turn-to-test-failure-scenarios/) 
        
## pgBadger

Enable the following options in `postgresql.conf` configuration file before starting the service:

```
log_min_duration_statement = 0
log_line_prefix = '%t [%p]: '
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

For details about each option, see [pdBadger documentation :octicons-link-external-16:](https://github.com/darold/pgbadger/#POSTGRESQL-CONFIGURATION).

## pgaudit

Add the `pgaudit` to `shared_preload_libraries` in `postgresql.conf`. The recommended way is to use the [ALTER SYSTEM](https://www.postgresql.org/docs/16/sql-altersystem.html) command. [Connect to psql](#connect-to-the-postgresql-server) and use the following command:

```sql
ALTER SYSTEM SET shared_preload_libraries = 'pgaudit';
```

Start / restart the server to apply the configuration.

To configure `pgaudit`, you must have the privileges of a superuser. You can specify the settings in one of these ways:

*  globally (in postgresql.conf or using ALTER SYSTEM ... SET), 
* at the database level (using ALTER DATABASE ... SET), 
* at the role level (using ALTER ROLE ... SET). Note that settings are not inherited through normal role inheritance and SET ROLE will not alter a user's pgAudit settings. This is a limitation of the roles system and not inherent to pgAudit. 

Refer to the [pgaudit documentation](https://github.com/pgaudit/pgaudit/blob/master/README.md#settings) for details about available settings.

To enable `pgaudit`, connect to psql and run the CREATE EXTENSION command:

```sql
CREATE EXTENSION pgaudit;
```

## pgaudit set-user

Add the `set-user` to `shared_preload_libraries` in `postgresql.conf`. The recommended way is to use the [ALTER SYSTEM](https://www.postgresql.org/docs/13/sql-altersystem.html) command. [Connect to psql](connect.md) and use the following command:

```sql
ALTER SYSTEM SET shared_preload_libraries = 'set-user';
```

Start / restart the server to apply the configuration.

Install the extension into your database:

```sql
psql <database>
CREATE EXTENSION set_user;
```

You can fine-tune user behavior with the [custom parameters](https://github.com/pgaudit/set_user#configuration-options) supplied with the extension.


## pgbouncer

`pgbouncer` requires the `pgbouncer.ini` configuration file to start. The default path is `/etc/pgbouncer/pgbouncer.ini`. When installing `pgbouncer` from a [tarball](tarball.md), the path is `percona-pgbouncer/etc/pgbouncer.ini`.

Find detailed information about configuration file options in the [`pgbouncer documentation`](https://www.pgbouncer.org/config.html).

## pgpool2

`pgpool-II` requires the configuration file to start. When you install pgpool from a package, the configuration file is automatically created for you at the path `/etc/pgpool2/pgpool.conf` on Debian and Ubuntu and `/etc/pgpool-II/pgpool.conf` on RHEL and derivatives.

When you installed pgpool from tarballs, you can use the sample configuration file `<tarballsdir>/percona-pgpool-II/etc/pgpool2/pgpool.conf.sample`:

```{.bash data-prompt="$"}
$ cp <tarballsdir>/percona-pgpool-II/etc/pgpool2/pgpool.conf.sample <config-gile-path>/pgpool.conf
```

Specify the path to it when starting pgpool:

```{.bash data-prompt="$"}
$ pgpool -f <config-gile-path>/pgpool.conf
```

## pg_stat_monitor

Please refer to [`pg_stat_monitor`](pg-stat-monitor.md#setup) for setup steps.

## wal2json

After the installation, enable the following option in `postgresql.conf` configuration file before starting the service:

```
wal_level = logical
```

## Next steps 

[Connect to PostgreSQL :material-arrow-right:](connect.md){.md-button}