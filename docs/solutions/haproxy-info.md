# HAProxy

HAProxy (High Availability Proxy) is a powerful, open-source load balancer and
proxy server used to improve the performance and reliability of web services by
distributing network traffic across multiple servers. It is widely used to enhance the scalability, availability, and reliability of web applications by balancing client requests among backend servers.

HAProxy architecture is
optimized to move data as fast as possible with the least possible operations.
It focuses on optimizing the CPU cache's efficiency by sticking connections to
the same CPU as long as possible.

## How HAProxy works

HAProxy operates as a reverse proxy, which means it accepts client requests and distributes them to one or more backend servers using the configured load-balancing algorithm. This ensures efficient use of server resources and prevents any single server from becoming overloaded.

- **Client request processing**:

    1. A client application connects to HAProxy instead of directly to the server.
    2. HAProxy analyzes the requests and determines what server to route it to for further processing.
    3. HAProxy forwards the request to the selected server using the routing algorithm defined in its configuration. It can be round robin, least connections, and others.
    4. HAProxy receives the response from the server and forwards it back to the client.
    5. After sending the response, HAProxy either closes the connection or keeps it open, depending on the configuration.

- **Load balancing**: HAProxy distributes incoming traffic using various algorithms such as round-robin, least connections, and IP hash.
- **Health checks**: HAProxy continuously monitors the health of backend servers to ensure requests are only routed to healthy servers.
- **SSL termination**: HAProxy offloads SSL/TLS encryption and decryption, reducing the workload on backend servers.
- **Session persistence**: HAProxy ensures that requests from the same client are routed to the same server for session consistency.
- **Traffic management**: HAProxy supports rate limiting, request queuing, and connection pooling for optimal resource utilization.
- **Security**: HAProxy supports SSL/TLS, IP filtering, and integration with Web Application Firewalls (WAF).

## Role in a HA Patroni cluster

HAProxy plays a crucial role in managing PostgreSQL high availability in a Patroni cluster. Patroni is an open-source tool that automates PostgreSQL cluster management, including failover and replication. HAProxy acts as a load balancer and proxy, distributing client connections across the cluster nodes. 

Client applications connect to HAProxy, which transparently forwards their requests to the appropriate PostgreSQL node. This ensures that clients always connect to the active primary node without needing to know the cluster's internal state and topology.

HAProxy monitors the health of PostgreSQL nodes using Patroni's API and routes traffic to the primary node. If the primary node fails, Patroni promotes a secondary node to a new primary, and HAProxy updates its routing to reflect the change. You can configure HAProxy to route write requests to the primary node and read requests - to the secondary nodes.

## Redundancy for HAProxy

Using a single HAProxy node in your deployment opens a risk for single point of failure: when HAProxy is down, clinents lose connection to the cluster. To eliminate this risk, add redundancy to HAProxy. To achieve this, you can set up multiple HAProxy instances with a failover mechanism. This ensures that if one HAProxy instance fails, another takes over, maintaining high availability.

To make this happen, you need the following:

1. Configure a virtual IP address that can be moved between HAProxy instances.

2. Install and configure Keepalived - a failover mechanism for HAProxy. Keepalived monitors the health of HAProxy instances.
If the primary HAProxy instance fails, Keepalived moves the virtual IP address to a backup instance. 

3. Ensure that HAProxy configurations are synchronized across all instances to maintain consistency.

