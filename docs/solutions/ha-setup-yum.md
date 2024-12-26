# Deploying PostgreSQL for high availability with Patroni on RHEL or CentOS

This guide provides instructions on how to set up a highly available PostgreSQL cluster with Patroni on Red Hat Enterprise Linux or CentOS. 


## Considerations

1. This is an example deployment where etcd runs on the same host machines as the Patroni and PostgreSQL and there is a single dedicated HAProxy host. Alternatively etcd can run on different set of nodes. 

    If etcd is deployed on the same host machine as Patroni and PostgreSQL, separate disk system for etcd and PostgreSQL is recommended due to performance reasons.
    
2. For this setup, we use the nodes running on Red Hat Enterprise Linux 8 as the base operating system:

    | Node name     | Application       | IP address
    |---------------|-------------------|--------------------
    | node1         | Patroni, PostgreSQL, etcd    | 10.104.0.1
    | node2         | Patroni, PostgreSQL, etcd    | 10.104.0.2
    | node3         | Patroni, PostgreSQL, etcd     | 10.104.0.3
    | HAProxy-demo  | HAProxy           | 10.104.0.6


!!! note

    We recommend not to expose the hosts/nodes where Patroni / etcd / PostgreSQL are running to public networks due to security risks.  Use Firewalls, Virtual networks, subnets or the like to protect the database hosts from any kind of attack.   

## Initial setup 

### Set up hostnames in the `/etc/hosts` file

It's not necessary to have name resolution, but it makes the whole setup more readable and less error prone. Here, instead of configuring a DNS, we use a local name resolution by updating the file `/etc/hosts`. By resolving their hostnames to their IP addresses, we make the nodes aware of each other's names and allow their seamless communication. 

=== "node1"   

    1. Set up the hostname for the node

        ```{.bash data-prompt="$"}
        $ sudo hostnamectl set-hostname node1
        ```

    2. Modify the `/etc/hosts` file to include the hostnames and IP addresses of the remaining nodes. Add the following at the end of the `/etc/hosts` file on all nodes:   

        ```text hl_lines="3 4"
        # Cluster IP and names 
        10.104.0.1 node1 
        10.104.0.2 node2 
        10.104.0.3 node3
        ```    

=== "node2"    

    1. Set up the hostname for the node

        ```{.bash data-prompt="$"}
        $ sudo hostnamectl set-hostname node2
        ```

    2. Modify the `/etc/hosts` file to include the hostnames and IP addresses of the remaining nodes. Add the following at the end of the `/etc/hosts` file on all nodes:   

        ```text hl_lines="2 4"
        # Cluster IP and names 
        10.104.0.1 node1 
        10.104.0.2 node2 
        10.104.0.3 node3
        ```    

=== "node3"    

    1. Set up the hostname for the node

        ```{.bash data-prompt="$"}
        $ sudo hostnamectl set-hostname node3
        ```

    2. Modify the `/etc/hosts` file to include the hostnames and IP addresses of the remaining nodes. Add the following at the end of the `/etc/hosts` file on all nodes:   

        ```text hl_lines="2 3"
        # Cluster IP and names 
        10.104.0.1 node1 
        10.104.0.2 node2 
        10.104.0.3 node3
        ```    

=== "HAproxy-demo"  

    1. Set up the hostname for the node

        ```{.bash data-prompt="$"}
        $ sudo hostnamectl set-hostname HAProxy-demo
        ```

    2. Modify the `/etc/hosts` file. The HAProxy instance should have the name resolution for all the three nodes in its `/etc/hosts` file. Add the following lines at the end of the file:    

        ```text hl_lines="3 4 5"
        # Cluster IP and names
        10.104.0.6 HAProxy-demo
        10.104.0.1 node1
        10.104.0.2 node2
        10.104.0.3 node3
        ```

### Install the software

Run the following commands on `node1`, `node2` and `node3`:

