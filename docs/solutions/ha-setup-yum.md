# Deploying PostgreSQL for high availability with Patroni on RHEL or CentOS

This guide provides instructions on how to set up a highly available PostgreSQL cluster with Patroni on Red Hat Enterprise Linux or CentOS. 


## Considerations

1. This is the example deployment suitable to be used for testing purposes in non-production environments. 
2. In this setup ETCD resides on the same hosts as Patroni. In production, consider deploying ETCD cluster on dedicated hosts because ETCD writes every request from the cluster to disk which requires significant amount of disk space. See [hardware recommendations](https://etcd.io/docs/v3.6/op-guide/hardware/) for details.
3. For this setup, we use the nodes running on Red Hat Enterprise Linux 8 as the base operating system:

    | Node name     | Application       | IP address
    |---------------|-------------------|--------------------
    | node1         | Patroni, PostgreSQL, ETCD    | 10.104.0.1
    | node2         | Patroni, PostgreSQL, ETCD    | 10.104.0.2
    | node3         | Patroni, PostgreSQL, ETCD     | 10.104.0.3
    | HAProxy-demo  | HAProxy           | 10.104.0.6


!!! note

    Ideally, in a production (or even non-production) setup, the PostgreSQL and ETCD nodes will be within a private subnet without any public connectivity to the Internet, and the HAProxy will be in a different subnet that allows client traffic coming only from a selected IP range. To keep things simple, we have implemented this architecture in a private environment, and each node can access the other by its internal, private IP.  

## Preparation 

### Set up hostnames in the `/etc/hosts` file

It's not necessary to have name resolution, but it makes the whole setup more readable and less error prone. Here, instead of configuring a DNS, we use a local name resolution by updating the file `/etc/hosts`. By resolving their hostnames to their IP addresses, we make the nodes aware of each other's names and allow their seamless communication. 

Modify the `/etc/hosts` file of each PostgreSQL node to include the hostnames and IP addresses of the remaining nodes. Add the following at the end of the `/etc/hosts` file on all nodes:

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

## Install Percona Distribution for PostgreSQL

Install Percona Distribution for PostgreSQL on `node1`, `node2` and `node3` from Percona repository:

1. [Install `percona-release`](https://www.percona.com/doc/percona-repo-config/installing.html).
2. Enable the repository:

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup ppg11
    ```

3. [Install Percona Distribution for PostgreSQL packages](../installing.md#on-red-hat-enterprise-linux-and-centos-using-yum).

!!! important

    **Don't** initialize the cluster and start the `postgresql` service. The cluster initialization and setup are handled by Patroni during the bootsrapping stage.

## Configure ETCD distributed store  

The distributed configuration store provides a reliable way to store data that needs to be accessed by large scale distributed systems. The most popular implementation of the distributed configuration store is ETCD. ETCD is deployed as a cluster for fault-tolerance and requires an odd number of members (n/2+1) to agree on updates to the cluster state. An ETCD cluster helps establish a consensus among nodes during a failover and manages the configuration for the three PostgreSQL instances.

The `etcd` cluster is first started in one node and then the subsequent nodes are added to the first node using the `add `command. The configuration is stored in the `/etc/etcd/etcd.conf` configuration file.

1. Install `etcd` on every PostgreSQL node. For CentOS 8, the `etcd` packages are available from Percona repository:

   - [Install `percona-release`](https://www.percona.com/doc/percona-repo-config/installing.html).
   - Enable the repository:

      ```{.bash data-prompt="$"}
      $ sudo percona-release setup ppg12
      ```
   
   - Install the etcd packages using the following command:

      ```{.bash data-prompt="$"}
      $ sudo yum install etcd python3-python-etcd
      ```

2. Configure ETCD on `node1`.

     Backup the `etcd.conf` file:
    
     ```{.bash data-promp="$"}
     sudo mv /etc/etcd/etcd.conf /etc/etcd/etcd.conf.orig
     ```

     Modify the `/etc/etcd/etcd.conf` configuration file:

     ```text
     [Member]
     ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
     ETCD_LISTEN_PEER_URLS="http://10.104.0.1:2380,http://localhost:2380" 
     ETCD_LISTEN_CLIENT_URLS="http://10.104.0.1:2379,http://localhost:2379"  

     ETCD_NAME="node1"
     ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.104.0.1:2380"
     ETCD_ADVERTISE_CLIENT_URLS="http://10.104.0.1:2379"
     ETCD_INITIAL_CLUSTER="node1=http://10.104.0.1:2380"
     ETCD_INITIAL_CLUSTER_TOKEN="percona-etcd-cluster"
     ETCD_INITIAL_CLUSTER_STATE="new"
     ```

3.  Start the `etcd` to apply the changes on `node1`:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable etcd
    $ sudo systemctl start etcd
    $ sudo systemctl status etcd
    ```

5. Check the etcd cluster members on `node1`.
    
    ```{.bash data-prompt="$"}
    $ sudo etcdctl member list
    ```

    The output resembles the following:

    ```{.text .no-copy}
    21d50d7f768f153a: name=default peerURLs=http://10.104.0.5:2380 clientURLs=http://10.104.0.5:2379 isLeader=true
    ```

6. Add `node2` to the cluster. Run the following command on `node1`:
    
    ```{.bash data-prompt="$"}
    $ sudo etcdctl member add node2 http://10.104.0.2:2380
    ```

    The output resembles the following one:
    
    ```{.text .no-copy}
    Added member named node2 with ID 10042578c504d052 to cluster

    ETCD_NAME="node2"
    ETCD_INITIAL_CLUSTER="node2=http://10.104.0.2:2380,node1=http://10.104.0.1:2380"
    ETCD_INITIAL_CLUSTER_STATE="existing"
    ```

7. Edit the `/etc/etcd/etcd.conf` configuration file on `node2` and add the output from the `add` command:

    ```text 
    [Member]
    ETCD_NAME="node2"
    ETCD_INITIAL_CLUSTER="node2=http://10.104.0.2:2380,node1=http://10.104.0.1:2380"
    ETCD_INITIAL_CLUSTER_STATE="existing"
    ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
    ETCD_INITIAL_CLUSTER_TOKEN="percona-etcd-cluster"
    ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.104.0.2:2380"
    ETCD_LISTEN_PEER_URLS="http://10.104.0.2:2380"
    ETCD_LISTEN_CLIENT_URLS="http://10.104.0.2:2379,http://localhost:2379"
    ETCD_ADVERTISE_CLIENT_URLS="http://10.104.0.2:2379"
    ```

8. Start the `etcd` to apply the changes on `node2`:
    
    ```{.bash data-promp="$"}
    $ sudo systemctl enable etcd
    $ sudo systemctl start etcd
    $ sudo systemctl status etcd
    ```

9. Add `node3` to the cluster. Run the following command on `node1`:
    
    ```{.bash data-prompt="$"}
    $ sudo etcdctl member add node3 http://10.104.0.3:2380
    ```

10. Configure `etcd` on `node3`. Edit the `/etc/etcd/etcd.conf` configuration file on `node3` and add the output from the `add` command as follows:

      ```text
      ETCD_NAME=node3
      ETCD_INITIAL_CLUSTER="node1=http://10.104.0.1:2380,node2=http://10.104.0.2:2380,node3=http://10.104.0.3:2380"
      ETCD_INITIAL_CLUSTER_STATE="existing"

      ETCD_INITIAL_CLUSTER_TOKEN="percona-etcd-cluster"
      ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.104.0.3:2380"
      ETCD_DATA_DIR="/var/lib/etcd/postgresql"
      ETCD_LISTEN_PEER_URLS="http://10.104.0.3:2380"
      ETCD_LISTEN_CLIENT_URLS="http://10.104.0.3:2379,http://localhost:2379"
      ETCD_ADVERTISE_CLIENT_URLS="http://10.104.0.3:2379"
      …
      ```  

11. Start the `etcd` service on `node3`:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable etcd
    $ sudo systemctl start etcd
    $ sudo systemctl status etcd
    ```

12. Check the etcd cluster members.
    
    ```{.bash data-prompt="$"}
    $ sudo etcdctl member list
    ```

    The output resembles the following:

    ```
    2d346bd3ae7f07c4: name=node2 peerURLs=http://10.104.0.2:2380 clientURLs=http://10.104.0.2:2379 isLeader=false
    8bacb519ebdee8db: name=node3 peerURLs=http://10.104.0.3:2380 clientURLs=http://10.104.0.3:2379 isLeader=false
    c5f52ea2ade25e1b: name=node1 peerURLs=http://10.104.0.1:2380 clientURLs=http://10.104.0.1:2379 isLeader=true
    ``` 


## Configure Patroni

1. Install Patroni on every PostgreSQL node:

    ```{.bash data-prompt="$"}
    $ sudo yum install percona-patroni
    ```

2. Install the Python module that enables Patroni to communicate with ETCD.

    ```{.bash data-prompt="$"}
    $ sudo python3 -m pip install patroni[etcd]
    ```

3. Create the directories required by Patroni

    * Create the directory to store the configuration file and make it owned by the `postgres` user.

      ```{.bash data-prompt="$"}
      $ sudo mkdir -p /etc/patroni/
      $ sudo chown -R  postgres:postgres /etc/patroni/
      ``` 

    * Create the data directory to store PostgreSQL data. Change its ownership to the `postgres` user and restrict the access to it 

     ```{.bash data-prompt="$"}
     $ sudo mkdir /data/pgsql -p
     $ sudo chown -R postgres:postgres /data/pgsql
     $ sudo chmod 700 /data/pgsql
     ```

4. Create the `/etc/patroni/patroni.yml` with the following configuration:
 
    ```yaml
    namespace: percona_lab
    scope: cluster_1
    name: node1

    restapi:
        listen: 0.0.0.0:8008
        connect_address: 10.104.0.1:8008   # PostgreSQL node IP address

    etcd:
        host: 10.104.0.1:2379  # ETCD node IP address

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
     initdb: # Note: It needs to be a list (some options need values, others are switches)
         - encoding: UTF8
         - data-checksums
     pg_hba: # Add following lines to pg_hba.conf after running 'initdb'
         - host replication replicator 127.0.0.1/32 trust
         - host replication replicator 0.0.0.0/0 md5
         - host all all 0.0.0.0/0 md5
         - host all all ::0/0 md5
     # Some additional users which needs to be created after initializing new cluster
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
      connect_address: 10.104.0.1:5432
      data_dir: /data/pgsql
      bin_dir: /usr/pgsql-12/bin
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
    ```

5. Create the configuration files for `node2` and `node3`. Replace the **node name and IP address** of `node1` to those of `node2` and `node3`, respectively.

6. Create the systemd unit file `patroni.service` in `/etc/systemd/system`. 

    ```{.bash data-prompt="$"}
    $ sudo vim /etc/systemd/system/patroni.service
    ```

    Add the following contents in the file:
   
    ```ini
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

7. Make systemd aware of the new service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable patroni
    $ sudo systemctl start patroni
    ```

    !!! admonition "Troubleshooting Patroni"

        To ensure that Patroni has started properly, check the logs using the following command:

        ```{.bash data-prompt="$"}
        $ sudo journalctl -u patroni.service -n 100 -f
        ```

        The output shouldn't show any errors:

        ```
        …

        Sep 23 12:50:21 node01 systemd[1]: Started PostgreSQL high-availability manager.
        Sep 23 12:50:22 node01 patroni[10119]: 2021-09-23 12:50:22,022 INFO: Selected new etcd server http://10.104.0.2:2379
        Sep 23 12:50:22 node01 patroni[10119]: 2021-09-23 12:50:22,029 INFO: No PostgreSQL configuration items changed, nothing to reload.
        Sep 23 12:50:22 node01 patroni[10119]: 2021-09-23 12:50:22,168 INFO: Lock owner: None; I am node1
        Sep 23 12:50:22 node01 patroni[10119]: 2021-09-23 12:50:22,177 INFO: trying to bootstrap a new cluster
        Sep 23 12:50:22 node01 patroni[10140]: The files belonging to this database system will be owned by user "postgres".
        Sep 23 12:50:22 node01 patroni[10140]: This user must also own the server process.
        Sep 23 12:50:22 node01 patroni[10140]: The database cluster will be initialized with locale "C.UTF-8".
        Sep 23 12:50:22 node01 patroni[10140]: The default text search configuration will be set to "english".
        Sep 23 12:50:22 node01 patroni[10140]: Data page checksums are enabled.
        Sep 23 12:50:22 node01 patroni[10140]: creating directory /var/lib/postgresql/12/main ... ok
        Sep 23 12:50:22 node01 patroni[10140]: creating subdirectories ... ok
        Sep 23 12:50:22 node01 patroni[10140]: selecting dynamic shared memory implementation ... posix
        Sep 23 12:50:22 node01 patroni[10140]: selecting default max_connections ... 100
        Sep 23 12:50:22 node01 patroni[10140]: selecting default shared_buffers ... 128MB
        Sep 23 12:50:22 node01 patroni[10140]: selecting default time zone ... Etc/UTC
        Sep 23 12:50:22 node01 patroni[10140]: creating configuration files ... ok
        Sep 23 12:50:22 node01 patroni[10140]: running bootstrap script ... ok
        Sep 23 12:50:23 node01 patroni[10140]: performing post-bootstrap initialization ... ok
        Sep 23 12:50:23 node01 patroni[10140]: syncing data to disk ... ok
        Sep 23 12:50:23 node01 patroni[10140]: initdb: warning: enabling "trust" authentication for local connections
        Sep 23 12:50:23 node01 patroni[10140]: You can change this by editing pg_hba.conf or using the option -A, or
        Sep 23 12:50:23 node01 patroni[10140]: --auth-local and --auth-host, the next time you run initdb.
        Sep 23 12:50:23 node01 patroni[10140]: Success. You can now start the database server using:
        Sep 23 12:50:23 node01 patroni[10140]:     /usr/lib/postgresql/12/bin/pg_ctl -D /var/lib/postgresql/12/main -l logfile start
        Sep 23 12:50:23 node01 patroni[10156]: 2021-09-23 12:50:23.672 UTC [10156] LOG:  redirecting log output to logging collector process
        Sep 23 12:50:23 node01 patroni[10156]: 2021-09-23 12:50:23.672 UTC [10156] HINT:  Future log output will appear in directory "log".
        Sep 23 12:50:23 node01 patroni[10119]: 2021-09-23 12:50:23,694 INFO: postprimary pid=10156
        Sep 23 12:50:23 node01 patroni[10165]: localhost:5432 - accepting connections
        Sep 23 12:50:23 node01 patroni[10167]: localhost:5432 - accepting connections
        Sep 23 12:50:23 node01 patroni[10119]: 2021-09-23 12:50:23,743 INFO: establishing a new patroni connection to the postgres cluster
        Sep 23 12:50:23 node01 patroni[10119]: 2021-09-23 12:50:23,757 INFO: running post_bootstrap
        Sep 23 12:50:23 node01 patroni[10119]: 2021-09-23 12:50:23,767 INFO: Software Watchdog activated with 25 second timeout, timing slack 15 seconds
        Sep 23 12:50:23 node01 patroni[10119]: 2021-09-23 12:50:23,793 INFO: initialized a new cluster
        Sep 23 12:50:33 node01 patroni[10119]: 2021-09-23 12:50:33,810 INFO: no action. I am (node1) the leader with the lock
        Sep 23 12:50:33 node01 patroni[10119]: 2021-09-23 12:50:33,899 INFO: no action. I am (node1) the leader with the lock
        Sep 23 12:50:43 node01 patroni[10119]: 2021-09-23 12:50:43,898 INFO: no action. I am (node1) the leader with the lock
        Sep 23 12:50:53 node01 patroni[10119]: 2021-09-23 12:50:53,894 INFO: no action. I am (node1) the leader with the 
        ```

        A common error is Patroni complaining about the lack of proper entries in the pg_hba.conf file. If you see such errors, you must manually add or fix the entries in that file and then restart the service.

        Changing the patroni.yml file and restarting the service will not have any effect here because the bootstrap section specifies the configuration to apply when PostgreSQL is first started in the node. It will not repeat the process even if the Patroni configuration file is modified and the service is restarted. 

        If Patroni has started properly, you should be able to locally connect to a PostgreSQL node using the following command:

        ```{.bash data-prompt="$"}
        $ sudo psql -U postgres

        psql (12.3)
        Type "help" for help.

        postgres=#
        ```

9. Configure, enable and start Patroni on the remaining nodes.
10. When all nodes are up and running, you can check the cluster status using the following command:

   ```{.bash data-prompt="$"}
   $ sudo patronictl -c /etc/patroni/patroni.yml list
   

   + Cluster: postgres (7011110722654005156) -----------+
   | Member | Host  | Role    | State   | TL | Lag in MB |
   +--------+-------+---------+---------+----+-----------+
   | node1  | node1 | Leader  | running |  1 |           |
   | node2  | node2 | Replica | running |  1 |         0 |
   | node3  | node3 | Replica | running |  1 |         0 |
   +--------+-------+---------+---------+----+-----------+
   ```

## Configure HAProxy

HAproxy is the load balancer and the single point of entry to your PostgreSQL cluster for client applications. A client application accesses the HAPpoxy URL and sends its read/write requests there. Behind-the-scene, HAProxy routes write requests to the primary node and read requests - to the secondaries in a round-robin fashion so that no secondary instance is unnecessarily loaded. To make this happen, provide different ports in the HAProxy configuration file. In this deployment, writes are routed to port 5000 and reads  - to port 5001

This way, a client application doesn’t know what node in the underlying cluster is the current primary. HAProxy sends connections to a healthy node (as long as there is at least one healthy node available) and ensures that client application requests are never rejected. 

1. Install HAProxy on the `HAProxy-demo` node:

    ```{.bash data-prompt="$"}
    $ sudo yum install percona-haproxy
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

3. Enable a SELinux boolean to allow HAProxy to bind to non standard ports:

    ```{.bash data-prompt="$"}
    $ sudo setsebool -P haproxy_connect_any on
    ```

4. Restart HAProxy:
    
    ```{.bash data-prompt="$"}
    $ sudo systemctl restart haproxy
    ```

5. Check the HAProxy logs to see if there are any errors:
   
    ```{.bash data-prompt="$"}
    $ sudo journalctl -u haproxy.service -n 100 -f
    ```