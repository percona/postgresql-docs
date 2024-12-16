# High Availability in PostgreSQL with Patroni

PostgreSQL has been widely adopted as a modern, high-performance transactional database. A highly available PostgreSQL cluster can withstand failures caused by network outages, resource saturation, hardware failures, operating system crashes or unexpected reboots. Such cluster is often a critical component of the enterprise application landscape, where [four nines of availability :octicons-link-external-16:](https://en.wikipedia.org/wiki/High_availability#Percentage_calculation) is a minimum requirement. 

There are several methods to achieve high availability in PostgreSQL. This solution document provides [Patroni](#patroni) - the open-source extension to facilitate and manage the deployment of high availability in PostgreSQL.

??? admonition "High availability methods"

    There are several native methods for achieving high availability with PostgreSQL:

    - shared disk failover, 
    - file system replication, 
    - trigger-based replication, 
    - statement-based replication, 
    - logical replication, 
    - Write-Ahead Log (WAL) shipping, and
    - [streaming replication](#streaming-replication)


    ## Streaming replication

    Streaming replication is part of Write-Ahead Log shipping, where changes to the WALs are immediately made available to standby replicas. With this approach, a standby instance is always up-to-date with changes from the primary node and can assume the role of primary in case of a failover.


    ### Why native streaming replication is not enough

    Although the native streaming replication in PostgreSQL supports failing over  to the primary node, it lacks some key features expected from a truly highly-available solution. These include:


    * No consensus-based promotion of a “leader” node during a failover
    * No decent capability for monitoring cluster status 
    * No automated way to bring back the failed primary node to the cluster
    * A manual or scheduled switchover is not easy to manage 

    To address these shortcomings, there are a multitude of third-party, open-source extensions for PostgreSQL. The challenge for a database administrator here is to select the right utility for the current scenario. 

    Percona Distribution for PostgreSQL solves this challenge by providing the [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) extension for achieving PostgreSQL high availability.

## Patroni

[Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) is a Patroni is an open-source tool that helps to deploy, manage, and monitor highly available PostgreSQL clusters using physical streaming replication. Patroni relies on a distributed configuration store like ZooKeeper, etcd, Consul or Kubernetes to store the cluster configuration. 

### Key benefits of Patroni:

* Continuous monitoring and automatic failover
* Manual/scheduled switchover with a single command
* Built-in automation for bringing back a failed node to cluster again.
* REST APIs for entire cluster configuration and further tooling.
* Provides infrastructure for transparent application failover
* Distributed consensus for every action and configuration.
* Integration with Linux watchdog for avoiding split-brain syndrome.

## etcd

As stated before, Patroni uses a distributed configuration store to store the cluster configuration, health and status.The most popular implementation of the distributed configuration store is etcd due to its simplicity, consistency and reliability. Etcd not only stores the cluster data, it also handles the election of a new primary node (a leader in ETCD terminology).

etcd is deployed as a cluster for fault-tolerance. An etcd cluster needs a majority of nodes, a quorum, to agree on updates to the cluster state. 

The recommended approach is to deploy an odd-sized cluster (e.g. 3, 5 or 7 nodes). The odd number of nodes ensures that there is always a majority of nodes available to make decisions and keep the cluster running smoothly. This majority is crucial for maintaining consistency and availability, even if one node fails. For a cluster with n members, the majority is (n/2)+1. 

To better illustrate this concept, let's take an example of clusters with 3 nodes and 4 nodes. 

In a 3-node cluster, if one node fails, the remaining 2 nodes still form a majority (2 out of 3), and the cluster can continue to operate.

In a 4-nodes cluster, if one node fails, there are only 3 nodes left, which is not enough to form a majority (3 out of 4). The cluster stops functioning.

In this solution we use a 3-nodes etcd cluster that resides on the same hosts with PostgreSQL and Patroni. Though 

!!! admonition "See also"

    - [Patroni documentation :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/SETTINGS.html#settings)

    - Percona Blog: 

        - [PostgreSQL HA with Patroni: Your Turn to Test Failure Scenarios :octicons-link-external-16:](https://www.percona.com/blog/2021/06/11/postgresql-ha-with-patroni-your-turn-to-test-failure-scenarios/) 

## Architecture layout

The following diagram shows the architecture of a three-node PostgreSQL cluster with a single-leader node. 

![Architecture of the three-node, single primary PostgreSQL cluster](../_images/diagrams/ha-architecture-patroni.png)

### Components

The components in this architecture are:

- PostgreSQL nodes 
- Patroni - a template for configuring a highly available PostgreSQL cluster.

- etcd - a Distributed Configuration store that stores the state of the PostgreSQL cluster. 

- HAProxy - the load balancer for the cluster and is the single point of entry to client applications. 

- pgBackRest - the backup and restore solution for PostgreSQL

- Percona Monitoring and Management (PMM) - the solution to monitor the health of your cluster 

### How components work together

Each PostgreSQL instance in the cluster maintains consistency with other members through streaming replication. Each instance hosts Patroni - a cluster manager that monitors the cluster health. Patroni relies on the operational etcd cluster to store the cluster configuration and sensitive data about the cluster health there. 

Patroni periodically sends heartbeat requests with the cluster status to etcd. etcd writes this information to disk and sends the response back to Patroni. If the current primary fails to renew its status as leader within the specified timeout, Patroni updates the state change in etcd, which uses this information to elect the new primary and keep the cluster up and running.

The connections to the cluster do not happen directly to the database nodes but are routed via a connection proxy like HAProxy. This proxy determines the active node by querying the Patroni REST API.

## Next steps

[Deploy on Debian or Ubuntu](ha-setup-apt.md){.md-button}
[Deploy on RHEL or derivatives](ha-setup-yum.md){.md-button}