1. Install Percona Distribution for PostgreSQL:

    * Check the [platform specific notes](../yum.md#for-percona-distribution-for-postgresql-packages) 
    * Install the `percona-release` repository management tool

        --8<-- "percona-release-yum.md"

    * Enable the repository:    

        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ppg{{pgversion}}
        ```    

    * Install Percona Distribution for PostgreSQL package

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-postgresql{{pgversion}}-server
        ```

    !!! important    

        **Don't** initialize the cluster and start the `postgresql` service. The cluster initialization and setup are handled by Patroni during the bootsrapping stage.

2. Install some Python and auxiliary packages to help with Patroni and etcd
    
    ```{.bash data-prompt="$"}
    $ sudo yum install python3-pip python3-devel binutils
    ```

3. Install etcd, Patroni, pgBackRest packages. Check [platform specific notes for Patroni](../yum.md#for-percona-patroni-package):

    ```{.bash data-prompt="$"}
    $ sudo yum install percona-patroni \
    etcd python3-python-etcd\
    percona-pgbackrest
    ```

4. Stop and disable all installed services:
    
    ```{.bash data-prompt="$"}
    $ sudo systemctl stop {etcd,patroni,postgresql}
    $ systemctl disable {etcd,patroni,postgresql}
    ```

## Configure etcd distributed store  

In our implementation we use etcd distributed configuration store. [Refresh your knowledge about etcd](high-availability.md#etcd).

!!! note
    
    If you [installed the software from tarballs](../tarball.md), you must first [enable etcd](../enable-extensions.md#etcd) before configuring it.

To get started with `etcd` cluster, you need to bootstrap it. This means setting up the initial configuration and starting the etcd nodes so they can form a cluster. There are the following bootstrapping mechanisms:  

* Static in the case when the IP addresses of the cluster nodes are known
* Discovery service - for cases when the IP addresses of the cluster are not known ahead of time.
    
Since we know the IP addresses of the nodes, we will use the static method. For using the discovery service, please refer to the [etcd documentation :octicons-external-link-16:](https://etcd.io/docs/v3.5/op-guide/clustering/#etcd-discovery){:target="_blank"}.

We will configure and start all etcd nodes in parallel. This can be done either by modifying each node's configuration or using the command line options. Use the method that you prefer more.

### Method 1. Modify the configuration file

1. Create the etcd configuration file on every node. You can edit the sample configuration file `/etc/etcd/etcd.conf.yaml` or create your own one. Replace the node names and IP addresses with the actual names and IP addresses of your nodes.

    === "node1"

         ```yaml title="/etc/etcd/etcd.conf.yaml"
         name: 'node1'
         initial-cluster-token: PostgreSQL_HA_Cluster_1
         initial-cluster-state: new
         initial-cluster: node1=http://10.104.0.1:2380,node2=http://10.104.0.2:2380,node3=http://10.104.0.3:2380
         data-dir: /var/lib/etcd
         initial-advertise-peer-urls: http://10.104.0.1:2380 
         listen-peer-urls: http://10.104.0.1:2380
         advertise-client-urls: http://10.104.0.1:2379
         listen-client-urls: http://10.104.0.1:2379
         ```

    === "node2"

         ```yaml title="/etc/etcd/etcd.conf.yaml"
         name: 'node2'
         initial-cluster-token: PostgreSQL_HA_Cluster_1
         initial-cluster-state: new
         initial-cluster: node1=http://10.104.0.1:2380,node2=http://10.104.0.2:2380,     node3=http://10.104.0.3:2380
         data-dir: /var/lib/etcd
         initial-advertise-peer-urls: http://10.104.0.2:2380 
         listen-peer-urls: http://10.104.0.2:2380
         advertise-client-urls: http://10.104.0.2:2379
         listen-client-urls: http://10.104.0.2:2379
         ```

    === "node3"

         ```yaml title="/etc/etcd/etcd.conf.yaml"
         name: 'node3'
         initial-cluster-token: PostgreSQL_HA_Cluster_1
         initial-cluster-state: new
         initial-cluster: node1=http://10.104.0.1:2380,node2=http://10.104.0.2:2380,     node3=http://10.104.0.3:2380
         data-dir: /var/lib/etcd
         initial-advertise-peer-urls: http://10.104.0.3:2380 
         listen-peer-urls: http://10.104.0.3:2380
         advertise-client-urls: http://10.104.0.3:2379
         listen-client-urls: http://10.104.0.3:2379
         ```

2. Enable and start the `etcd` service on all nodes:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable --now etcd
    $ sudo systemctl start etcd
    $ sudo systemctl status etcd
    ```

    During the node start, etcd searches for other cluster nodes defined in the configuration. If the other nodes are not yet running, the start may fail by a quorum timeout. This is expected behavior. Try starting all nodes again at the same time for the etcd cluster to be created.

--8<-- "check-etcd.md"

### Method 2. Start etcd nodes with command line options

1. On each etcd node, set the environment variables for the cluster members, the cluster token and state:

    ```
    TOKEN=PostgreSQL_HA_Cluster_1
    CLUSTER_STATE=new
    NAME_1=node1
    NAME_2=node2
    NAME_3=node3
    HOST_1=10.104.0.1
    HOST_2=10.104.0.2
    HOST_3=10.104.0.3
    CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_3}=http://${HOST_3}:2380
    ```

2. Start each etcd node in parallel using the following command:

    === "node1"

        ```{.bash data-prompt="$"}
        THIS_NAME=${NAME_1}
        THIS_IP=${HOST_1}
        etcd --data-dir=data.etcd --name ${THIS_NAME} \
        	--initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
        	--advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
        	--initial-cluster ${CLUSTER} \
        	--initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN}
        ```

    === "node2"

        ```{.bash data-prompt="$"}
        THIS_NAME=${NAME_2}
        THIS_IP=${HOST_2}
        etcd --data-dir=data.etcd --name ${THIS_NAME} \
        	--initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
        	--advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
        	--initial-cluster ${CLUSTER} \
        	--initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN}
        ```

    === "node3"

        ```{.bash data-prompt="$"}
        THIS_NAME=${NAME_3}
        THIS_IP=${HOST_3}
        etcd --data-dir=data.etcd --name ${THIS_NAME} \
        	--initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
        	--advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
        	--initial-cluster ${CLUSTER} \
        	--initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN}
        ```

--8<-- "check-etcd.md"

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
       DATA_DIR="/var/lib/pgsql/data/"
       PG_BIN_DIR="/usr/pgsql-{{pgversion}}/bin"
       ```

       **NOTE**: Check the path to the data and bin folders on your operating system and change it for the variables accordingly.
    
    * Patroni information:

       ```bash
       NAMESPACE="percona_lab"
       SCOPE="cluster_1
       ```

2. Create the directories required by Patroni

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

3. Use the following command to create the `/etc/patroni/patroni.yml` configuration file and add the following configuration for `node1`:

    ```bash
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

    tags:
        nofailover: false
        noloadbalance: false
        clonefrom: false
        nosync: false
    " | sudo tee -a /etc/patroni/patroni.yml
    ```

4. Check that the systemd unit file `percona-patroni.service` is created in `/etc/systemd/system`. If it is created, skip this step. 

    If it's **not created**, create it manually and specify the following contents within:

    ```ini title="/etc/systemd/system/percona-patroni.service"
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

5. Make `systemd` aware of the new service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl daemon-reload
    ```

6. Repeat steps 1-5 on the remaining nodes. In the end you must have the configuration file and the systemd unit file created on every node. 
7. Now it's time to start Patroni. You need the following commands on all nodes but not in parallel. Start with the `node1` first, wait for the service to come to live, and then proceed with the other nodes one-by-one, always waiting for them to sync with the primary node:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable --now patroni
    $ sudo systemctl restart patroni
    ```

   When Patroni starts, it initializes PostgreSQL (because the service is not currently running and the data directory is empty) following the directives in the bootstrap section of the configuration file. 

8. Check the service to see if there are errors:

    ```{.bash data-prompt="$"}
    $ sudo journalctl -fu patroni
    ```

    A common error is Patroni complaining about the lack of proper entries in the pg_hba.conf file. If you see such errors, you must manually add or fix the entries in that file and then restart the service.

    Changing the patroni.yml file and restarting the service will not have any effect here because the bootstrap section specifies the configuration to apply when PostgreSQL is first started in the node. It will not repeat the process even if the Patroni configuration file is modified and the service is restarted. 

    If Patroni has started properly, you should be able to locally connect to a PostgreSQL node using the following command:

    ```{.bash data-prompt="$"}
    $ sudo psql -U postgres

    psql ({{dockertag}})
    Type "help" for help.

    postgres=#
    ```

9. When all nodes are up and running, you can check the cluster status using the following command:

    ```{.bash data-prompt="$"}
    $ sudo patronictl -c /etc/patroni/patroni.yml list
    ```
    
    The output resembles the following:

    ```{.text .no-copy}
    + Cluster: cluster_1 (7440127629342136675) -----+----+-------+
    | Member | Host       | Role    | State     | TL | Lag in MB |
    +--------+------------+---------+-----------+----+-----------+
    | node1  | 10.0.100.1 | Leader  | running   |  1 |           |
    | node2  | 10.0.100.2 | Replica | streaming |  1 |         0 |
    | node3  | 10.0.100.3 | Replica | streaming |  1 |         0 |
    +--------+------------+---------+-----------+----+-----------+
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

## Next steps

[Configure pgBackRest](pgbackrest.md){.md-button}


