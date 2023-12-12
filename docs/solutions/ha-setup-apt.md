# Deploying PostgreSQL for high availability with Patroni on Debian or Ubuntu

This guide provides instructions on how to set up a highly available PostgreSQL cluster with Patroni on Debian or Ubuntu. 


## Preconditions

1. This is the example deployment suitable to be used for testing purposes in non-production environments. 
2. In this setup ETCD resides on the same hosts as Patroni. In production, consider deploying ETCD cluster on dedicated hosts or at least have separate disks for ETCD and PostgreSQL. This is because ETCD writes every request from the cluster to disk which can be CPU intensive and affects disk performance. See [hardware recommendations](https://etcd.io/docs/v3.6/op-guide/hardware/) for details.
3. For this setup, we will use the nodes running on Ubuntu 22.04 as the base operating system:

| Node name     | Public IP address | Internal IP address
|---------------|-------------------|--------------------
| node1         | 157.230.42.174    | 10.104.0.7
| node2         | 68.183.177.183    | 10.104.0.2
| node3         | 165.22.62.167     | 10.104.0.8
| HAProxy-demo  | 134.209.111.138   | 10.104.0.6


!!! note

    In a production (or even non-production) setup, the PostgreSQL nodes will be within a private subnet without any public connectivity to the Internet, and the HAProxy will be in a different subnet that allows client traffic coming only from a selected IP range. To keep things simple, we have implemented this architecture in a DigitalOcean VPS environment, and each node can access the other by its internal, private IP. 


## Initial setup 

It’s not necessary to have name resolution, but it makes the whole setup more readable and less error prone. Here, instead of configuring a DNS, we use a local name resolution by updating the file /etc/hosts. By resolving their hostnames to their IP addresses, we make the nodes aware of each other’s names and allow their seamless communication.

1. Run the following command on each node. Change the node name to `node1`, `node2` and `node3` respectively:

    ```{.bash data-prompt="$"}
    $ sudo hostnamectl set-hostname node1
    ```

2. Modify the `/etc/hosts` file of each PostgreSQL node to include the hostnames and IP addresses of the remaining nodes. Add the following at the end of the `/etc/hosts` file on all nodes:

    === "node1"    

        ```text hl_lines="3 4"
        # Cluster IP and names 
        10.104.0.1 node1 
        10.104.0.2 node2 
        10.104.0.3 node3
        ```    

    === "node2"    

        ```text hl_lines="2 4"
        # Cluster IP and names 
        10.104.0.1 node1 
        10.104.0.2 node2 
        10.104.0.3 node3
        ```    

    === "node3"    

        ```text hl_lines="2 3"
        # Cluster IP and names 
        10.104.0.1 node1 
        10.104.0.2 node2 
        10.104.0.3 node3
        ```    

    === "HAproxy-demo"    

        The HAProxy instance should have the name resolution for all the three nodes in its `/etc/hosts` file. Add the following lines at the end of the file:    

        ```text hl_lines="4 5 6"
        # Cluster IP and names
        10.104.0.6 HAProxy-demo
        10.104.0.1 node1
        10.104.0.2 node2
        10.104.0.3 node3
        ```


### Install the software

Run the following commands on node1`, `node2` and `node3`:

1. Install Percona Distribution for PostgreSQL
    
    * [Install `percona-release`](https://www.percona.com/doc/percona-repo-config/installing.html).

    * Enable the repository:

       ```{.bash data-prompt="$"}
       $ sudo percona-release setup ppg14
       ```

    * [Install Percona Distribution for PostgreSQL packages](../apt.md).

2. Install some Python and auxiliary packages to help with Patroni and ETCD
    
    ```{.bash data-prompt="$"}
    $ sudo apt install python3-pip python3-dev binutils
    ```

3. Install ETCD, Patroni, pgBackRest packages:


    ```{.bash data-prompt="$"}
    $ sudo apt install percona-patroni \
    etcd etcd-server etcd-client \
    percona-pgbackrest
    ```

4. Stop and disable all installed services:
    
    ```{.bash data-prompt="$"}
    $ sudo systemctl stop {etcd,patroni,postgresql}
    $ systemctl disable {etcd,patroni,postgresql}
    ```

5. Even though Patroni can use an existing Postgres installation, remove the data directory to force it to initialize a new Postgres cluster instance.

   ```{.bash data-promp="$"}
   $ sudo systemctl stop postgresql
   $ sudo rm -rf /var/lib/postgresql/14/main
   ```

## Configure ETCD distributed store  

The distributed configuration store helps establish a consensus among nodes during a failover and will manage the configuration for the three PostgreSQL instances. Although Patroni can work with other distributed consensus stores (i.e., Zookeeper, Consul, etc.), the most commonly used one is `etcd`. 

The `etcd` cluster is first started in one node and then the subsequent nodes are added to the first node using the `add `command. The configuration is stored in the `/etc/default/etcd` file.

### Configure `node1` 

1. Back up the configuration file

    ```{.bash data-promp="$"}
    $ sudo mv /etc/default/etcd /etc/default/etcd.orig
    ```

2. Export environment variables to simplify the config file creation

    * Node name:

       ```{.bash data-prompt="$"}
       $ export NODE_NAME=`hostname -f`
       ```

    * Node IP:

       ```{.bash data-prompt="$"}
       $ export NODE_IP=`hostname -i | awk '{print $1}'`
       ```
    
    * Initial cluster token for the ETCD cluster during bootstrap:

       ```{.bash data-prompt="$"}
       $ export ETCD_TOKEN='PostgreSQL_HA_Cluster_1'
       ```

    * ETCD data directory:

       ```{.bash data-prompt="$"}
       $ export ETCD_DATA_DIR='/var/lib/etcd/postgresql'
       ```

3. Modify the `/etc/default/etcd` configuration file as follows:. 

    ```{.bash data-prompt="$"} 
    $ echo "
    ETCD_NAME=${NODE_NAME}
    ETCD_INITIAL_CLUSTER="${NODE_NAME}=http://${NODE_IP}:2380"
    ETCD_INITIAL_CLUSTER_STATE="new"
    ETCD_INITIAL_CLUSTER_TOKEN="${ETCD_TOKEN}"
    ETCD_INITIAL_ADVERTISE_PEER_URLS="http://${NODE_IP}:2380"
    ETCD_DATA_DIR="${ETCD_DATA_DIR}"
    ETCD_LISTEN_PEER_URLS="http://${NODE_IP}:2380"
    ETCD_LISTEN_CLIENT_URLS="http://${NODE_IP}:2379,http://localhost:2379"
    ETCD_ADVERTISE_CLIENT_URLS="http://${NODE_IP}:2379"
    " | sudo tee -a /pg_ha/config/etcd.conf 
    ```

4. Start the `etcd` service to apply the changes on `node1`.

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable --now etcd
    $ sudo systemctl start etcd
    $ sudo systemctl status etcd
    ```

5. Check the etcd cluster members on `node1`:

    * On `node3`, the `ETCD_INITIAL_CLUSTER` parameter includes the IP addresses of all three nodes:

      ```text
      ETCD_NAME=node3
      ETCD_INITIAL_CLUSTER="node1=http://10.104.0.7:2380,node2=http://10.104.0.2:2380,node3=http://10.104.0.8:2380"
      ETCD_INITIAL_CLUSTER_TOKEN="devops_token"
      ETCD_INITIAL_CLUSTER_STATE="existing"
      ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.104.0.8:2380"
      ETCD_DATA_DIR="/var/lib/etcd/postgresql"
      ETCD_LISTEN_PEER_URLS="http://10.104.0.8:2380"
      ETCD_LISTEN_CLIENT_URLS="http://10.104.0.8:2379,http://localhost:2379"
      ETCD_ADVERTISE_CLIENT_URLS="http://10.104.0.8:2379"
      …
      ```  

6. Add the `node2` to the cluster. Run the following command on `node1`:

    ```{.bash data-promp="$"}
    $ sudo etcdctl member add node2 http://10.104.0.2:2380
    $ sudo etcdctl member add node3 http://10.104.0.8:2380
    ```

    The output resembles the following one:
    
    ```{.text .no-copy}
    Added member named node2 with ID 10042578c504d052 to cluster

    ETCD_NAME="node2"
    ETCD_INITIAL_CLUSTER="node2=http://10.104.0.2:2380,node1=http://10.104.0.1:2380"
    ETCD_INITIAL_CLUSTER_STATE="existing"
    ```
### Configure `node2`

1. Back up the configuration file and export environment variables as described in steps 1-2 of the [`node1` configuration](#configure-node1) 
2. Edit the `/etc/default/etcd` configuration file on `node2`. Use the result of the `add` command on `node1` to change the configuration file as follows:

    ```{.bash data-prompt="$"}
    $ echo "
    ETCD_NAME="node2"
    ETCD_INITIAL_CLUSTER="node1=http://10.0.100.1:2380,node2=http://10.0.100.2:2380"
    ETCD_INITIAL_CLUSTER_STATE="existing"

    ETCD_INITIAL_CLUSTER_TOKEN="${ETCD_TOKEN}"
    ETCD_INITIAL_ADVERTISE_PEER_URLS="http://${NODE_IP}:2380"
    ETCD_DATA_DIR="${ETCD_DATA_DIR}"
    ETCD_LISTEN_PEER_URLS="http://${NODE_IP}:2380"
    ETCD_LISTEN_CLIENT_URLS="http://${NODE_IP}:2379,http://localhost:2379"
    ETCD_ADVERTISE_CLIENT_URLS="http://${NODE_IP}:2379"
    " | sudo tee -a /pg_ha/config/etcd.conf
    ```

3. Start the `etcd` service to apply the changes on `node2`:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable --now etcd
    $ sudo systemctl start etcd
    $ sudo systemctl status etcd
    ```

### Configure `node3`

1. Add `node3` to the cluster. **Run the following command on `node1`**

    ```{.bash data-prompt="$"}
    $ sudo etcdctl member add node3 http://10.104.0.3:2380
    ```

2. On `node3`, back up the configuration file and export environment variables as described in steps 1-2 of the [`node1` configuration](#configure-node1) 
3. Modify the `/etc/default/etcd` configuration file and add the output of the `add` command:

    ```{.bash data-prompt="$"}
    $ echo "
    ETCD_NAME=node3
    ETCD_INITIAL_CLUSTER="node1=http://10.104.0.1:2380,node2=http://10.104.0.2:2380,node3=http://10.104.0.3:2380"
    ETCD_INITIAL_CLUSTER_STATE="existing"  
    ETCD_INITIAL_CLUSTER_TOKEN="${ETCD_TOKEN}"
    ETCD_INITIAL_ADVERTISE_PEER_URLS="http://${NODE_IP}:2380"
    ETCD_DATA_DIR="${ETCD_DATA_DIR}"
    ETCD_LISTEN_PEER_URLS="http://${NODE_IP}:2380"
    ETCD_LISTEN_CLIENT_URLS="http://${NODE_IP}:2379,http://localhost:2379"
    ETCD_ADVERTISE_CLIENT_URLS="http://${NODE_IP}:2379"
    " | sudo tee -a /pg_ha/config/etcd.conf
    ```  

4. Start the `etcd` service on `node3`:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable --now etcd
    $ sudo systemctl start etcd
    $ sudo systemctl status etcd
    ```

5. Check the etcd cluster members.
    
    ```{.bash data-promp="$"}
    $ sudo etcdctl member list
    ```

    The output resembles the following:

    ```
    21d50d7f768f153a: name=node1 peerURLs=http://10.104.0.7:2380 clientURLs=http://10.104.0.7:2379 isLeader=true
    af4661d829a39112: name=node2 peerURLs=http://10.104.0.2:2380 clientURLs=http://10.104.0.2:2379 isLeader=false
    e3f3c0c1d12e9097: name=node3 peerURLs=http://10.104.0.8:2380 clientURLs=http://10.104.0.8:2379 isLeader=false
    ```

## Configure Patroni

Run the following commands on all nodes. You can do this in parallel:

1. Export and create environment variables to simplify the config file creation:

    * Node name:

       ```{.bash data-prompt="$"}
       $ export NODE_NAME=`hostname -f`
       ```

    * Node IP:

       ```{.bash data-prompt="$"}
       $ export NODE_IP=`hostname -i | awk '{print $1}'`
       ```
   
    * Create variables to store the PATH:

       ```bash
       DATA_DIR="/var/lib/postgresql/14/main"
       PG_BIN_DIR="/usr/lib/postgresql/14/bin"
       ```

       **NOTE**: Check the path to the data and bin folders on your operating system and change it for the variables accordingly.

    * Patroni information:

       ```bash
       NAMESPACE="percona_lab"
       SCOPE="cluster_1
       ```

2. Create the `/etc/patroni/patroni.yml` configuration file. The file holds the default configuration values for a PostgreSQL cluster and will reflect the current cluster setup. Add the following configuration for `node1`:

    ```bash
    echo "
    namespace: ${NAMESPACE}
    scope: ${SCOPE}
    name: ${NODE_NAME}

    restapi:
        listen: 0.0.0.0:8008
        connect_address: ${NODE_IP}:8008

    etcd:
        host: ${NODE_IP}:2379

    bootstrap:
      # this section will be written into Etcd:/<namespace>/<scope>/config after initializing new cluster
      dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
        slots:
              percona_cluster_1:
              type: physical

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

      # some desired options for 'initdb'
      initdb:  # Note: It needs to be a list (some options need values, others are switches)
      - encoding: UTF8
      - data-checksums

      pg_hba:  # Add following lines to pg_hba.conf after running 'initdb'
      - host replication replicator 127.0.0.1/32 trust
      - host replication replicator 0.0.0.0/0 md5
      - host all all 0.0.0.0/0 md5
      - host all all ::0/0 md5

      # Additional script to be launched after initial cluster creation (will be passed the connection URL as parameter)
    # post_init: /usr/local/bin/setup_cluster.sh
      # Some additional users users which needs to be created after initializing new cluster
      users:
          admin:
              password: qaz123
              options:
                  - createrole
                  - createdb
          percona:
              password: qaz123
              options:
                  - createrole
                  - createdb 

    postgresql:
        cluster_name: cluster_1
        listen: 0.0.0.0:5432
        connect_address: ${NODE_IP}:5432
        data_dir: ${DATADIR}
        bin_dir: ${PG_BIN_DIR}
        pgpass: /tmp/pgpass
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

    tags:
        nofailover: false
        noloadbalance: false
        clonefrom: false
        nosync: false
    " | sudo tee -a /etc/patroni/patroni.yml
    ```

    ??? admonition "Patroni configuration file"

        Let’s take a moment to understand the contents of the `patroni.yml` file. 

        The first section provides the details of the node and its connection ports. After that, we have the `etcd` service and its port details.

        Following these, there is a `bootstrap` section that contains the PostgreSQL configurations and the steps to run once the database is initialized. The `pg_hba.conf` entries specify all the other nodes that can connect to this node and their authentication mechanism. 

3. Check that the `systemd` unit file `patroni.service` is created in `/etc/systemd/system`. If it is created, skip this step. 

    If it's **not** created, create it manually and specify the following contents within: 

     ```ini title="/etc/systemd/system/patroni.service"
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

4. Make `systemd` aware of the new service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl daemon-reload
    ```

5. Now it's time to start Patroni. You need the following commands on all nodes but not in parallel. Start with the `node1` first, wait for the service to come to live, and then proceed with the other nodes one-by-one, always waiting for them to sync with the primary node:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable --now patroni
    $ sudo systemctl restart patroni
    ```
   
    When Patroni starts, it initializes PostgreSQL (because the service is not currently running and the data directory is empty) following the directives in the bootstrap section of the configuration file. 

6. Check the service to see if there are errors:

    ```{.bash data-prompt="$"}
    $ sudo journalctl -fu patroni
    ```

    A common error is Patroni complaining about the lack of proper entries in the pg_hba.conf file. If you see such errors, you must manually add or fix the entries in that file and then restart the service.

    Changing the patroni.yml file and restarting the service will not have any effect here because the bootstrap section specifies the configuration to apply when PostgreSQL is first started in the node. It will not repeat the process even if the Patroni configuration file is modified and the service is restarted.

7. Check the cluster:
 
    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/patroni.yml list $SCOPE
    ```

    The output on `node1` resembles the following:

    ```{.text .no-copy}
    + Cluster: cluster_1 --+---------+---------+----+-----------+
    | Member | Host        | Role    | State   | TL | Lag in MB |
    +--------+-------------+---------+---------+----+-----------+
    | node-1 | 10.0.100.1  | Leader  | running |  1 |           |
    +--------+-------------+---------+---------+----+-----------+
    ```

    On the remaining nodes:
    
    ```{.text .no-copy}
    + Cluster: cluster_1 --+---------+---------+----+-----------+
    | Member | Host        | Role    | State   | TL | Lag in MB |
    +--------+-------------+---------+---------+----+-----------+
    | node-1 | 10.0.100.1  | Leader  | running |  1 |           |
    | node-2 | 10.0.100.2  | Replica | running |  1 |         0 |
    +--------+-------------+---------+---------+----+-----------+
    ```

If Patroni has started properly, you should be able to locally connect to a PostgreSQL node using the following command:

```{.bash data-prompt="$"}
$ sudo psql -U postgres
```

The command output looks like the following:

```
psql (14.10)

Type "help" for help.

postgres=#
```

## Configure HAProxy

HAProxy node will accept client connection requests and route those to the active node of the PostgreSQL cluster. This way, a client application doesn’t have to know what node in the underlying cluster is the current primary. All it needs to do is to access a single HAProxy URL and send its read/write requests there. Behind-the-scene, HAProxy routes the connection to a healthy node (as long as there is at least one healthy node available) and ensures that client application requests are never rejected. 

HAProxy is capable of routing write requests to the primary node and read requests - to the secondaries in a round-robin fashion so that no secondary instance is unnecessarily loaded. To make this happen, provide different ports in the HAProxy configuration file. In this deployment, writes are routed to port 5000 and reads  - to port 5001.

1. Install HAProxy on the `HAProxy-demo` node:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-haproxy
    ```

2. The HAProxy configuration file path is: `/etc/haproxy/haproxy.cfg`. Specify the following configuration in this file.

    ```
    global
        maxconn 100

    defaults
        log global
        mode tcp
        retries 2
        timeout client 30m
        timeout connect 4s
        timeout server 30m
        timeout check 5s

    listen stats
        mode http
        bind *:7000
        stats enable
        stats uri /

    listen primary
        bind *:5000
        option httpchk /primary 
        http-check expect status 200
        default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
        server node1 node1:5432 maxconn 100 check port 8008
        server node2 node2:5432 maxconn 100 check port 8008
        server node3 node3:5432 maxconn 100 check port 8008

    listen standbys
        balance roundrobin
        bind *:5001
        option httpchk /replica 
        http-check expect status 200
        default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
        server node1 node1:5432 maxconn 100 check port 8008
        server node2 node2:5432 maxconn 100 check port 8008
        server node3 node3:5432 maxconn 100 check port 8008
    ```


    HAProxy will use the REST APIs hosted by Patroni to check the health status of each PostgreSQL node and route the requests appropriately. 

3. Restart HAProxy:
    
    ```{.bash data-prompt="$"}
    $ sudo systemctl restart haproxy
    ```

4. Check the HAProxy logs to see if there are any errors:
   
    ```{.bash data-prompt="$"}
    $ sudo journalctl -u haproxy.service -n 100 -f
    ```

## Next steps

[Configure pgBackRest](pgbackrest.md){.md-button}