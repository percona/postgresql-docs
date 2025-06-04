# Configure HAProxy

HAproxy is the load balancer and the single point of entry to your PostgreSQL cluster for client applications. A client application accesses the HAPoxy URL and sends its read/write requests there. Behind-the-scene, HAProxy routes write requests to the primary node and read requests - to the secondaries in a round-robin fashion so that no secondary instance is unnecessarily loaded. To make this happen, provide different ports in the HAProxy configuration file. In this deployment, writes are routed to port 5000 and reads  - to port 5001.

This way, a client application doesn't know what node in the underlying cluster is the current primary. HAProxy sends connections to a healthy node (as long as there is at least one healthy node available) and ensures that client application requests are never rejected. 

To eliminate a single point of failure for HAProxy, you need the failover tool for it. 

For this document we focus on deployment on premises and we use `keepalived`. It monitors HAProxy state and manages the virtual IP for HAProxy.

If you use a cloud infrastructure, it may be easier to use the load balancer provided by the cloud provider to achieve high-availability with HAProxy. 

## HAProxy setup

1. Install HAProxy on the HAProxy nodes: `HAProxy1`, `HAProxy2` and `HAProxy3`:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-haproxy
    ```

2. The HAProxy configuration file path is: `/etc/haproxy/haproxy.cfg`. Specify the following configuration in this file for every node.

    ```
    global
        maxconn 100                # Maximum number of concurrent connections

    defaults
        log global                 # Use global logging configuration
        mode tcp                   # TCP mode for PostgreSQL connections
        retries 2                  # Number of retries before marking a server as failed
        timeout client 30m         # Maximum time to wait for client data
        timeout connect 4s         # Maximum time to establish connection to server
        timeout server 30m         # Maximum time to wait for server response
        timeout check 5s           # Maximum time to wait for health check response

    listen stats                # Statistics monitoring 
        mode http              # The protocol for web-based stats UI
        bind *:7000            # Port to listen to on all network interfaces
        stats enable           # Statistics reporting interface
        stats uri /stats       # URL path for the stats page
        stats auth percona:myS3cr3tpass    # Username:password authentication

    listen primary
        bind *:5000                        # Port for write connections
        option httpchk /primary 
        http-check expect status 200  
        default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions  # Server health check parameters
        server node1 node1:5432 maxconn 100 check port 8008 
        server node2 node2:5432 maxconn 100 check port 8008  
        server node3 node3:5432 maxconn 100 check port 8008 

    listen standbys
        balance roundrobin     # Round-robin load balancing for read connections
        bind *:5001            # Port for read connections
        option httpchk /replica 
        http-check expect status 200  
        default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions  # Server health check parameters
        server node1 node1:5432 maxconn 100 check port 8008  
        server node2 node2:5432 maxconn 100 check port 8008  
        server node3 node3:5432 maxconn 100 check port 8008  
    ```

    HAProxy will use the REST APIs hosted by Patroni to check the health status of each PostgreSQL node and route the requests appropriately. 

    To monitor HAProxy stats, create the user who has the access to it. Read more about statistics dashboard in [HAProxy documentation :octicons-link-external-16:](https://www.haproxy.com/documentation/haproxy-configuration-tutorials/alerts-and-monitoring/statistics/)

3. Restart HAProxy:
    
    ```{.bash data-prompt="$"}
    $ sudo systemctl restart haproxy
    ```

4. Check the HAProxy logs to see if there are any errors:
   
    ```{.bash data-prompt="$"}
    $ sudo journalctl -u haproxy.service -n 100 -f
    ```

## Keepalived setup

The HAproxy instances will share a virtual IP address `203.0.113.1` as the single point of entry for client applications.

In this setup we define the basic health check for HAProxy. You may want to use a more sophisticated check. You can do this by writing a script and referencing it in the `keeplaived` configuration. See the [Example of HAProxy health check](#example-of-haproxy-health-check) section for details.

1. Install `keepalived` on all HAProxy nodes:

    === ":material-debian: On Debian and Ubuntu"

        ```{.bash data-prompt="$"}
        $ sudo apt install keepalived
        ```

    === ":material-redhat: On RHEL and derivatives"

        ```{.bash data-prompt="$"}
        $ sudo yum install keepalived
        ```

2. Create the `keepalived` configuration file at `/etc/keepalived/keepalived.conf` with the following contents for each node:

    === "Primary HAProxy (HAProxy1)"

        ```ini
        vrrp_script chk_haproxy {
            script "killall -0 haproxy"    # Basic check if HAProxy process is running
            interval 3                      # Check every 2 seconds
            fall 3                          # The number of failures to mark the node as down
            rise 2                          # The number of successes to mark the node as up
            weight -11                        # Reduce priority by 2 on failure
        }

        vrrp_instance CLUSTER_1 {           # The name of Patroni cluster
            state MASTER                    # Initial state for the primary node
            interface eth1                  # Network interface to bind to
            virtual_router_id 99            # Unique ID for this VRRP instance
            priority 110                   # The priority for the primary must be the highest
            advert_int 1                   # Advertisement interval
            authentication {
                auth_type PASS
                auth_pass myS3cr3tpass     # Authentication password
            }
            virtual_ipaddress {
                203.0.113.1/24            # The virtual IP address
            }
            track_script {
                chk_haproxy
            }
        }
        ```

    === "HAProxy2"

        ```ini
        vrrp_script chk_haproxy {
            script "killall -0 haproxy"    # Basic check if HAProxy process is running
            interval 2                      # Check every 2 seconds
            fall 2                          # The number of failures to mark the node as down
            rise 2                          # The number of successes to mark the node as up
            weight 2                        # Reduce priority by 2 on failure
        }

        vrrp_instance CLUSTER_1 {
            state BACKUP                    # Initial state for backup node
            interface eth1                  # Network interface to bind to
            virtual_router_id 99           # Same ID as primary
            priority 100                   # Lower priority than primary
            advert_int 1                   # Advertisement interval
            authentication {
                auth_type PASS
                auth_pass myS3cr3tpass     # Same password as primary
            }
            virtual_ipaddress {
                203.0.113.1/24 
            }
            track_script {
                chk_haproxy
            }
        }
        ```

    === "HAProxy3"

        ```ini
        vrrp_script chk_haproxy {
            script "killall -0 haproxy"    # Basic check if HAProxy process is running
            interval 2                      # Check every 2 seconds
            fall 3                          # The number of failures to mark the node as down
            rise 2                          # The number of successes to mark the node as up
            weight 6                        # Reduce priority by 2 on failure
        }

        vrrp_instance CLUSTER_1 {
            state BACKUP                    # Initial state for backup node
            interface eth1                  # Network interface to bind to
            virtual_router_id 99           # Same ID as primary
            priority 105                    # Lowest priority
            advert_int 1                   # Advertisement interval
            authentication {
                auth_type PASS
                auth_pass myS3cr3tpass     # Same password as primary
            }
            virtual_ipaddress {
                203.0.113.1/24 
            }
            track_script {
                chk_haproxy
            }
        }
        ```

3. Start `keepalived`:
 
    ```{.bash data-prompt="$"}
    $ sudo systemctl start keepalived
    ```

4. Check the `keepalived` status:
 
    ```{.bash data-prompt="$"}
    $ sudo systemctl status keepalived
    ```

!!! note

    The basic health check (`killall -0 haproxy`) only verifies that the HAProxy process is running. For production environments, consider implementing more comprehensive health checks that verify the node's overall responsiveness and HAProxy's ability to handle connections.

### Example of HAProxy health check

Sometimes checking only the running haproxy process is not enough. The process may be running while HAProxy is in a degraded state. A good practice is to make additional checks to ensure HAProxy is healthy.

Here's an example health check script for HAProxy. It performs the following checks:

1. Verifies that the HAProxy process is running
2. Tests if the HAProxy admin socket is accessible
3. Confirms that HAProxy is binding to the default port `5432`

```bash
#!/bin/bash

# Exit codes:
# 0 - HAProxy is healthy
# 1 - HAProxy is not healthy

# Check if HAProxy process is running
if ! pgrep -x haproxy > /dev/null; then
    echo "HAProxy process is not running"
    exit 1
fi

# Check if HAProxy socket is accessible
if ! socat - UNIX-CONNECT:/var/run/haproxy/admin.sock > /dev/null 2>&1; then
    echo "HAProxy socket is not accessible"
    exit 1
fi

# Check if HAProxy is binding to port 5432
if ! netstat -tuln | grep -q ":5432 "; then
    exit 1
fi

# All checks passed
exit 0
```

Save this script as `/usr/local/bin/check_haproxy.sh` and make it executable:

```{.bash data-prompt="$"}
$ sudo chmod +x /usr/local/bin/check_haproxy.sh
```

Then define this script in Keepalived configuration on each node:

```ini
vrrp_script chk_haproxy {
    script "/usr/local/bin/check_haproxy.sh"
    interval 2
    fall 3
    rise 2
    weight -10
}
```


Congratulations! You have successfully configured your HAProxy solution.  Now you can proceed to testing it.

## Next steps

[Test Patroni PostgreSQL cluster](ha-test.md){.md-button}