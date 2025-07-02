# How components work together

This document explains how components of the proposed [high-availability architecture](ha-architecture.md) work together.

## Database and DSC layers

Let's start with the database and DCS layers as they are interconnected and work closely together. 

Every database node hosts PostgreSQL and Patroni instances.

Each PostgreSQL instance in the cluster maintains consistency with other members through streaming replication. Streaming replication is asynchronous by default, meaning that the primary does not wait for the secondaries to acknowledge the receipt of the data to consider the transaction complete.

Each Patroni instance manages its own PostgreSQL instance. This means that Patroni starts and stops PostgreSQL and manages its configuration, being a sophisticated service manager for a PostgreSQL cluster.

Patroni also can make an initial cluster initialization, monitor the cluster state and take other automatic actions if needed. To do so, Patroni relies on and uses the Distributed Configuration Store (DCS), represented by `etcd` in our architecture. 

Though Patroni supports various Distributed Configuration Stores like ZooKeeper, etcd, Consul or Kubernetes, we recommend and support `etcd` as the most popular DCS due to its simplicity, consistency and reliability.   

Note that the PostgreSQL high availability (HA) cluster and Patroni cluster are the same thing, and we will use these names interchangeably.

When you start Patroni, it writes the cluster configuration information in `etcd`. During the initial cluster initialization, Patroni uses the `etcd` locking mechanism to ensure that only one instance becomes the primary. This mechanism ensures that only a single process can hold a resource at a time avoiding race conditions and inconsistencies. 

You start Patroni instances one by one so the first instance acquires the lock with a lease in `etcd` and becomes the primary PostgreSQL node. The other instances join the primary as replicas, waiting for the lock to be released.

If the current primary node crashes, its lease on the lock in `etcd` expires. The lock is automatically released after its expiration time. `etcd` the starts a new election and a standby node attempts to acquire the lock to become the new primary.

Patroni uses not only `etcd` locking mechanism. It also uses `etcd` to store the current state of the cluster, ensuring that all nodes are aware of the latest topology and status. 

Another important component is the watchdog. It runs on each database node. The purpose of watchdog is to prevent split-brain scenarios, where multiple nodes might mistakenly think they are the primary node. The watchdog monitors the node's health by receiving periodic "keepalive" signals from Patroni. If these signals stop due to a crash, high system load or any other reason, the watchdog resets the node to ensure it does not cause inconsistencies.

## Load balancing layer

This layer consists of HAProxy as the connection router and load balancer.

HAProxy acts as a single point of entry to your cluster for client applications. It accepts all requests from client applications and distributes the load evenly across the cluster nodes. It can route read/write requests to the primary and read-only requests to the secondary nodes. This behavior is defined within HAProxy configuration. To determine the current primary node, HAProxy queries the Patroni REST API.

HAProxy must be also redundant. Each application server or Pod can have its own HAProxy. If it cannot have own HAProxy, you can deploy HAProxy outside the application layer. This may introduce additional network hops and a failure point. 

If you are deploying HAProxy outside the application layer, you need a minimum of 2 HAProxy nodes (one is active and another one standby) to avoid a single point of failure. These instances share a floating virtual IP address using Keepalived.

Keepalived acts as the failover tool for HAProxy. It provides the virtual IP address (VIP) for HAProxy and monitors its state. When the current active HAProxy node is down, it transfers the VIP to the remaining node and fails over the services there.

## Services layer

Finally, the services layer is represented by `pgBackRest` and PMM. 

`pgBackRest` can manage a dedicated backup server or make backups to the cloud. `pgBackRest` agent are deployed on every database node. `pgBackRest` can utilize standby nodes to offload the backup load from the primary. However, WAL archiving is happening only from the primary node. By communicating with its agents,`pgBackRest` determines the current cluster topology and uses the nodes to make backups most effectively without any manual reconfiguration at the event of a switchover or failover.

The monitoring solution is optional but nice to have. It enables you to monitor the health of your high-availability architecture, receive timely alerts should performance issues occur and proactively react to them.

