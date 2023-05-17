# Enable Percona Distribution for PostgreSQL extensions

Some extensions require additional configuration before using them with Percona Distribution for PostgreSQL. This sections provides configuration instructions per extension.

**Patroni**

Patroni is the third-party high availability solution for PostgreSQL. The [High Availability in PostgreSQL with Patroni](solutions/high-availability.md) chapter provides details about the solution overview and architecture deployment. 

While setting up a high availability PostgreSQL cluster with Patroni, you will need the following components:

- Patroni installed on every ``postresql`` node. 

- Distributed Configuration Store (DCS). Patroni supports such DCSs as ETCD, zookeeper, Kubernetes though [ETCD](https://etcd.io/) is the most popular one. It is available upstream as DEB packages for Debian 10, 11 and Ubuntu 18.04, 20.04, 22.04.  

     For CentOS 8, RPM packages for ETCD is available within Percona Distribution for PostreSQL.  You can install it using the following command: 

     ```{.bash data-prompt="$"}
     $ sudo yum install etcd python3-python-etcd
     ```
  
- [HAProxy](http://www.haproxy.org/).

See the configuration guidelines for [Debian and Ubuntu](solutions/ha-setup-apt.md) and [RHEL and CentOS](solutions/ha-setup-yum.md). 


!!! admonition "See also"

    - [Patroni documentation](https://patroni.readthedocs.io/en/latest/SETTINGS.html#settings)

    - Percona Blog: 

        - [PostgreSQL HA with Patroni: Your Turn to Test Failure Scenarios](https://www.percona.com/blog/2021/06/11/postgresql-ha-with-patroni-your-turn-to-test-failure-scenarios/) 
        
**pgBadger**

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

For details about each option, see [pdBadger documentation](https://github.com/darold/pgbadger/#POSTGRESQL-CONFIGURATION).

**pgAudit set-user**

Add the `set-user` to `shared_preload_libraries` in `postgresql.conf`. The recommended way is to use the [ALTER SYSTEM](https://www.postgresql.org/docs/14/sql-altersystem.html) command. [Connect to psql](#connect-to-the-postgresql-server) and use the following command:

```sql
ALTER SYSTEM SET shared_preload_libraries = 'set-user';
```

Start / restart the server to apply the configuration.

You can fine-tune user behavior with the [custom parameters](https://github.com/pgaudit/set_user#configuration-options) supplied with the extension.

**wal2json**

After the installation, enable the following option in `postgresql.conf` configuration file before starting the service:

```
wal_level = logical
```
