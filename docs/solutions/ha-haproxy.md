# Configure HAProxy

HAproxy is the load balancer and the single point of entry to your PostgreSQL cluster for client applications. A client application accesses the HAPpoxy URL and sends its read/write requests there. Behind-the-scene, HAProxy routes write requests to the primary node and read requests - to the secondaries in a round-robin fashion so that no secondary instance is unnecessarily loaded. To make this happen, provide different ports in the HAProxy configuration file. In this deployment, writes are routed to port 5000 and reads  - to port 5001

This way, a client application doesn’t know what node in the underlying cluster is the current primary. HAProxy sends connections to a healthy node (as long as there is at least one healthy node available) and ensures that client application requests are never rejected. 

1. Install HAProxy on the `HAProxy-demo` node:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-haproxy
    ```

2. The HAProxy configuration file path is: `/etc/haproxy/haproxy.cfg`. Specify the following configuration in this file.

    ```
    global
        maxconn 100

    defaults
        log global
        mode tcp
        retries 2
        timeout client 30m
        timeout connect 4s
        timeout server 30m
        timeout check 5s

    listen stats
        mode http
        bind *:7000
        stats enable
        stats uri /

    listen primary
        bind *:5000
        option httpchk /primary 
        http-check expect status 200
        default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
        server node1 node1:5432 maxconn 100 check port 8008
        server node2 node2:5432 maxconn 100 check port 8008
        server node3 node3:5432 maxconn 100 check port 8008

    listen standbys
        balance roundrobin
        bind *:5001
        option httpchk /replica 
        http-check expect status 200
        default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
        server node1 node1:5432 maxconn 100 check port 8008
        server node2 node2:5432 maxconn 100 check port 8008
        server node3 node3:5432 maxconn 100 check port 8008
    ```


    HAProxy will use the REST APIs hosted by Patroni to check the health status of each PostgreSQL node and route the requests appropriately. 

3. Restart HAProxy:
    
    ```{.bash data-prompt="$"}
    $ sudo systemctl restart haproxy
    ```

4. Check the HAProxy logs to see if there are any errors:
   
    ```{.bash data-prompt="$"}
    $ sudo journalctl -u haproxy.service -n 100 -f
    ```