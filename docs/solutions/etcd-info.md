# ETCD

`etcd` is one of the key components in high availability architecture, therefore, it's important to understand it.

`etcd` is a distributed key-value consensus store that helps applications store and manage cluster configuration data and perform distributed coordination of a PostgreSQL cluster.

`etcd` runs as a cluster of nodes that communicate with each other to maintain a consistent state. The primary node in the cluster is called the "leader", and the remaining nodes are the "followers".

## How `etcd` works

Each node in the cluster stores data in a structured format and keeps a copy of the same data to ensure redundancy and fault tolerance. When you write data to `etcd`, the change is sent to the leader node, which then replicates it to the other nodes in the cluster. This ensures that all nodes remain synchronized and maintain data consistency.

When a client wants to change data, it sends the request to the leader. The leader accepts the writes and proposes this change to the followers. The followers vote on the proposal. If a majority of followers agree (including the leader), the change is committed, ensuring consistency. The leader then confirms the change to the client.

This flow corresponds to the Raft consensus algorithm, based on which `etcd` works. Read morea bout it the [`ectd` Raft consensus](#etcd-raft-consensus) section.

## Leader election

An `etcd` cluster can have only one leader node at a time. The leader is responsible for receiving client requests, proposing changes, and ensuring they are replicated to the followers. When an `etcd` cluster starts, or if the current leader fails, the nodes hold an election to choose a new leader. Each node waits for a random amount of time before sending a vote request to other nodes, and the first node to get a majority of votes becomes the new leader. The cluster remains available as long as a majority of nodes (quorum) are still running.

### How many members to have in a cluster

The recommended approach is to deploy an odd-sized cluster (e.g., 3, 5, or 7 nodes). The odd number of nodes ensures that there is always a majority of nodes available to make decisions and keep the cluster running smoothly. This majority is crucial for maintaining consistency and availability, even if one node fails. For a cluster with `n` members, the majority is `(n/2)+1`.

To better illustrate this concept, take an example of clusters with 3 nodes and 4 nodes. In a 3-node cluster, if one node fails, the remaining 2 nodes still form a majority (2 out of 3), and the cluster can continue to operate. In a 4-node cluster, if one node fails, there are only 3 nodes left, which is not enough to form a majority (3 out of 4). The cluster stops functioning.

## `etcd` Raft consensus

The heart of `etcd`'s reliability is the Raft consensus algorithm. Raft ensures that all nodes in the cluster agree on the same data. This ensures a consistent view of the data, even if some nodes are unavailable or experiencing network issues. 

An example of the Raft's role in `etcd` is the situation when there is no majority in the cluster. If a majority of nodes can't communicate (for example, due to network partitions), no new leader can be elected, and no new changes can be committed. This prevents the system from getting into an inconsistent state. The system waits for the network to heal and a majority to be re-established. This is crucial for data integrity.

You can also check [this resource :octicons-link-external-16:](https://thesecretlivesofdata.com/raft/) to learn more about Raft and understand it better.

## `etcd` logs and performance considerations

`etcd` keeps a detailed log of every change made to the data. These logs are essential for several reasons, including the ensurance of consistency, fault tolerance, leader elections, auditing, and others, maintaining a consistent state across nodes. For example, if a node fails, it can use the logs to catch up with the other nodes and restore its data. The logs also provide a history of all changes, which can be useful for debugging and security analysis if needed.

### Slow disk performance

`etcd` is very sensitive to disk I/O performance. Writing to the logs is a frequent operation and will be slow if the disk is slow. This can lead to timeouts, delaying consensus, instability, and even data loss. In extreme cases, slow disk performance can cause a leader to fail health checks, triggering unnecessary leader elections. Always use fast, reliable storage for `etcd`.

### Slow or high-latency networks

Communication between `etcd` nodes is critical. A slow or unreliable network can cause delays in replicating data, increasing the risk of stale reads. This can trigger premature timeouts leading to leader elections happening more frequently, and even delays in leader elections in some cases, impacting performance and stability. Also keep in mind that if nodes cannot reach each other in a timely manner, the cluster may lose quorum and become unavailable.

## etcd Locks

`etcd` provides a distributed locking mechanism, which helps applications coordinate actions across multiple nodes and access to shared resources preventing conflicts. Locks ensure that only one process can hold a resource at a time, avoiding race conditions and inconsistencies. Patroni is an example of an application that uses `etcd` locks for primary election control in the PostgreSQL cluster. 

### Deployment considerations

Running `etcd` on separate hosts has the following benefits:

* Both PostgreSQL and `etcd` are highly dependant on I/O. And running them on the separate hosts improves performance.

* Higher resilience. If one or even two PostgreSQL node crash, the `etcd` cluster remains healthy and can trigger a new primary election. 

* Scalability and better performance. You can scale the `etcd` cluster separately from PostgreSQL based on the load and thus achieve better performance.

Note that separate deployment increases the complexity of the infrastructure and requires additional effort on maintenance. Also, pay close attention to network configuration to eliminate the latency that might occur due to the communication between `etcd` and Patroni nodes over the network.

If a separate dedicated host for 1 is not a viable option, you can use the same host machines used for Patroni and PostgreSQL.

## Next steps

[Patroni](patroni-info.md){.md-button}