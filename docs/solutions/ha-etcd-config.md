# Etcd setup

In our solutions, we use etcd distributed configuration store. [Refresh your knowledge about etcd](ha-components.md#database-and-dsc-layers).

## Install etcd

Install etcd on all PostgreSQL nodes: `node1`, `node2` and `node3`.

=== ":material-debian: On Debian / Ubuntu"

    1. Install etcd:    

        ```{.bash data-prompt="$"}
        $ sudo apt install etcd etcd-server etcd-client 
        ```

    2. Stop and disable etcd:
    
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop etcd
        $ sudo systemctl disable etcd
        ```

=== ":material-redhat: On RHEL and derivatives"

    
    1. Install etcd. 

        ```{.bash data-prompt="$"}
        $ sudo yum install
        etcd python3-python-etcd\
        ```

    2. Stop and disable etcd:
    
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop etcd
        $ systemctl disable etcd
        ```

!!! note
    
    If you [installed etcd from tarballs](../tarball.md), you must first [enable it](../enable-extensions.md#etcd) before configuring it.

## Configure etcd

To get started with `etcd` cluster, you need to bootstrap it. This means setting up the initial configuration and starting the etcd nodes so they can form a cluster. There are the following bootstrapping mechanisms:  

* Static in the case when the IP addresses of the cluster nodes are known
* Discovery service - for cases when the IP addresses of the cluster are not known ahead of time.
    
Since we know the IP addresses of the nodes, we will use the static method. For using the discovery service, please refer to the [etcd documentation :octicons-link-external-16:](https://etcd.io/docs/v3.5/op-guide/clustering/#etcd-discovery){:target="_blank"}.

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
        	--initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} &
        ```

    === "node2"

        ```{.bash data-prompt="$"}
        THIS_NAME=${NAME_2}
        THIS_IP=${HOST_2}
        etcd --data-dir=data.etcd --name ${THIS_NAME} \
        	--initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
        	--advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
        	--initial-cluster ${CLUSTER} \
        	--initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} &
        ```

    === "node3"

        ```{.bash data-prompt="$"}
        THIS_NAME=${NAME_3}
        THIS_IP=${HOST_3}
        etcd --data-dir=data.etcd --name ${THIS_NAME} \
        	--initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
        	--advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
        	--initial-cluster ${CLUSTER} \
        	--initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} &
        ```

--8<-- "check-etcd.md"

## Next steps

[Patroni setup :material-arrow-right:](ha-patroni.md){.md-button}
