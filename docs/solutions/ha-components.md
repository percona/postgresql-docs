# How components work together

This document explains how components of the proposed [high-availability architecture](ha-architecture.md) work together.

Each PostgreSQL instance in the cluster maintains consistency with other members through streaming replication. We use the default asynchronous streaming replication during which the primary doesn't wait for the secondaries to acknowledge the receipt of the data to consider the transaction complete. 

Each PostgreSQL instance also hosts Patroni and etcd. Patroni and etcd are responsible for creating and managing the cluster, monitoring the cluster health and handling failover in the case of the outage. 

<add a disclaimer about having a dedicated etcd cluster and why>

Patroni periodically sends heartbeat requests with the cluster status to etcd. etcd writes this information to disk and sends the response back to Patroni. If the current primary fails to renew its status as leader within the specified timeout, Patroni updates the state change in etcd, which uses this information to elect the new primary and keep the cluster up and running.

The connections to the cluster do not happen directly to the database nodes but are routed via a connection proxy like HAProxy. This proxy determines the active node by querying the Patroni REST API.
