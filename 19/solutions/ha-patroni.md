> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/19/llms.txt).

# Patroni setup

## Install Percona Distribution for PostgreSQL and Patroni

Run the following commands as root or with `sudo` privileges on `node1`, `node2` and `node3`.

**On Debian / Ubuntu**

1. Disable the upstream `postgresql-19` package.

1. Install Percona Distribution for PostgreSQL package

   ```
   $ sudo apt install percona-postgresql-19
   ```

1. Install some Python and auxiliary packages to help with Patroni

   ```
   $ sudo apt install python3-pip python3-dev binutils
   ```

1. Install Patroni

   ```
   $ sudo apt install percona-patroni
   ```

1. Stop and disable all installed services:

   ```
   $ sudo systemctl stop {patroni,postgresql}
   $ sudo systemctl disable {patroni,postgresql}
   ```

1. Even though Patroni can use an existing Postgres installation, our recommendation for a **new cluster that has no data** is to remove the data directory. This forces Patroni to initialize a new Postgres cluster instance.

   ```
   $ sudo systemctl stop postgresql
   $ sudo rm -rf /var/lib/postgresql/19/main
   ```

**On RHEL and derivatives**

1. Install Percona Distribution for PostgreSQL package

   ```
   $ sudo yum install percona-postgresql19-server
   ```

