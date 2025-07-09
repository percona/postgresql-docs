# Patroni

Patroni is an open-source tool designed to manage and automate the high availability (HA) of PostgreSQL clusters. It ensures that your PostgreSQL database remains available even in the event of hardware failures, network issues or other disruptions. Patroni achieves this by using distributed consensus stores like ETCD, Consul, or ZooKeeper to manage cluster state and automate failover processes. We'll use [`etcd`](etcd-info.md) in our architecture.

## Key benefits of Patroni for high availability

- Automated failover and promotion of a new primary in case of a failure;
- Prevention and protection from split-brain scenarios (where two nodes believe they are the primary and both accept transactions). Split-brain can lead to serious logical corruptions such as wrong, duplicate data or data loss, and to associated business loss and risk of litigation;
- Simplifying the management of PostgreSQL clusters across multiple data centers;
- Self-healing via automatic restarts of failed PostgreSQL instances or reinitialization of broken replicas.
- Integration with tools like `pgBackRest`, `HAProxy`, and monitoring systems for a complete HA solution.

## How Patroni works

Patroni uses the `etcd` distributed consensus store to coordinate the state of a PostgreSQL cluster for the following operations:

1. Cluster state management:

    - After a user installs and configures Patroni, Patroni takes over the PostgreSQL service administration and configuration;
    - Patroni maintains the cluster state data such as PostgreSQL configuration, information about which node is the primary and which are replicas, and their health status.
    - Patroni manages PostgreSQL configuration files such as`postgresql.conf` and `pg_hba.conf` dynamically, ensuring consistency across the cluster.
    - A Patroni agent runs on each cluster node and communicates with `etcd` and other nodes.

2. Primary node election:

    - Patroni initiates a primary election process after the cluster is initialized;
    - Patroni initiates a failover process if the primary node fails;
    - When the old primary is recovered, it rejoins the cluster as a new replica;
    - Every new node added to the cluster joins it as a new replica;
    - `etcd` and the Raft consensus algorithm ensures that only one node is elected as the new primary, preventing split-brain scenarios.

3. Automatic failover:

    - If the primary node becomes unavailable, Patroni initiates a new primary election process with the most up-to-date replicas;
    - When a node is elected it is automatically promoted to primary;
    - Patroni updates the `etcd` consensus store and reconfigures the remaining replicas to follow the new primary.

4. Health checks:

    - Patroni continuously monitors the health of all PostgreSQL instances;
    - If a node fails or becomes unreachable, Patroni takes corrective actions by restarting PostgreSQL or initiating a failover process.

## Split-brain prevention

Split-brain is an issue, which occurs when two or more nodes believe they are the primary, leading to data inconsistencies.

Patroni prevents split-brain by using a three-layer protection and prevention mechanism where the `etcd` distributed locking mechanism plays a key role:

* At the Patroni layer, a node needs to acquire a leader key in the race before promoting itself as the primary. If the node cannot to renew its leader key, Patroni demotes it to a replica.
* The `etcd` layer uses the Raft consensus algorithm to allow only one node to acquire the leader key.
- At the OS and hardware layers, Patroni uses Linux Watchdog to perform [STONITH](https://en.wikipedia.org/wiki/Fencing_(computing)#STONITH) / fencing and terminate a PostgreSQL instance to prevent a split-brain scenario.

One important aspect of how Patroni works is that it requires a quorum (the majority) of nodes to agree on the cluster state, preventing isolated nodes from becoming a primary. The quorum strengthens Patroni's capabilities of preventing split-brain.

## Watchdog

Patroni can use a watchdog mechanism to improve resilience. But what is watchdog?

A watchdog is a mechanism that ensures a system can recover from critical failures. In the context of Patroni, a watchdog is used to forcibly restart the node and terminate a failed primary node to prevent split-brain scenarios.

While Patroni itself is designed for high availability, a watchdog provides an extra layer of protection against system-level failures that Patroni might not be able to detect, such as kernel panics or hardware lockups.  If the entire operating system becomes unresponsive, Patroni might not be able to function correctly. The watchdog operates independently so it can detect that the server is unresponsive and reset it, bringing it back to a known good state.

Watchdog adds an extra layer of safety, because it helps protecting against scenarios where the `etcd` consensus store is unavailable or network partitions occur.

There are 2 types of watchdogs:

- Hardware watchdog: A physical device that reboots the server if the operating system becomes unresponsive.
- Software watchdog (also called a softdog): A software-based watchdog timer tha emulates the functionality of a hardware watchdog but is implemented entirely in software. It is part of the Linux kernel's watchdog infrastructure and is useful in systems that lack dedicated hardware watchdog timers. The softdog monitors the system and takes corrective actions such as killing processes or rebooting the node.

Most of the servers in the cloud nowadays use a softdog.

## Integration with other tools

Patroni integrates well with other tools to create a comprehensive high-availability solution. In our architecture, such tools are:

* HAProxy to check the current topology and route the traffic to both the primary and replica nodes, balancing the load among them,
* pgBackRest to help to ensure robust backup and restore,
* PMM for monitoring.

Patroni provides hooks that allow you to customize its behavior. You can use hooks to execute custom scripts or commands at various stages of Patroni lifecycle, such as before and after failover, or when a new instance joins the cluster. Thereby you can integrate Patroni with other systems and automate various tasks. For example, use a hook to update the monitoring system when a failover occurs.

## Next step

[HAProxy](haproxy-info.md){.md-button}