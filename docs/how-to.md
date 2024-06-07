# How to

## How to configure ETCD nodes simultaneously

!!! note 

    We assume you have a deeper knowledge of how ETCD works. Otherwise, refer to the configuration where you add ETCD nodes one by one. 

Instead of adding `etcd` nodes one by one, you can configure and start all nodes in parallel. 

1. Create ETCD configuration file on every node. You can edit the sample configuration file `/etc/etcd/etcd.conf.yaml` or create your own one. Replace the node names and IP addresses with the actual names and IP addresses of your nodes:

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
         name: 'node1'
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
    ```

    During the node start, ETCD searches for other cluster nodes defined in the configuration. If the other nodes are not yet running, the start may fail by a quorum timeout. This is expected behavior. Try starting all nodes again at the same time for the ETCD cluster to be created.

3. Check the etcd cluster members.  Connect to one of the nodes and run the following command:

    ```{.bash data-prompt="$"}
    $ sudo etcdctl member list
    ```

    The output resembles the following:

    ```
    2d346bd3ae7f07c4: name=node2 peerURLs=http://10.104.0.2:2380 clientURLs=http://10.104.0.2:2379 isLeader=false
    8bacb519ebdee8db: name=node3 peerURLs=http://10.104.0.3:2380 clientURLs=http://10.104.0.3:2379 isLeader=false
    c5f52ea2ade25e1b: name=node1 peerURLs=http://10.104.0.1:2380 clientURLs=http://10.104.0.1:2379 isLeader=true
    ```