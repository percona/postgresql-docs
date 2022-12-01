# Deploying PostgreSQL for high availability with Patroni on Debian or Ubuntu

This guide provides instructions on how to set up a highly available PostgreSQL cluster with Patroni on Debian or Ubuntu. 


## Preconditions

For this setup, we will use the nodes running on Ubuntu 20.04 as the base operating system and having the following IP addresses:

| Node name     | Public IP address | Internal IP address
|---------------|-------------------|--------------------
| node1         | 157.230.42.174    | 10.104.0.7
| node2         | 68.183.177.183    | 10.104.0.2
| node3         | 165.22.62.167     | 10.104.0.8
| HAProxy-demo  | 134.209.111.138   | 10.104.0.6


!!! note

    In a production (or even non-production) setup, the PostgreSQL nodes will be within a private subnet without any public connectivity to the Internet, and the HAProxy will be in a different subnet that allows client traffic coming only from a selected IP range. To keep things simple, we have implemented this architecture in a DigitalOcean VPS environment, and each node can access the other by its internal, private IP. 

### Setting up hostnames in the `/etc/hosts` file

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

### Install Percona Distribution for PostgreSQL

1. Follow the [installation instructions](../installing.md#on-debian-and-ubuntu-using-apt) to install Percona Distribution for PostgreSQL on `node1`, `node2` and `node3`.

2. Remove the data directory. Patroni requires a clean environment to initialize a new cluster. Use the following commands to stop the PostgreSQL service and then remove the data directory:

   ```{.bash data-prompt="$"}
   $ sudo systemctl stop postgresql
   $ sudo rm -rf /var/lib/postgresql/11/main
   ```

## Configure ETCD distributed store  

The distributed configuration store helps establish a consensus among nodes during a failover and will manage the configuration for the three PostgreSQL instances. Although Patroni can work with other distributed consensus stores (i.e., Zookeeper, Consul, etc.), the most commonly used one is `etcd`. 

The `etcd` cluster is first started in one node and then the subsequent nodes are added to the first node using the `add `command. The configuration is stored in the `/etc/default/etcd` file.

1. Install `etcd` on every PostgreSQL node using the following command:

    ```{.bash data-prompt="$"}
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

    ```{.bash data-prompt="$"}
    $ sudo etcdctl member add node2 http://10.104.0.2:2380
    $ sudo etcdctl member add node3 http://10.104.0.8:2380
    ```

4. Restart the `etcd` service on `node2` and `node3`:

    ```{.bash data-prompt="$"}
    $ sudo systemctl restart etcd
    ```

5. Check the etcd cluster members.
    
    ```{.bash data-prompt="$"}
    $ sudo etcdctl member list
    ```

    The output resembles the following:

    ```
    21d50d7f768f153a: name=node1 peerURLs=http://10.104.0.7:2380 clientURLs=http://10.104.0.7:2379 isLeader=true
    af4661d829a39112: name=node2 peerURLs=http://10.104.0.2:2380 clientURLs=http://10.104.0.2:2379 isLeader=false
    e3f3c0c1d12e9097: name=node3 peerURLs=http://10.104.0.8:2380 clientURLs=http://10.104.0.8:2379 isLeader=false
    ```

## Set up the watchdog service

The Linux kernel uses the utility called a _watchdog_ to protect against an unresponsive system. The watchdog monitors a system for unrecoverable application errors, depleted system resources, etc., and initiates a reboot to safely return the system to a working state. The watchdog functionality is  useful for servers that are intended to run without human intervention for a long time. Instead of users finding a hung server, the watchdog functionality can help maintain the service.

In this example, we will configure _Softdog_ - a standard software implementation for watchdog that is shipped with Ubuntu 20.04. 

Complete the following steps on all three PostgreSQL nodes to load and configure Softdog.  

1. Load Softdog:

    ```{.bash data-prompt="$"}
    $ sudo sh -c 'echo "softdog" >> /etc/modules'
    ```

2. Patroni will be interacting with the watchdog service. Since Patroni is run by the `postgres` user, this user must have access to Softdog. To make this happen, change the ownership  of the `watchdog.rules` file to the `postgres` user: 

    ```{.bash data-prompt="$"}
    $ sudo sh -c 'echo "KERNEL==\"watchdog\", OWNER=\"postgres\", GROUP=\"postgres\"" >> /etc/udev/rules.d/61-watchdog.rules'
    ```

3. Remove Softdog from the blacklist. 

    * Find out the files where Softdog is blacklisted:

       ```{.bash data-prompt="$"}
       $ grep blacklist /lib/modprobe.d/* /etc/modprobe.d/* |grep softdog
       ```
     
      In our case, `modprobe `is blacklisting the Softdog:

      ```
      /lib/modprobe.d/blacklist_linux_5.4.0-73-generic.conf:blacklist softdog
      ```
    
    * Remove the `blacklist softdog` line from the `/lib/modprobe.d/blacklist_linux_5.4.0-73-generic.conf` file. 
    * Restart the service 

      ```{.bash data-prompt="$"}
      $ sudo modprobe softdog
      ```
    
    * Verify the `modprobe` is working correctly by running the `lsmod `command:
      
      ```{.bash data-prompt="$"}
      $ sudo lsmod | grep softdog
      ```
      
      The output will show a process identifier if it’s running.

      ```
      softdog                16384  0
      ```

4. Check that the Softdog files under the `/dev/ `folder are owned by the `postgres `user: 


```{.bash data-prompt="$"}
$ ls -l /dev/watchdog*

crw-rw---- 1 postgres postgres  10, 130 Sep 11 12:53 /dev/watchdog
crw------- 1 root     root     245,   0 Sep 11 12:53 /dev/watchdog0
```


!!! tip 

    If the ownership has not been changed for any reason, run the following command to manually change it:
    
    ```{.bash data-prompt="$"}
    $ sudo chown postgres:postgres /dev/watchdog*
    ```

## Configure Patroni

1. Install Patroni on every PostgreSQL node:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-patroni
    ```

2. Create the `patroni.yml` configuration file under the `/etc/patroni` directory.  The file holds the default configuration values for a PostgreSQL cluster and will reflect the current cluster setup.

3. Add the following configuration for `node1`:

    ```yaml
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
      data_dir: "/var/lib/postgresql/11/main"
      bin_dir: "/usr/lib/postgresql/11/bin"
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

    !!! admonition "Patroni configuration file"

        Let’s take a moment to understand the contents of the `patroni.yml` file. 

        The first section provides the details of the first node (`node1`) and its connection ports. After that, we have the `etcd` service and its port details.

        Following these, there is a `bootstrap` section that contains the PostgreSQL configurations and the steps to run once the database is initialized. The `pg_hba.conf` entries specify all the other nodes that can connect to this node and their authentication mechanism. 


4. Create the configuration files for `node2` and `node3`. Replace the reference to `node1` with `node2` and `node3`, respectively.
5. Enable and restart the patroni service on every node. Use the following commands:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable patroni
    $ sudo systemctl restart patroni
    ```
   
When Patroni starts, it initializes PostgreSQL (because the service is not currently running and the data directory is empty) following the directives in the bootstrap section of the configuration file. 

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
    Sep 23 12:50:23 node01 patroni[10140]:     /usr/lib/postgresql/11/bin/pg_ctl -D /var/lib/postgresql/11/main -l logfile start
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
```

The command output is the following

```
psql (11.13)
Type "help" for help.

postgres=#
```

## Configure HAProxy

HAProxy node will accept client connection requests and route those to the active node of the PostgreSQL cluster. This way, a client application doesn’t have to know what node in the underlying cluster is the current primary. All it needs to do is to access a single HAProxy URL and send its read/write requests there. Behind-the-scene, HAProxy routes the connection to a healthy node (as long as there is at least one healthy node available) and ensures that client application requests are never rejected. 

HAProxy is capable of routing write requests to the primary node and read requests - to the secondaries in a round-robin fashion so that no secondary instance is unnecessarily loaded. To make this happen, provide different ports in the HAProxy configuration file. In this deployment, writes are routed to port 5000 and reads  - to port 5001.

1. Install HAProxy on the `HAProxy-demo` node:

    ```{.bash data-prompt="$"}
    $ sudo apt install haproxy
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

## Testing

See the [Testing PostgreSQL cluster](ha-test.md) for the guidelines on how to test your PostgreSQL cluster for replication, failure, switchover.