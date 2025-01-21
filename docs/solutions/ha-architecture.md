# Architecture 

As we discussed in the [overview of high availability](high-availability.md), the minimalist approach to a highly-available deployment is to have a three-node PostgreSQL cluster with the cluster management and failover mechanisms, load balancer and a backup / restore solution.

The following diagram shows this architecture with the tools we recommend to use. 

![Architecture of the three-node, single primary PostgreSQL cluster](../_images/diagrams/ha-architecture-patroni.png)

## Components

The components in this architecture are:

- PostgreSQL nodes bearing the user data. 

- Patroni - an automatic failover system. Patroni requires and uses the Distributed Configuration Store to store the cluster configuration, health and status.

- etcd - a Distributed Configuration Store.  It not only stores the state of the PostgreSQL cluster but also handles the election of a new primary. 

- HAProxy - the load balancer and the single point of entry to the cluster for client applications. 

- keepalived - a failover solution for HAProxy

- pgBackRest - the backup and restore solution for PostgreSQL

- Percona Monitoring and Management (PMM) - the solution to monitor the health of your cluster 

## Additional reading

[How components work together](ha-components.md){.md-button}

## Next steps 

[Deployment - initial setup](ha-init-setup.md){.md-button}