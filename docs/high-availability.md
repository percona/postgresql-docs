# High Availability in PostgreSQL with Patroni

!!! summary

    - Solution overview
    - Cluster deployment
    - Testing the cluster

PostgreSQL has been widely adopted as a modern, high-performance transactional database. A highly available PostgreSQL cluster can withstand failures caused by network outages, resource saturation, hardware failures, operating system crashes, or unexpected reboots.  Such cluster is often a critical component of the enterprise application landscape, where [four nines of availability](https://en.wikipedia.org/wiki/High_availability#Percentage_calculation) is a minimum requirement. 

This document provides instructions on how to set up and test a highly-available, single-primary, three-node cluster with Percona PostgreSQL and [Patroni](#patroni). 

??? admonition "High availability overview"

    There are a few methods for achieving high availability with PostgreSQL:

    - shared disk failover, 
    - file system replication, 
    - trigger-based replication, 
    - statement-based replication, 
    - logical replication, and 
    - Write-Ahead Log (WAL) shipping.

    In recent times, PostgreSQL high availability is most commonly achieved with [streaming replication](#streaming-replication).


    ## Streaming replication

    Streaming replication is part of Write-Ahead Log shipping, where changes to the WALs are immediately made available to standby replicas. With this approach, a standby instance is always up-to-date with changes from the primary node and can assume the role of primary in case of a failover.


    ### Why native streaming replication is not enough

    Although the native streaming replication in PostgreSQL supports failing over  to the primary node, it lacks some key features expected from a truly highly-available solution. These include:


    * No consensus-based promotion of a “leader” node during a failover
    * No decent capability for monitoring cluster status 
    * No automated way to bring back the failed primary node to the cluster
    * A manual or scheduled switchover is not easy to manage 

    To address these shortcomings, there are a multitude of third-party, open-source extensions for PostgreSQL. The challenge for a database administrator here is to select the right utility for the current scenario. 

    Percona Distribution for PostgreSQL solves this challenge by providing the [Patroni](https://patroni.readthedocs.io/en/latest/) extension for achieving PostgreSQL high availability.

## Patroni

[Patroni](https://patroni.readthedocs.io/en/latest/) provides a template-based approach to create highly available PostgreSQL clusters. Running atop the PostgreSQL streaming replication process, it integrates with watchdog functionality to detect failed primary nodes and take corrective actions to prevent outages. Patroni also provides a pluggable configuration store to manage distributed, multi-node cluster configuration and comes with REST APIs to monitor and manage the cluster. There is also a command-line utility called _patronictl_ that helps manage switchovers and failure scenarios.

## Architecture layout

The following diagram shows the architecture of a three-node PostgreSQL cluster with a single-leader node. 

![Architecture of the three-node, single primary PostgreSQL cluster](_images/diagrams/patroni-architecture.png)

### Components

The following are the components:

- Three ProxySQL nodes: `node1`, `node2` and `node3`
- A dedicated HAProxy node `HAProxy-demo`. HAProxy is an open-source load balancing software through which client connections to the cluster are routed.
- ETCD - a distributed configuration storage
- Softdog - a watchdog utility which is used to detect unhealthy nodes in an acceptable time frame.

Both ETCD and Softdog instances are running on PostgreSQL nodes.

## Deployment

### Preconditions

We will use the nodes running on Ubuntu 20.04 as the base operating system and having the following IP addresses:

| Node name     | Public IP address | Internal IP address
|---------------|-------------------|--------------------
| node1         | 157.230.42.174    | 10.104.0.7
| node2         | 68.183.177.183    | 10.104.0.2
| node3         | 165.22.62.167     | 10.104.0.8
| HAProxy-demo  | 134.209.111.138   | 10.104.0.6


!!! note

    In a production (or even non-production) setup, the PostgreSQL nodes will be within a private subnet without any public connectivity to the Internet, and the HAProxy will be in a different subnet that allows client traffic coming only from a selected IP range. To keep things simple, we have implemented this architecture in a DigitalOcean VPS environment, and each node can access the other by its internal, private IP. 

#### Setting up hostnames in the `/etc/hosts` file

To make the nodes aware of each other and allow their seamless communication, resolve their hostnames to their public IP addresses. Modify the `/etc/hosts` file of each node as follows:

| node 1                    | node 2                    | node 3
|---------------------------| --------------------------|-----------------------
| <code> 127.0.0.1 localhost node1 <br> 10.104.0.7 node1 <br> **10.104.0.2 node2** <br> **10.104.0.8 node3** </code>   | <code>127.0.0.1 localhost node2  <br> **10.104.0.7 node1** <br> 10.104.0.2 node2  <br> **10.104.0.8 node3** </code>  | <code> 127.0.0.1 localhost node3 <br> **10.104.0.7 node1** <br> **10.104.0.2 node2** <br> 10.104.0.8 node3 </code>


The `/etc/hosts` file of the HAProxy-demo node looks like the following:

```
127.0.1.1 HAProxy-demo HAProxy-demo
127.0.0.1 localhost
10.104.0.6 HAProxy-demo
10.104.0.7 node1
10.104.0.2 node2
10.104.0.8 node3
```

#### Install Percona Distribution for PostgreSQL

1. Follow the [installation instructions](installing.md) to install Percona Distribution for PostgreSQL on `node1`, `node2` and `node3`.

2. Remove the data directory. Patroni requires a clean environment to initialize a new cluster. Use the following commands to stop the PostgreSQL service and then remove the data directory:

   ```sh
   $ sudo systemctl stop postgresql
   $ sudo rm -rf /var/lib/postgresql/13/main
   ```

### Configure ETCD distributed store  

The distributed configuration store helps establish a consensus among nodes during a failover and will manage the configuration for the three PostgreSQL instances. Although Patroni can work with other distributed consensus stores (i.e., Zookeeper, Consul, etc.), the most commonly used one is `etcd`. 

The `etcd` cluster is first started in one node and then the subsequent nodes are added to the first node using the `add `command. The configuration is stored in the `/etc/default/etcd` file.

1. Install `etcd` on every PostgreSQL node using the package manager of your operating system. In our example, we will use `apt`:

    ```sh
    $ sudo apt install etcd
    ```

2. Modify the `/etc/default/etcd` configuration file on each node.

    * On `node1`, add the IP address of `node1` to the `ETCD_INITIAL_CLUSTER` parameter. The configuration file looks as follows:

      ```text
      ETCD_NAME=node1
      ETCD_INITIAL_CLUSTER="node1=http://10.104.0.7:2380"
      ETCD_INITIAL_CLUSTER_TOKEN="devops_token"
      ETCD_INITIAL_CLUSTER_STATE="new"
      ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.104.0.7:2380"
      ETCD_DATA_DIR="/var/lib/etcd/postgresql"
      ETCD_LISTEN_PEER_URLS="http://10.104.0.7:2380"
      ETCD_LISTEN_CLIENT_URLS="http://10.104.0.7:2379,http://localhost:2379"
      ETCD_ADVERTISE_CLIENT_URLS="http://10.104.0.7:2379"
      …
      ```

    * On `node2`, add the IP addresses of both `node1` and `node2` to the `ETCD_INITIAL_CLUSTER` parameter:

      ```text
      ETCD_NAME=node2
      ETCD_INITIAL_CLUSTER="node1=http://10.104.0.7:2380,node2=http://10.104.0.2:2380"
      ETCD_INITIAL_CLUSTER_TOKEN="devops_token"
      ETCD_INITIAL_CLUSTER_STATE="existing"
      ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.104.0.2:2380"
      ETCD_DATA_DIR="/var/lib/etcd/postgresql"
      ETCD_LISTEN_PEER_URLS="http://10.104.0.2:2380"
      ETCD_LISTEN_CLIENT_URLS="http://10.104.0.2:2379,http://localhost:2379"
      ETCD_ADVERTISE_CLIENT_URLS="http://10.104.0.2:2379"
      …
      ```

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

3. On `node1`, add `node2` and `node3` to the cluster using the `add` command:

    ```sh
    $ sudo etcdctl member add node2 http://10.104.0.2:2380
    $ sudo etcdctl member add node3 http://10.104.0.8:2380
    ```

4. Restart the `etcd` service on `node2` and `node3`:

    ```sh
    $ sudo systemctl restart etcd
    ```

    The result will look like this:
    
    ```
    21d50d7f768f153a: name=node1 peerURLs=http://10.104.0.7:2380 clientURLs=http://10.104.0.7:2379 isLeader=true
    af4661d829a39112: name=node2 peerURLs=http://10.104.0.2:2380 clientURLs=http://10.104.0.2:2379 isLeader=false
    e3f3c0c1d12e9097: name=node3 peerURLs=http://10.104.0.8:2380 clientURLs=http://10.104.0.8:2379 isLeader=false
    ```

### Set up the watchdog service

The Linux kernel uses the utility called a _watchdog_ to protect against an unresponsive system. The watchdog monitors a system for unrecoverable application errors, depleted system resources, etc., and initiates a reboot to safely return the system to a working state. The watchdog functionality is  useful for servers that are intended to run without human intervention for a long time. Instead of users finding a hung server, the watchdog functionality can help maintain the service.

In this example, we will configure _Softdog_ - a standard software implementation for watchdog that is shipped with Ubuntu 20.04. 

Complete the following steps on all three PostgreSQL nodes to load and configure Softdog.  

1. Load Softdog:

    ```sh
    $ sudo sh -c 'echo "softdog" >> /etc/modules'
    ```

2. Patroni will be interacting with the watchdog service. Since Patroni is run by the `postgres` user, this user must have access to Softdog. To make this happen, change the ownership  of the `watchdog.rules` file to the `postgres` user: 

    ``` sh
    $ sudo sh -c 'echo "KERNEL==\"watchdog\", OWNER=\"postgres\", GROUP=\"postgres\"" >> /etc/udev/rules.d/61-watchdog.rules'
    ```

3. Remove Softdog from the blacklist. 

    * Find out the files where Softdog is blacklisted:

       ```sh
       $ grep blacklist /lib/modprobe.d/* /etc/modprobe.d/* |grep softdog
       ```
     
      In our case, `modprobe `is blacklisting the Softdog:

      ```
      /lib/modprobe.d/blacklist_linux_5.4.0-73-generic.conf:blacklist softdog
      ```
    
    * Remove the `blacklist softdog` line from the `/lib/modprobe.d/blacklist_linux_5.4.0-73-generic.conf` file. 
    * Restart the service 

      ```sh
      $ sudo modprobe softdog
      ```
    
    * Verify the `modprobe` is working correctly by running the `lsmod `command:
      
      ```sh
      $ sudo lsmod | grep softdog
      ```
      
      The output will show a process identifier if it’s running.

      ```
      softdog                16384  0
      ```

4. Check that the Softdog files under the `/dev/ `folder are owned by the `postgres `user: 


```
$ ls -l /dev/watchdog*

crw-rw---- 1 postgres postgres  10, 130 Sep 11 12:53 /dev/watchdog
crw------- 1 root     root     245,   0 Sep 11 12:53 /dev/watchdog0
```


!!! tip 

    If the ownership has not been changed for any reason, run the following command to manually change it:
    
    ```sh
    $ sudo chown postgres:postgres /dev/watchdog*
    ```

### Configure Patroni

1. Install Patroni on every PostgreSQL node:

    ```sh
    $ sudo apt-get install percona-patroni
    ```

2. Create the `patroni.yml` configuration file under the `/etc/patroni` directory.  The file holds the default configuration values for a PostgreSQL cluster and will reflect the current cluster setup.

3. Add the following configuration for `node1`:

    ```yml
    scope: stampede1
    name: node1

    restapi:
      listen: 0.0.0.0:8008
      connect_address: node1:8008

    etcd:
      host: node1:2379

    bootstrap:
      # this section will be written into Etcd:/<namespace>/<scope>/config after initializing new cluster
      dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
    #    primary_start_timeout: 300
    #    synchronous_mode: false
        postgresql:
          use_pg_rewind: true
          use_slots: true
          parameters:
            wal_level: replica
            hot_standby: "on"
            logging_collector: 'on'
            max_wal_senders: 5
            max_replication_slots: 5
            wal_log_hints: "on"
            #archive_mode: "on"
            #archive_timeout: 600
            #archive_command: "cp -f %p /home/postgres/archived/%f"
            #recovery_conf:
            #restore_command: cp /home/postgres/archived/%f %p

      # some desired options for 'initdb'
      initdb:  # Note: It needs to be a list (some options need values, others are switches)
      - encoding: UTF8
      - data-checksums

      pg_hba:  # Add following lines to pg_hba.conf after running 'initdb'
      - host all all 10.104.0.7/32 md5
      - host replication replicator 127.0.0.1/32 trust
      - host all all 10.104.0.2/32 md5  
      - host all all 10.104.0.8/32 md5 
      - host all all 10.104.0.6/32 trust
    #  - hostssl all all 0.0.0.0/0 md5

      # Additional script to be launched after initial cluster creation (will be passed the connection URL as parameter)
    # post_init: /usr/local/bin/setup_cluster.sh
      # Some additional users users which needs to be created after initializing new cluster
      users:
        admin:
          password: admin
          options:
            - createrole
            - createdb
        replicator: 
          password: password    
          options:
            - replication 
    postgresql:
      listen: 0.0.0.0:5432
      connect_address: node1:5432
      data_dir: "/var/lib/postgresql/13/main"
      bin_dir: "/usr/lib/postgresql/13/bin"
    #  config_dir:
      pgpass: /tmp/pgpass0
      authentication:
        replication:
          username: replicator
          password: password
        superuser:
          username: postgres
          password: password
      parameters:
        unix_socket_directories: '/var/run/postgresql'

    watchdog:
      mode: required # Allowed values: off, automatic, required
      device: /dev/watchdog
      safety_margin: 5

    tags:
        nofailover: false
        noloadbalance: false
        clonefrom: false
        nosync: false
    ```

4. Create the configuration files for `node2` and `node3`. Replace the reference to `node1` with `node2` and `node3`, respectively.
5. Enable and restart the patroni service on every node. Use the following commands:

   ```sh
   $ sudo systemctl enable patroni
   $ sudo systemctl restart patroni
   ```
   
When Patroni starts, it initializes PostgreSQL (because the service is not currently running and the data directory is empty) following the directives in the bootstrap section of the configuration file. If Patroni has started properly, you should be able to locally connect to a PostgreSQL node using the following command:

```sh
$ sudo psql -U postgres

psql (13.3 (Ubuntu 2:13-3.2.focal))
Type "help" for help.

postgres=#
```

### Configure HAProxy

HAProxy node will accept client connection requests and route those to the active node of the PostgreSQL cluster. This way, a client application doesn’t have to know what node in the underlying cluster is the current primary. All it needs to do is to access a single HAProxy URL and send its read/write requests there. Behind-the-scene, HAProxy routes the connection to a healthy node (as long as there is at least one healthy node available) and ensures that client application requests are never rejected. 

HAProxy is capable of routing write requests to the primary node and read requests - to the secondaries in a round-robin fashion so that no secondary instance is unnecessarily loaded. To make this happen, provide different ports in the HAProxy configuration file. In this deployment, writes are routed to port 5000 and reads  - to port 5001.

1. Install HAProxy on the `HAProxy-demo` node:

    ``` sh
    $ sudo apt-get install haproxy
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
    
    ```sh
    $ sudo systemctl restart haproxy
    ```


4. Check the HAProxy logs to see if there are any errors:
   
    ```sh
    $ sudo journalctl -u haproxy.service -n 100 -f
    ```

## Testing the Patroni PostgreSQL Cluster

This section covers the following scenarios to test the PostgreSQL cluster:

* replication, 
* connectivity, 
* failover, and 
* manual switchover.

### Testing replication 

1. Connect to the cluster and establish the `psql` session from a client machine that can connect to the HAProxy node. Use the HAProxy-demo node's public IP address:

    ```
    psql -U postgres -h 134.209.111.138 -p 5000
    ```

2. Run the following commands to create a table and insert a few rows:

    ```sql
    CREATE TABLE customer(name text,age integer);
    INSERT INTO CUSTOMER VALUES('john',30);
    INSERT INTO CUSTOMER VALUES('dawson',35);
    ```

3. To ensure that the replication is working, we can log in to each PostgreSQL node and run a simple SQL statement against the locally running instance:

    ```sh
    $ sudo psql -U postgres -c "SELECT * FROM CUSTOMER;"
    ```
    
    The results on each node should be the following:

    ```
      name  | age
    --------+-----
     john   |  30
     dawson |  35
    (2 rows)
    ```

### Testing failover

In a proper setup, client applications won't have issues connecting to the cluster, even if one or even two of the nodes go down. We will test the cluster for failover in the following scenarios:

#### Scenario 1. Intentionally stop the PostgreSQL on the primary node and verify access to PostgreSQL.

1. Run the following command on any node to check the current cluster status:

    ``` sh
    $ sudo patronictl -c /etc/patroni/patroni.yml list

    + Cluster: stampede1 (7011110722654005156) -----------+
    | Member | Host  | Role    | State   | TL | Lag in MB |
    +--------+-------+---------+---------+----+-----------+
    | node1  | node1 | Leader  | running |  1 |           |
    | node2  | node2 | Replica | running |  1 |         0 |
    | node3  | node3 | Replica | running |  1 |         0 |
    +--------+-------+---------+---------+----+-----------+
    ```

2. `node1` is the current leader. Stop Patroni in `node1` to see how it changes the cluster:
    
    ```sh
    $ sudo systemctl stop patroni
    ```

3. Once the service stops in `node1`, check the logs in `node2` and `node3` using the following command: 

    ```sh
    $ sudo journalctl -u patroni.service -n 100 -f
    ```

    ??? admonition "Output"
        
        ```
        Sep 23 14:18:13 node03 patroni[10042]: 2021-09-23 14:18:13,905 INFO: no action. I am a secondary (node3) and following a leader (node1)
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,011 INFO: Got response from node2 http://node2:8008/patroni: {"state": "running", "postprimary_start_time": "2021-09-23 12:50:29.460027+00:00", "role": "replica", "server_version": 130003, "cluster_unlocked": true, "xlog": {"received_location": 67219152, "replayed_location": 67219152, "replayed_timestamp": "2021-09-23 13:19:50.329387+00:00", "paused": false}, "timeline": 1, "database_system_identifier": "7011110722654005156", "patroni": {"version": "2.1.0", "scope": "stampede1"}}
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,031 WARNING: Request failed to node1: GET http://node1:8008/patroni (HTTPConnectionPool(host='node1', port=8008): Max retries exceeded with url: /patroni (Caused by ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))))
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,038 INFO: Software Watchdog activated with 25 second timeout, timing slack 15 seconds
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,043 INFO: promoted self to leader by acquiring session lock
        Sep 23 14:18:20 node03 patroni[13641]: server promoting
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,049 INFO: cleared rewind state after becoming the leader
        Sep 23 14:18:21 node03 patroni[10042]: 2021-09-23 14:18:21,101 INFO: no action. I am (node3) the leader with the lock
        Sep 23 14:18:21 node03 patroni[10042]: 2021-09-23 14:18:21,117 INFO: no action. I am (node3) the leader with the lock
        Sep 23 14:18:31 node03 patroni[10042]: 2021-09-23 14:18:31,114 INFO: no action. I am (node3) the leader with the lock
        ...
        ```
  
    The logs in `node3` show that the requests to `node1` are failing, the watchdog is coming into action, and `node3` is promoting itself as the leader:

  
4. Verify that you can still access the cluster through the HAProxy instance and read data:

    ```
    psql -U postgres -h 10.104.0.6 -p 5000 -c "SELECT * FROM CUSTOMER;"

      name  | age
    --------+-----
     john   |  30
     dawson |  35
    (2 rows)
    ```


5. Restart the Patroni service in `node1`
    
    ```sh
    $ sudo systemctl start patroni
    ```

6. Check the current cluster status:  

    
    ```sh
    $ sudo patronictl -c /etc/patroni/patroni.yml list

    + Cluster: stampede1 (7011110722654005156) -----------+
    | Member | Host  | Role    | State   | TL | Lag in MB |
    +--------+-------+---------+---------+----+-----------+
    | node1  | node1 | Replica | running |  2 |         0 |
    | node2  | node2 | Replica | running |  2 |         0 |
    | node3  | node3 | Leader  | running |  2 |           |
    +--------+-------+---------+---------+----+-----------+

    ```

As we see, `node3` remains the leader and the rest are replicas.

#### Scenario 2. Abrupt machine shutdown or power outage 

To emulate the power outage, let's kill the service in `node3` and see what happens in `node1` and `node2`. 

1. Identify the process ID of Patroni and then kill it with a `-9` switch. 

    ```sh
    $ ps aux | grep -i patroni

    postgres   10042  0.1  2.1 647132 43948 ?        Ssl  12:50   0:09 /usr/bin/python3 /usr/bin/patroni /etc/patroni/patroni.yml

    $ sudo kill -9 10042
    ```

2. Check the logs on `node2`: 

    ```sh
    $ sudo journalctl -u patroni.service -n 100 -f
    ```

    ??? admonition "Output"

        ```
        Sep 23 14:40:41 node02 patroni[10577]: 2021-09-23 14:40:41,656 INFO: no action. I am a secondary (node2) and following a leader (node3)
        …
        Sep 23 14:41:01 node02 patroni[10577]: 2021-09-23 14:41:01,373 INFO: Got response from node1 http://node1:8008/patroni: {"state": "running", "postprimary_start_time": "2021-09-23 14:25:30.076762+00:00", "role": "replica", "server_version": 130003, "cluster_unlocked": true, "xlog": {"received_location": 67221352, "replayed_location": 67221352, "replayed_timestamp": null, "paused": false}, "timeline": 2, "database_system_identifier": "7011110722654005156", "patroni": {"version": "2.1.0", "scope": "stampede1"}}
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,364 WARNING: Request failed to node3: GET http://node3:8008/patroni (HTTPConnectionPool(host='node3', port=8008): Max retries exceeded with url: /patroni (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x7f57e06dffa0>, 'Connection to node3 timed out. (connect timeout=2)')))
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,373 INFO: Software Watchdog activated with 25 second timeout, timing slack 15 seconds
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,385 INFO: promoted self to leader by acquiring session lock
        Sep 23 14:41:03 node02 patroni[15478]: server promoting
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,397 INFO: cleared rewind state after becoming the leader
        Sep 23 14:41:04 node02 patroni[10577]: 2021-09-23 14:41:04,450 INFO: no action. I am (node2) the leader with the lock
        Sep 23 14:41:04 node02 patroni[10577]: 2021-09-23 14:41:04,475 INFO: no action. I am (node2) the leader with the lock
        …
        … 
        ```
    
    `node2` realizes that the leader is dead, and promotes itself as the leader.

3. Try accessing the cluster using the HAProxy endpoint at any point in time between these operations. The cluster is still accepting connections.


### Manual switchover

Typically, a manual switchover is needed for planned downtime to perform maintenance activity on the leader node. Patroni provides the `switchover` command to manually switch over from the leader node. 

Run the following command on `node2` (the current leader node):

```sh
$ sudo patronictl -c /etc/patroni/patroni.yml switchover
```

Patroni asks the name of the current primary node and then the node that should take over as the switched-over primary. You can also specify the time at which the switchover should happen. To trigger the process immediately, specify the value _now_:


```
primary [node2]: node2
Candidate ['node1', 'node3'] []: node1
When should the switchover take place (e.g. 2021-09-23T15:56 )  [now]: now
Current cluster topology
+ Cluster: stampede1 (7011110722654005156) -----------+
| Member | Host  | Role    | State   | TL | Lag in MB |
+--------+-------+---------+---------+----+-----------+
| node1  | node1 | Replica | running |  3 |         0 |
| node2  | node2 | Leader  | running |  3 |           |
| node3  | node3 | Replica | stopped |    |   unknown |
+--------+-------+---------+---------+----+-----------+
Are you sure you want to switchover cluster stampede1, demoting current primary node2? [y/N]: y
2021-09-23 14:56:40.54009 Successfully switched over to "node1"
+ Cluster: stampede1 (7011110722654005156) -----------+
| Member | Host  | Role    | State   | TL | Lag in MB |
+--------+-------+---------+---------+----+-----------+
| node1  | node1 | Leader  | running |  3 |           |
| node2  | node2 | Replica | stopped |    |   unknown |
| node3  | node3 | Replica | stopped |    |   unknown |
+--------+-------+---------+---------+----+-----------+
```


Restart the Patroni service in `node2` (after the "planned maintenance"). The node rejoins the cluster as a secondary.