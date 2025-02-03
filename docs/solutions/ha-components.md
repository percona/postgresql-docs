# How components work together

This document explains how components of the proposed [high-availability architecture](ha-architecture.md) work together.

## Database layer

Let's start with the database layer. Every database node hosts PostgreSQL and Patroni instances.

Each PostgreSQL instance in the cluster maintains consistency with other members through streaming replication. Streaming replication is asynchronous by default, meaning the primary does not wait for the secondaries to acknowledge the receipt of the data to consider the transaction complete.

Each Patroni instance runs on top of and manages its own PostgreSQL instance. Patroni is responsible for creating and managing the PostgreSQL cluster. It performs the initial cluster initialization and monitors the cluster state. 

Note that the PostgreSQL cluster and Patroni cluster are the same thing, and we will use these names interchangeably.

When you start a Patroni cluster, all PostgreSQL nodes are started as standby nodes. To ensure that only one instance becomes the primary, Patroni uses the `etcd` locking mechanism. This mechanism ensures that only a single process can hold a resource at a time avoiding race conditions and inconsistencies. 

The first instance to successfully acquire the lock with a lease becomes the primary PostgreSQL node, and the other instances remain in the standby mode, waiting for the lock to be released.

If the current primary node crashes, its lease on the lock expires. The lock is automatically released after its expiration time. A new election then begins, and a standby node attempts to acquire the lock to become the new primary.

Patroni uses not only `etcd` locking mechanism. It also uses `etcd` to store the current state of the cluster, ensuring that all nodes are aware of the latest changes. 

## `etcd` layer

Let's move to the etcd layer. It consists only of `etcd`. This is a crucial component so it's important to understand it.

`etcd` is a distributed key-value store that helps you store and manage cluster configuration data and perform distributed coordination of a PostgreSQL cluster.

`etcd` runs as a cluster of nodes that communicate with each other to maintain a consistent state. The primary node in the cluster is called the leader, and the remaining nodes are the followers.

### How `etcd` works

Each node in the cluster stores data in a structured format and keeps a copy of the same data to ensure redundancy and fault tolerance. When you write data to `etcd`, the change is sent to the leader node, which then replicates it to the other nodes in the cluster. This ensures that all nodes remain synchronized and maintain data consistency.

### Leader election

An `etcd` cluster can have one and only one leader node at a time. The leader is responsible for receiving client requests, proposing changes, and ensuring they are replicated to the followers. When an `etcd` cluster starts, or if the current leader fails, the nodes hold an election to choose a new leader. Each node waits for a random amount of time before sending a vote request to other nodes, and the first node to get a majority of votes becomes the new leader. The cluster remains available as long as a majority of nodes (quorum) are still running.

### How many members to have in a cluster

The recommended approach is to deploy an odd-sized cluster (e.g., 3, 5, or 7 nodes). The odd number of nodes ensures that there is always a majority of nodes available to make decisions and keep the cluster running smoothly. This majority is crucial for maintaining consistency and availability, even if one node fails. For a cluster with n members, the majority is (n/2)+1.

To better illustrate this concept, take an example of clusters with 3 nodes and 4 nodes. In a 3-node cluster, if one node fails, the remaining 2 nodes still form a majority (2 out of 3), and the cluster can continue to operate. In a 4-node cluster, if one node fails, there are only 3 nodes left, which is not enough to form a majority (3 out of 4). The cluster stops functioning.

### `etcd` Raft consensus

The heart of `etcd`'s reliability is the Raft consensus algorithm. Raft ensures that all nodes in the cluster agree on the same data. This ensures a consistent view of the data, even if some nodes are unavailable or experiencing network issues. 

A good example of the role of Raft in `etcd` is the situation when there is no majority. If a majority of nodes can't communicate (for example, due to network partitions), no new leader can be elected, and no new changes can be committed. This prevents the system from getting into an inconsistent state. The system waits for the network to heal and a majority to be re-established. This is crucial for data integrity.

### Deployment considerations

In this solution, we deploy `etcd` on the same nodes where PostgreSQL and Patroni are running. Such a deployment is simpler to set up and maintain. It suits for small scale, testing environments or environments with low load.

For improved high availability, resource isolation, and fault tolerance, you can deploy `etcd` on separate nodes. Such a deployment also enables you to scale the `etcd` cluster separately from PostgreSQL based on the load and thus achieve better performance. Note that separate deployment increases the complexity of the infrastructure and requires additional effort on maintenance. Also, pay close attention to network configuration to eliminate the latency that might occur due to the communication between `etcd` and Patroni nodes over the network.

## Load balancing layer

This layer consists of HAProxy and keepalived.

HAProxy acts as a single point of entry to your cluster for client applications. It accepts all requests from client applications and distributes the load evenly across the cluster nodes. HAProxy determines the active node by querying the Patroni REST API.

HAProxy must be also redundant. You need minimum 2 HAProxy instances (one active and another one standby) to eliminate the single point of failure and be able to perform failover. This is where keepalived comes in. 

Keepalived is the failover tool for HAProxy. It provides the virtual IP address (VIP) for HAProxy and monitors its state. When the current active HAProxy node is down, it transfers the VIP to the remaining node and fails over the services there.

## Backup layer

## Monitoring layer

