> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/16/llms.txt).

# Etcd setup

In our solutions, we use etcd distributed configuration store. [Refresh your knowledge about etcd](https://docs.percona.com/postgresql/16/solutions/etcd-info.html).

## Install etcd

Install etcd on all PostgreSQL nodes: `node1`, `node2` and `node3`.

**On Debian / Ubuntu**

1. Install etcd:

   ```
   $ sudo apt install etcd etcd-server etcd-client
   ```

1. Stop and disable etcd:

   ```
   $ sudo systemctl stop etcd
   $ sudo systemctl disable etcd
   ```

**On RHEL and derivatives**

1. Install etcd.

   ```
   $ sudo yum install etcd python3-python-etcd
   ```

1. Stop and disable etcd:

   ```
   $ sudo systemctl stop etcd
   $ sudo systemctl disable etcd
   ```

Note

If you [installed etcd from tarballs](https://docs.percona.com/postgresql/16/tarball.html), you must first [enable it](https://docs.percona.com/postgresql/16/enable-extensions.html#etcd) before configuring it.

## Configure etcd

To get started with `etcd` cluster, you need to bootstrap it. This means setting up the initial configuration and starting the etcd nodes so they can form a cluster. There are the following bootstrapping mechanisms:

- Static in the case when the IP addresses of the cluster nodes are known
- Discovery service - for cases when the IP addresses of the cluster are not known ahead of time.

Since we know the IP addresses of the nodes, we will use the static method. For using the discovery service, please refer to the [etcd documentation](https://etcd.io/docs/v3.5/op-guide/clustering/#etcd-discovery) .

We will configure and start all etcd nodes in parallel. This can be done either by modifying each node’s configuration or using the command line options. Use the method that you prefer more.

### Method 1. Modify the configuration file

1. Create the etcd configuration file on every node. You can edit the sample configuration file `/etc/etcd/etcd.conf.yaml` or create your own one. Replace the node names and IP addresses with the actual names and IP addresses of your nodes.

   **node1**

   /etc/etcd/etcd.conf.yaml

   ```
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

   **node2**

   /etc/etcd/etcd.conf.yaml

   ```
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

   **node3**

   /etc/etcd/etcd.conf.yaml

   ```
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

1. Enable and start the `etcd` service on all nodes:

   ```
   $ sudo systemctl enable --now etcd
   $ sudo systemctl status etcd
   ```

   During the node start, etcd searches for other cluster nodes defined in the configuration. If the other nodes are not yet running, the start may fail by a quorum timeout. This is expected behavior. Try starting all nodes again at the same time for the etcd cluster to be created.

1. Check the etcd cluster members. Use `etcdctl` for this purpose. Ensure that `etcdctl` interacts with etcd using API version 3 and knows which nodes, or endpoints, to communicate with. For this, we will define the required information as environment variables. Run the following commands on one of the nodes:

   ```
   export ETCDCTL_API=3
   HOST_1=10.104.0.1
   HOST_2=10.104.0.2
   HOST_3=10.104.0.3
   ENDPOINTS=$HOST_1:2379,$HOST_2:2379,$HOST_3:2379
   ```

1. Now, list the cluster members and output the result as a table as follows:

   ```
   $ sudo etcdctl --endpoints=$ENDPOINTS -w table member list
   ```

   Sample output

   ```
   +------------------+---------+-------+------------------------+----------------------------+------------+
   |        ID        | STATUS  | NAME  |         PEER ADDRS     |        CLIENT ADDRS        | IS LEARNER |
   +------------------+---------+-------+------------------------+----------------------------+------------+
   | 4788684035f976d3 | started | node2 | http://10.104.0.2:2380 | http://192.168.56.102:2379 |      false |
   | 67684e355c833ffa | started | node3 | http://10.104.0.3:2380 | http://192.168.56.103:2379 |      false |
   | 9d2e318af9306c67 | started | node1 | http://10.104.0.1:2380 | http://192.168.56.101:2379 |      false |
   +------------------+---------+-------+------------------------+----------------------------+------------+
   ```

1. To check what node is currently the leader, use the following command

   ```
   $ sudo etcdctl --endpoints=$ENDPOINTS -w table endpoint status
   ```

   Sample output

   ```
   +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
   |      ENDPOINT   |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
   +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
   | 10.104.0.1:2379 | 9d2e318af9306c67 |  3.5.16 |   20 kB |      true |      false |         2 |         10 |                 10 |        |
   | 10.104.0.2:2379 | 4788684035f976d3 |  3.5.16 |   20 kB |     false |      false |         2 |         10 |                 10 |        |
   | 10.104.0.3:2379 | 67684e355c833ffa |  3.5.16 |   20 kB |     false |      false |         2 |         10 |                 10 |        |
   +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
   ```

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

1. Start each etcd node in parallel using the following command:

   **node1**

   ```
   THIS_NAME=${NAME_1}
   THIS_IP=${HOST_1}
   etcd --data-dir=data.etcd --name ${THIS_NAME} \
       --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
       --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
       --initial-cluster ${CLUSTER} \
       --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} &
   ```

   **node2**

   ```
   THIS_NAME=${NAME_2}
   THIS_IP=${HOST_2}
   etcd --data-dir=data.etcd --name ${THIS_NAME} \
       --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
       --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
       --initial-cluster ${CLUSTER} \
       --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} &
   ```

   **node3**

   ```
   THIS_NAME=${NAME_3}
   THIS_IP=${HOST_3}
   etcd --data-dir=data.etcd --name ${THIS_NAME} \
       --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
       --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
       --initial-cluster ${CLUSTER} \
       --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN} &
   ```

1. Check the etcd cluster members. Use `etcdctl` for this purpose. Ensure that `etcdctl` interacts with etcd using API version 3 and knows which nodes, or endpoints, to communicate with. For this, we will define the required information as environment variables. Run the following commands on one of the nodes:

   ```
   export ETCDCTL_API=3
   HOST_1=10.104.0.1
   HOST_2=10.104.0.2
   HOST_3=10.104.0.3
   ENDPOINTS=$HOST_1:2379,$HOST_2:2379,$HOST_3:2379
   ```

1. Now, list the cluster members and output the result as a table as follows:

   ```
   $ sudo etcdctl --endpoints=$ENDPOINTS -w table member list
   ```

   Sample output

   ```
   +------------------+---------+-------+------------------------+----------------------------+------------+
   |        ID        | STATUS  | NAME  |         PEER ADDRS     |        CLIENT ADDRS        | IS LEARNER |
   +------------------+---------+-------+------------------------+----------------------------+------------+
   | 4788684035f976d3 | started | node2 | http://10.104.0.2:2380 | http://192.168.56.102:2379 |      false |
   | 67684e355c833ffa | started | node3 | http://10.104.0.3:2380 | http://192.168.56.103:2379 |      false |
   | 9d2e318af9306c67 | started | node1 | http://10.104.0.1:2380 | http://192.168.56.101:2379 |      false |
   +------------------+---------+-------+------------------------+----------------------------+------------+
   ```

1. To check what node is currently the leader, use the following command

   ```
   $ sudo etcdctl --endpoints=$ENDPOINTS -w table endpoint status
   ```

   Sample output

   ```
   +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
   |      ENDPOINT   |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
   +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
   | 10.104.0.1:2379 | 9d2e318af9306c67 |  3.5.16 |   20 kB |      true |      false |         2 |         10 |                 10 |        |
   | 10.104.0.2:2379 | 4788684035f976d3 |  3.5.16 |   20 kB |     false |      false |         2 |         10 |                 10 |        |
   | 10.104.0.3:2379 | 67684e355c833ffa |  3.5.16 |   20 kB |     false |      false |         2 |         10 |                 10 |        |
   +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
   ```

## Next steps

[Patroni setup](https://docs.percona.com/postgresql/16/solutions/ha-patroni.html)