1. Check the [platform specific notes for Patroni](https://docs.percona.com/postgresql/19/yum.html#for-percona-distribution-for-postgresql-packages)

1. Install some Python and auxiliary packages to help with Patroni and etcd

   ```
   $ sudo yum install python3-pip python3-devel binutils
   ```

1. Install Patroni

   ```
   $ sudo yum install percona-patroni
   ```

1. Stop and disable all installed services:

   ```
   $ sudo systemctl stop {patroni,postgresql-19}
   $ sudo systemctl disable {patroni,postgresql-19}
   ```

Important

**Don’t** initialize the cluster and start the `postgresql` service. The cluster initialization and setup are handled by Patroni during the bootsrapping stage.

## Configure Patroni

Run the following commands on all nodes. You can do this in parallel:

### Create environment variables

Environment variables simplify the config file creation:

1. Node name:

   ```
   $ export NODE_NAME=`hostname -f`
   ```

1. Node IP:

   ```
   $ export NODE_IP=`getent hosts $(hostname -f) | awk '{ print $1 }' | grep -v grep | grep -v '127.0.1.1'`
   ```

   - Check that the correct IP address is defined:

   ```
   $ echo $NODE_IP
   ```

   Sample output `node1`

   ```
   10.104.0.7
   ```

   If you have multiple IP addresses defined on your server and the environment variable contains the wrong one, you can manually redefine it. For example, run the following command for `node1`:

   ```
   $ NODE_IP=10.104.0.7
   ```

1. Create variables to store the `PATH`. Check the path to the `data` and `bin` folders on your operating system and change it for the variables accordingly:

   **Debian and Ubuntu**

   ```
   DATA_DIR="/var/lib/postgresql/19/main"
   PG_BIN_DIR="/usr/lib/postgresql/19/bin"
   ```

   **RHEL and derivatives**

   ```
   DATA_DIR="/var/lib/pgsql/data/"
   PG_BIN_DIR="/usr/pgsql-19/bin"
   ```

1. Patroni information:

   ```
   NAMESPACE="percona_lab"
   SCOPE="cluster_1"
   ```

### Create the directories required by Patroni

Create the directory to store the configuration file and make it owned by the `postgres` user.

```
$ sudo mkdir -p /etc/patroni/
$ sudo chown -R  postgres:postgres /etc/patroni/
```

### Patroni configuration file

Use the following command to create the `/etc/patroni/patroni.yml` configuration file and add the following configuration for every node:

```
echo "
namespace: ${NAMESPACE}
scope: ${SCOPE}
name: ${NODE_NAME}

restapi:
    listen: 0.0.0.0:8008
    connect_address: ${NODE_IP}:8008

etcd3:
    host: ${NODE_IP}:2379

bootstrap:
  # this section will be written into Etcd:/<namespace>/<scope>/config after initializing new cluster
  dcs:
      ttl: 30
      loop_wait: 10
      retry_timeout: 10
      maximum_lag_on_failover: 1048576

      postgresql:
          use_pg_rewind: true
          use_slots: true
          parameters:
              wal_level: replica
              hot_standby: "on"
              wal_keep_segments: 10
              max_wal_senders: 5
              max_replication_slots: 10
              wal_log_hints: "on"
              logging_collector: 'on'
              max_wal_size: '10GB'
              archive_mode: "on"
              archive_timeout: 600s
              archive_command: "cp -f %p /home/postgres/archived/%f"
          pg_hba:
              - local all all          peer
              - host replication replicator 127.0.0.1/32 trust
              - host replication replicator 10.0.0.0/8 scram-sha-256
              - host all all 0.0.0.0/0 scram-sha-256
              - host all all ::0/0 scram-sha-256
          recovery_conf:
              restore_command: cp /home/postgres/archived/%f %p

  # some desired options for 'initdb'
  initdb: # Note: It needs to be a list (some options need values, others are switches)
      - encoding: UTF8
      - data-checksums


postgresql:
    cluster_name: cluster_1
    listen: 0.0.0.0:5432
    connect_address: ${NODE_IP}:5432
    data_dir: ${DATA_DIR}
    bin_dir: ${PG_BIN_DIR}
    pgpass: /tmp/pgpass0
    authentication:
        replication:
            username: replicator
            password: replPasswd
        superuser:
            username: postgres
            password: qaz123
    parameters:
        unix_socket_directories: "/var/run/postgresql/"
    create_replica_methods:
        - basebackup
    basebackup:
        checkpoint: 'fast'

    watchdog:
      mode: required # Allowed values: off, automatic, required
      device: /dev/watchdog
      safety_margin: 5

tags:
    nofailover: false
    noloadbalance: false
    clonefrom: false
    nosync: false
" | sudo tee /etc/patroni/patroni.yml
```

Patroni configuration file

Let’s take a moment to understand the contents of the `patroni.yml` file.

The first section provides the details of the node and its connection ports. After that, we have the `etcd` service and its port details.

The `bootstrap.dcs` section stores cluster-wide settings in etcd. The `pg_hba` and `recovery_conf` entries live under `bootstrap.dcs.postgresql` so Patroni can manage `pg_hba.conf` and recovery settings consistently across all nodes. Authentication uses `scram-sha-256` instead of `md5`. The sample `restore_command` pairs with `archive_mode` and `archive_command` for WAL archiving. Additional database users can be created at any time with standard SQL commands; they are not defined in this file.

The `postgresql.watchdog` section enables the Linux watchdog for STONITH/fencing when a node hangs, which helps prevent split-brain scenarios.

### Systemd configuration

1. Check that the systemd unit file `percona-patroni.service` is created in `/etc/systemd/system`. If it is created, skip this step.

   If it’s **not created**, create it manually and specify the following contents within:

   /etc/systemd/system/percona-patroni.service

   ```
   [Unit]
   Description=Runners to orchestrate a high-availability PostgreSQL
   After=syslog.target network.target 

   [Service]
   Type=simple 

   User=postgres
   Group=postgres 

   # Start the patroni process
   ExecStart=/bin/patroni /etc/patroni/patroni.yml 

   # Send HUP to reload from patroni.yml
   ExecReload=/bin/kill -s HUP $MAINPID 

   # only kill the patroni process, not its children, so it will gracefully stop postgres
   KillMode=process 

   # Give a reasonable amount of time for the server to start up/shut down
   TimeoutSec=30 

   # Do not restart the service if it crashes, we want to manually inspect database on failure
   Restart=no 

   [Install]
   WantedBy=multi-user.target
   ```

1. Make `systemd` aware of the new service:

   ```
   $ sudo systemctl daemon-reload
   ```

1. Make sure you have the configuration file and the `systemd` unit file created on every node.

### Start Patroni

Now it’s time to start Patroni. You need the following commands on all nodes but **not in parallel**.

1. Start Patroni on `node1` first, wait for the service to come to live, and then proceed with the other nodes one-by-one, always waiting for them to sync with the primary node:

   ```
   $ sudo systemctl enable --now percona-patroni
   ```

   When Patroni starts, it initializes PostgreSQL (because the service is not currently running and the data directory is empty) following the directives in the bootstrap section of the configuration file.

1. Check the service to see if there are errors:

   ```
   $ sudo journalctl -fu percona-patroni
   ```

   See [Troubleshooting Patroni startup](#troubleshooting-patroni-startup) for guidelines in case of errors.

   If Patroni has started properly, you should be able to locally connect to a PostgreSQL node using the following command:

   ```
   $ sudo psql -U postgres

   psql (19.0)
   Type "help" for help.

   postgres=#
   ```

1. When all nodes are up and running, you can check the cluster status using the following command:

   ```
   $ sudo patronictl -c /etc/patroni/patroni.yml list
   ```

   The output resembles the following:

   Sample output node1

   ```
   + Cluster: cluster_1 (7440127629342136675) -----+----+-------+
   | Member | Host       | Role    | State     | TL | Lag in MB |
   +--------+------------+---------+-----------+----+-----------+
   | node1  | 10.0.100.1 | Leader  | running   |  1 |           |
   ```

   Sample output node3

   ```
   + Cluster: cluster_1 (7440127629342136675) -----+----+-------+
   | Member | Host       | Role    | State     | TL | Lag in MB |
   +--------+------------+---------+-----------+----+-----------+
   | node1  | 10.0.100.1 | Leader  | running   |  1 |           |
   | node2  | 10.0.100.2 | Replica | streaming |  1 |         0 |
   | node3  | 10.0.100.3 | Replica | streaming |  1 |         0 |
   +--------+------------+---------+-----------+----+-----------+
   ```

### Troubleshooting Patroni startup

A common error is Patroni complaining about the lack of proper entries in the `pg_hba.conf` file.

An example of such an error is `No pg_hba.conf entry for replication connection from host to <IP>, user replicator, no encryption`. This means that Patroni cannot connect to the node you’re adding to the cluster. To resolve this issue, add the IP addresses of the nodes to the cluster-wide `pg_hba` list under `postgresql` (stored in the DCS). For a **new cluster** that has not been bootstrapped yet, define the same `pg_hba` list under `bootstrap.dcs.postgresql` in `patroni.yml` before starting Patroni on the first node. Adjust the network CIDR to match your deployment; the sample below uses `10.0.0.0/8` for the lab network:

```
postgresql:
  pg_hba:
    - local all all          peer
    - host replication replicator 127.0.0.1/32 trust
    - host replication replicator 10.0.0.0/8 scram-sha-256
    - host replication replicator 10.0.100.2/32 scram-sha-256
    - host replication replicator 10.0.100.3/32 scram-sha-256
    - host all all 0.0.0.0/0 scram-sha-256
    - host all all ::0/0 scram-sha-256
  recovery_conf:
      restore_command: cp /home/postgres/archived/%f %p
```

For production use, we recommend adding nodes individually with specific `/32` entries as the more secure way. However, if your network is secure and you trust it, you can add the whole network these nodes belong to (for example, `10.0.0.0/8`) so all nodes from this network can connect to the Patroni cluster.

If the cluster is **already running**, changing `patroni.yml` alone does not update `pg_hba.conf`. Update the DCS configuration instead:

```
$ sudo patronictl -c /etc/patroni/patroni.yml edit-config
```

Add or fix the `pg_hba` entries in the editor, save, and Patroni applies the changes across the cluster. For a **new cluster** that has not been bootstrapped yet, fix `patroni.yml` before starting Patroni on the first node.

## Next steps

[pgBackRest setup](https://docs.percona.com/postgresql/19/solutions/pgbackrest.html)
