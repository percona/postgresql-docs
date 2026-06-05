# High Availability in PostgreSQL with Patroni

Whether you are a small startup or a big enterprise, downtime of your services may cause severe consequences, such as loss of customers, impact on your reputation, and penalties for not meeting the Service Level Agreements (SLAs). That’s why ensuring a highly-available deployment is crucial.

But what does it mean, high availability (HA)? And how to achieve it? This document answers these questions. 

After reading this document, you will learn the following:

* [What is high availability](#what-is-high-availability).
* The recommended [reference architecture](ha-architecture.md) to achieve it.
* How to deploy it using our step-by-step deployment guides for each component. The deployment instructions focus on the minimalistic approach to high availability that we recommend. It also gives instructions how to deploy additional components that you can add when your infrastructure grows.
* How to verify that your high availability deployment works as expected, providing replication and failover with the [testing guidelines](ha-test.md)
* Additional components that you can add to address existing limitations on your infrastructure. An example of such limitations can be the ones on application driver/connectors, or the lack of the connection pooler at the application framework.

## What is high availability

High availability (HA) is the ability of the system to operate continuously without the interruption of services. During the outage, the system must be able to transfer the services from the failed component to the healthy ones so that they can take over its responsibility. The system must have sufficient automation to perform this transfer without the need for human intervention, minimizing disruption.

Overall, High availability is about:

1. Reducing the chance of failures.
2. Elimination of single-point-of-failure (SPOF).
3. Automatic detection of failures.
4. Automatic action to reduce the impact.

### How to achieve it? 

A short answer is: add redundancy to your deployment, eliminate a single point of failure (SPOF) and have the mechanism to transfer the services from a failed member to the healthy one. 

For a long answer, let's break it down into steps. 

#### Step 1. Replication

First, you should have more than one copy of your data. This means, you need to have several instances of your database where one is the primary instance that accepts reads and writes. Other instances are replicas – they must have an up-to-date copy of the data from the primary and remain in sync with it. They may also accept reads to offload your primary. 

You must deploy these instances on separate hardware (servers or nodes) and use separate storage for storing the data. This way you eliminate a single point of failure for your database.

The minimum number of database nodes is two: one primary and one replica. 

The recommended deployment is a three-instance cluster consisting of one primary and two replica nodes. The replicas receive the data via the replication mechanism. 

![Primary-replica setup](../_images/diagrams/ha-overview-replication.svg)

PostgreSQL natively supports logical and streaming replication. To achieve high availability, use streaming replication instead of logical replication. This ensures an exact copy of the entire PostgreSQL instance is maintained and ready to take over, while reducing the delay between primary and replica nodes to the lowest possible level to minimize the risk of data loss.

#### Step 2. Switchover and Failover

You may want to transfer the primary role from one machine to another. This action is called a **manual switchover**. A reason for that could be the following:

* A planned maintenance on the OS level, like applying quarterly security updates or replacing some of the end-of-life components from the server
* Troubleshooting some of the problems, like high network latency.

Switchover is a manual action performed when you decide to transfer the primary role to another node. The high-availability framework makes this process easier and helps minimize downtime during maintenance, thereby improving overall availability.

There could be an unexpected situation where a primary node is down or not responding. Reasons for that can be different, from hardware or network issues to software failures, power outages and the like. In such situations, the high-availability solution should automatically detect the problem, find out a suitable candidate from the remaining nodes and transfer the primary role to the best candidate (promote a new node to become a primary). Such automatic remediation is called **Failover**.

![Failover](../_images/diagrams/ha-overview-failover.svg)

You can do a manual failover when automatic remediation fails, for example, due to:

* A complete network partitioning.
* High-availability framework not being able to find a good candidate.
* The insufficient number of nodes remaining for a new primary election.

The good high-availability framework allows a human operator / administrator to easily take the full control and do a manual failover when needed.

#### Step 3. Connection routing and load balancing

After a switchover or failover, routing the connection to new nodes is a major challenge. A traditional approach is to use DNS resolution. However, there are a few drawbacks to DNS-based routing. All connections are typically routed to the primary node, which is acceptable if standby nodes are not required to serve read-only queries. In addition, delays in DNS record propagation can affect new connections established immediately after a switchover.

A better option is to use the features of application connectors / drivers to request the desired role of the node. Drivers like the JDBC driver for PostgreSQL are well known for supporting this feature for quite some time. Almost all application drivers these days have this feature, including those based on libpq. This is considered the best option for modern architectures.

An option widely used with PostgreSQL is the use of connection proxies like HAProxy to facilitate separate connection endpoints for both read-only and read-write connections.
![Load-balancer](../_images/diagrams/ha-overview-load-balancer.svg)
The proxy becomes a single point of entry for all incoming connections. To mitigate the risk of a single proxy failure, multiple proxy instances should be deployed — preferably a separate proxy for each application server.
However, this approach adds an additional network hop, which can adversely affect performance. The proxy may also mask client IP addresses and affect traceability.
On the other hand, proxies can distribute read requests across replicas to evenly spread the load.

Before proceeding to redirect read-only connections to standby nodes, it is important to understand the trade-offs

##### Connection Routing: Primary vs. Standby Node
The optimal approach is to design the application to intelligently route connections to either the Primary or Standby node based on specific business logic and workload requirements.

* **Primary Connections (Higher Cost):** Connections to the primary node are highly critical and in high demand, as the primary handles all write operations.

* **Standby Connections (Lower Cost):** Read-only connections to a standby node are computationally "cheaper" because their resource consumption does not directly impact the transaction throughput or performance of the primary node.
  
While offloading read traffic to a standby node frees up primary resources, the application must be architected to handle the following technical limitations:

1. **Strict Isolation & ACID Limitations:** Standby nodes cannot fully participate in the primary's active concurrency control mechanisms. Consequently, strict, real-time ACID compliance for transactions cannot be guaranteed on the standby side.

2. **Eventual Consistency:** Due to replication lag, data on the standby node is eventually consistent rather than immediately consistent. Queries routed here may occasionally read stale or obsolete data.

3. **Locking Restrictions:** Standby sessions do not participate in exclusive locks held on the primary node. Even basic shared locks (like AccessShareLock) cannot block DDL or data modifications occurring on the primary.

4. **Query Conflicts and Cancellations:** Because the standby node lacks active concurrency control, conflicts between long-running read queries on the standby and WAL (Write-Ahead Log) replay from the primary are common. This can lead to automatic statement cancellations on the standby, which the application logic must be resilient enough to catch and retry.

5. **Transaction Block Constraints:** Read-only queries intended for the standby node should generally not be wrapped inside complex, multi-statement transaction blocks that expect write-forwarding or immediate visibility.

Only specific application workloads that can tolerate eventual consistency, query cancellations, and replication lag should opt-in for read-only connections routed to the standby node.

#### The Shift Away From Floating Virtual IPs (VIPs)

Historically, many organizations have used floating Virtual IP (VIP) addresses to mitigate the risk of a single point of failure when applications connect to a proxy layer. In this architecture, multiple load balancer instances share a single public or private IP address that dynamically "floats" from a failed instance to a healthy, active one. To orchestrate this transition and monitor instance health, a dedicated failover clustering solution (such as Keepalived or Corosync) must be deployed alongside the load balancers.

**Important Operational Guidance:** While a floating VIP sounds seamless in theory, real-world production data shows that VIP deployments frequently introduce complex failure modes, split-brain scenarios, and an overall increase in high-severity incidents. Based on feedback from enterprise environments, the use of floating VIPs is highly discouraged. As already stated, reducing the chance of failure is an important objective of investment in High Availability infrastructure. Therefore, this frequent point of failure is discouraged.

The use of an external load balancer is optional. If your application implements the logic of connection routing and load-balancing, it is a highly-recommended approach.

#### Step 4. Backups 

Even with replication and failover mechanisms in place, it’s crucial to have regular backups of your data. Backups provide a safety net for catastrophic failures that affect both the primary and replica nodes. While replication ensures data is synchronized across multiple nodes, it does not protect against data corruption, accidental deletions, or malicious attacks that can affect all nodes.

![Backup tool](../_images/diagrams/ha-overview-backup.svg)

Having regular backups ensures that you can restore your data to a previous state, preserving data integrity and availability even in the worst-case scenarios. Store your backups in separate, secure locations and regularly test them to ensure that you can quickly and accurately restore them when needed. This additional layer of protection is essential to maintaining continuous operation and minimizing data loss. 

The backup tool is optional but highly-recommended for data corruption recovery. Additionally, backups protect against human error, when a user can accidentally drop a table or make another mistake.

As a result, you end up with the following components for a minimalistic highly-available deployment:

* A minimum two-node PostgreSQL cluster with the replication configured among nodes. The recommended minimalistic cluster is a three-node one.
* A solution to manage the cluster and perform automatic failover when the primary node is down.
* (Optional but recommended) A load-balancing proxy that provides a single point of entry to your cluster and distributes the load across cluster nodes. You need at least two instances of a load-balancing proxy and a failover tool to eliminate a single point of failure.
* (Optional but recommended) A backup and restore solution to protect data against loss, corruption and human error.

Optionally, you can add a monitoring tool to observe the health of your deployment, receive alerts about performance issues and timely react to them.

### What tools to use?

The PostgreSQL ecosystem offers many tools for high availability, but choosing the right ones can be challenging. At Percona, we have carefully selected and tested open-source tools to ensure they work well together and help you achieve high availability. 

In our [reference architecture](ha-architecture.md) section we recommend a combination of open-source components and frameworks, focusing on a minimalistic PostgreSQL cluster.

Note that all the components are recommended but not mandatory. You can use your own solutions and alternatives if they better meet your business needs. However, deviating from proven methods and architecture may increase the risk.

### Additional reading

[Measuring high availability](ha-measure.md){.md-button}

## Next steps

[Architecture :material-arrow-right:](ha-architecture.md){.md-button}


