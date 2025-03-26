# High Availability in PostgreSQL with Patroni

Whether you are a small startup or a big enterprise, downtime of your services may cause severe consequences, such as loss of customers, impact on your reputation, and penalties for not meeting the Service Level Agreements (SLAs). That’s why ensuring a highly-available deployment is crucial.

But what does it mean, high availability? And how to achieve it? This document answers these questions. 

After reading this document, you will learn the following:

* [what is high availability](#what-is-high-availability)
* the recommended [reference architecture](ha-architecture.md) to achieve it
* how to deploy it using our step-by-step deployment guides for each component. The deployment instructions focus on the minimalistic approach to high availability that we recommend. It also gives instructions how to deploy additional components that you can add when your infrastructure grows.
* how to verify that your high availability deployment works as expected, providing replication and failover with the [testing guidelines](ha-test.md)

## What is high availability

High availability is the ability of the system to operate continuously without the interruption of services. During the outage, the system must be able to transfer the services from the database node that is down to one of the remaining nodes. 

### How to achieve it? 

A short answer is: add redundancy to your deployment, eliminate a single point of failure (SPOF) and have the mechanism to transfer the services from a failed member to the healthy one. 

For a long answer, let's break it down into steps. 

#### Step 1. Replication

First, you should have more than one copy of your data. This means, you need to have several instances of your database where one is the primary instance that accepts reads and writes. Other instances are replicas – they must have an up-to-date copy of the data from the primary and remain in sync with it. They may also accept reads to offload your primary. 

You typically deploy these instances on separate servers or nodes. The minimum number of database nodes is two: one primary and one replica. 

The recommended deployment is a three-instance cluster consisting of one primary and two replica nodes. The replicas receive the data via the replication mechanism. 

![Primary-replica setup](../_images/diagrams/ha-overview-replication.svg)

PostgreSQL natively supports logical and streaming replication. For high availability we recommend streaming replication as it happens in real time, minimizing the delay between the primary and replica nodes.

#### Step 2. Failover

Next, you may have a situation when a primary node is down or not responding. Reasons for that can be different – from hardware or network issues to software failures, power outages, and scheduled maintenance. In this case, you must have the way to know about it and to transfer the operation from the primary node to one of the secondaries. This process is called failover.  

![Failover](../_images/diagrams/ha-overview-failover.svg)

You can do a manual failover. It suits for environments where downtime does not impact operations or revenue. However, this requires dedicated personnel and may lead to additional downtime. 

Another option is automated failover, which significantly minimizes downtime and is less error-prone than manual one. Automated failover can be accomplished by adding an open-source failover tool to your deployment.

#### Step 3. Load balancer

Instead of a single node you now have a cluster. How to enable users to connect to the cluster and ensure they always connect to the correct node, especially when the primary node changes? 

One option is to configure a DNS resolution that resolves the IPs of all cluster nodes. A drawback here is that only the primary node accepts all requests. When your system grows, so does the load and it may lead to overloading the primary node and result in performance degradation. 

You can write your application to send read/write requests to the primary and read-only requests to the secondary nodes. This requires significant programming experience.

![Load-balancer](../_images/diagrams/ha-overview-load-balancer.svg)

Another option is to use a load-balancing proxy. Instead of connecting directly to the IP address of the primary node, which can change during a failover, you use a proxy that acts as a single point of entry for the entire cluster. This proxy provides the IP address visible for user applications. It also knows which node is currently the primary and directs all incoming write requests to it. At the same time, it can distribute read requests among the replicas to evenly spread the load and improve performance.

To eliminate a single point of failure for a load balancer, deploy minimum two instances of it for redundancy. The instances share the public IP address so that it can "float" from one instance to another in the case of a failure. To control the load balancer's state and transfer the IP address to the active instance, you also need the failover solution for load balancers.

The use of a load balancer is optional, if your application implements this logic, but is highly-recommended. 

#### Step 4. Backups 

Even with replication and failover mechanisms in place, it’s crucial to have regular backups of your data. Backups provide a safety net for catastrophic failures that affect both the primary and replica nodes. While replication ensures data is synchronized across multiple nodes, it does not protect against data corruption, accidental deletions, or malicious attacks that can affect all nodes.

![Backup tool](../_images/diagrams/ha-overview-backup.svg)

Having regular backups ensures that you can restore your data to a previous state, preserving data integrity and availability even in the worst-case scenarios. Store your backups in separate, secure locations and regularly test them to ensure that you can quickly and accurately restore them when needed. This additional layer of protection is essential to maintaining continuous operation and minimizing data loss. 

The backup tool is optional but highly-recommended for data corruption recovery.

As a result, you end up with the following components for a minimalistic highly-available deployment:

* A minimum two-node PostgreSQL cluster with the replication configured among nodes. The recommended minimalistic cluster is a three-node one.
* A solution to manage the cluster and perform automatic failover when the primary node is down.
* (Optional but recommended) A load-balancing proxy that provides a single point of entry to your cluster and distributes the load across cluster nodes. You need at least two instances of a load-balancing proxy and a failover tool to eliminate a single point of failure.
* (Optional but recommended) A backup and restore solution to protect data against loss and corruption.

Optionally, you can add a monitoring tool to observe the health of your deployment, receive alerts about performance issues and timely react to them.

### What tools to use?

The PostgreSQL ecosystem offers many tools for high availability, but choosing the right ones can be challenging. At Percona, we have carefully selected and tested open-source tools to ensure they work well together and help you achieve high availability. 

In our [reference architecture](ha-architecture.md) section we recommend a combination of open-source tools, focusing on a minimalistic three-node PostgreSQL cluster.

Note that the tools are recommended but not mandatory. You can use your own solutions and alternatives if they better meet your business needs. However, in this case, we cannot guarantee their compatibility and smooth operation.

### Additional reading

[Measuring high availability](ha-measure.md){.md-button}

## Next steps

[Architecture](ha-architecture.md){.md-button}


