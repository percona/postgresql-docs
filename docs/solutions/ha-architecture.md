# Architecture 

As we discussed in the [overview of high availability](high-availability.md), the minimalist approach to a highly-available deployment is to have a three-node PostgreSQL cluster with the cluster management and failover mechanisms, load balancer and a backup / restore solution.

The following diagram shows this architecture with the tools we recommend to use. 

![Architecture of the three-node, single primary PostgreSQL cluster](../_images/diagrams/HA-PG-basic-no pgBadger.png#only-light)
![Architecture of the three-node, single primary PostgreSQL cluster](../_images/diagrams/HA-PG-basic-no pgBadger-dark.png#only-dark)

## Components

The components in this architecture are:

- PostgreSQL nodes bearing the user data. 

- etcd - a Distributed Configuration Store.  It stores the state of the PostgreSQL cluster and handles the election of a new primary. 

- Patroni - an automatic failover system. Patroni requires and uses the Distributed Configuration Store to store the cluster configuration, health and status.

- HAProxy - the load balancer and the single point of entry to the cluster for client applications. 

- keepalived - a high-availability and failover solution for HAProxy. It provides a virtual IP (VIP) address for HAProxy and prevents its single point of failure by failing over the services to the operational instance

- pgBackRest - the backup and restore solution for PostgreSQL

- Percona Monitoring and Management (PMM) - the solution to monitor the health of your cluster 

- (Optional) pgbouncer - a connection pooler for PostgreSQL. The aim of pgbouncer is to lower the performance impact of opening new connections to PostgreSQL.

## Additional reading

[How components work together](ha-components.md){.md-button}

## Next steps 

[Deployment - initial setup](ha-init-setup.md){.md-button}