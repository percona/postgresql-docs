# Configure HAProxy

HAproxy is the load balancer and the single point of entry to your PostgreSQL cluster for client applications. A client application accesses the HAPpoxy URL and sends its read/write requests there. Behind-the-scene, HAProxy routes write requests to the primary node and read requests - to the secondaries in a round-robin fashion so that no secondary instance is unnecessarily loaded. To make this happen, provide different ports in the HAProxy configuration file. In this deployment, writes are routed to port 5000 and reads  - to port 5001.

This way, a client application doesn't know what node in the underlying cluster is the current primary. HAProxy sends connections to a healthy node (as long as there is at least one healthy node available) and ensures that client application requests are never rejected. 

To eliminate a single point of failure for HAProxy, we use `keepalived` - the failover tool for it. 

## HAProxy setup

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

## Keepalived setup

1. Install `keepalived` on all HAProxy nodes:

    === ":material-debian: On Debian and Ubuntu"

        ```{.bash data-prompt="$"}
        $ sudo apt install keepalived
        ```

    === "material-redhat "On RHEL and derivatives"

        ```{.bash data-prompt="$"}
        $ sudo dnf install keepalived
        ```

3. Use the script to check the state of the primary node. This script makes an HTTP request to the primary Patroni node, checks if the response status code is `200`, and exits with a success code (0) if it is. If the status code is anything other than 200, it exits with a failure code (1).  Create the `chk_primary.sh` file and specify the following within:

    ```bash title="chk_primary.sh"
    #!/bin/bash

    RET=`/usr/bin/curl -s -o /dev/null -w "%{http_code}" http://localhost:8008/primary`

    if [[ $RET -eq "200" ]]
    then
       exit 0
    fi

    exit 1
    ```

4. Make the script executable:

    ```{.bash data-prompt="$"}
    $ sudo chmod +x /path/to/chk_primary.sh
    ```

4. The path to the `keepalived` configuration file is `/etc/keepalived/keepalived.conf`. Configure a primary and a secondary HAProxy nodes separately. 

    Edit the `/etc/keepalived/keepalived.conf` configuration file. Specify the following information:

    * `vrrp_instance string` - the name of Patroni cluster, `CLUSTER_1` in our case.
    * `interface` - The interface where Patroni nodes reside
    * `unicast_src_ip` - The IP address of the HAProxy node you currently configure. 
    * `unicast_peer` - The IP address of the remaining HAProxy nodes 
    * `virtual_ipaddress` - A public IP address of HAProxy, its subnet and the interface where it resides


    * `vrrp_script chk_patroni` - The path to the `chk_primary.sh` script

    === "Primary HAProxy"

        ```ini
        global_defs {
            process_names
        
            enable_script_security  # Check that the script can only be edited by root
        
            script_user root        # Systemctl does only work with root

            vrrp_version 3          # Using the latest protocol version allows for dynamic_interfaces

            # vrrp_min_garp true      # After switching to MASTER state 5 gratuitous arp (garp) are send and
                                    # after 5 seconds another 5 garp are send. (For the switches to update the arp table)
                                    # This option disables the second time "5 garp are send (as this is not necessary with modern switches)
        }

        vrrp_script chk_patroni {
            script "/usr/local/bin/chk_primary.sh"

            # script "/usr/bin/killall -0 haproxy"     # Sending the zero signal returns OK (0) if the process or process group ID exists, 
                                            # otherwise, it returns ERR (-1 and sets errno to ESRCH). 
                                            # Note that the kill(2) man page states that error checking is still performed, 
                                            # meaning it will return na error (-1) and set errno to EPERM if: 
                                            #   - The target process doesn't exists 
                                            #   - The target process exists but the sending process does not have enough permissions to send it a signal
        
            # script "/usr/bin/systemctl is-active --quiet haproxy"   # The more intelligent way of checking the haproxy process
                                            # Simpler way of checking haproxy process:
                                            # script "/usr/bin/killall -0 haproxy"
        
            fall 2                          # 2 fails required for 'ilure
        
            rise 2                          # 2 OKs required to consider the process up after failure
        
            interval 1                      # check every X seconds

            weight -10                      # add 10 points rc=0
        }

        vrrp_instance CLUSTER_1 {
            state MASTER            # Initial state, MASTER|BACKUP
                                    # MASTER on haproxy1, BACKUP on haproxy2, BACKUP on haproxy3, etc
                                    # NOTE that if the priority is 255, then the instance will transition immediately
                                    # to MASTER if state MASTER is specified; otherwise the instance will
                                    # wait between 3 and 4 advert intervals before it can transition,
                                    # depending on the priority

            interface eth1        # interface for inside_network, bound by vrrp.
                                    # Note: if using unicasting, the interface can be omitted as long
                                    #   as the unicast addresses are not IPv6 link local addresses (this is
                                    #   necessary, for example, if using asymmetric routing).
                                    #   If the interface is omitted, then all VIPs and eVIPs should specify
                                    #   the interface they are to be configured on, otherwise they will be
                                    #   added to the default interface.

            virtual_router_id 99    # Needs to be the same value in all nodes of the same cluster
                                    # HOWEVER, each cluster needs to have an UNIQUE ID
        
            priority 95             # The higher the priority the higher the chance to be promoted to MASTER
            advert_int 1            # Specify the VRRP Advert interval in seconds

            # authentication {        # Non compliant but good to have with unicast
            #     auth_type PASS
            #     auth_pass passw123
            # }

            unicast_src_ip 10.104.0.6  # The default IP for binding vrrpd is the primary IP
                                            # on the defined interface. If you want to hide the location of vrrpd,
                                            # use this IP as src_addr for multicast or unicast vrrp packets.

            unicast_peer {                  # Do not send VRRP adverts over a VRRP multicast group.
                                            # Instead it sends adverts to the following list of
                                            # ip addresses using unicast. It can be cool to use
                                            # the VRRP FSM and features in a networking
                                            # environment where multicast is not supported!
                                            # IP addresses specified can be IPv4 as well as IPv6.
                                            # If min_ttl and/or max_ttl are specified, the TTL/hop limit
                                            # of any received packet is checked against the specified
                                            # TTL range, and is discarded if it is outside the range.
                                            # Specifying min_ttl or max_ttl turns on check_unicast_src.
                10.104.0.5
            }

            unicast_fault_no_peer           # It is not possible to operate in unicast mode without any peers.
                                            # Until v2.2.4 keepalived would silently operate in multicast mode
                                            # if no peers were specified but a unicast keyword had been specified.
                                            # Using this keywork stops defaulting to multicast if no peers are
                                            # specified and puts the VRRP instance into fault state.

            virtual_ipaddress {
                134.209.111.138/24 brd + dev eth1 label eth1:0
            }

            track_script {          # Check that haproxy is up
                chk_patroni
            }
        }
        ```
        
    === "Secondary HAProxy"

        ```ini
        global_defs {
            process_names

            enable_script_security  # Check that the script can only be edited by root

            script_user root        # Systemctl does only work with root

            vrrp_version 3          # Using the latest protocol version allows for dynamic_interfaces

            # vrrp_min_garp true      # After switching to MASTER state 5 gratuitous arp (garp) are send and
                                    # after 5 seconds another 5 garp are send. (For the switches to update the arp table)
                                    # This option disables the second time "5 garp are send (as this is not necessary with modern switches)
        }

        vrrp_script chk_patroni {
            script "/usr/local/bin/chk_primary.sh"

            # script "/usr/bin/killall -0 haproxy"     # Sending the zero signal returns OK (0) if the process or process group ID exists, 
                                            # otherwise, it returns ERR (-1 and sets errno to ESRCH). 
                                            # Note that the kill(2) man page states that error checking is still performed, 
                                            # meaning it will return na error (-1) and set errno to EPERM if: 
                                            #   - The target process doesn't exists 
                                            #   - The target process exists but the sending process does not have enough permissions to send it a signal

            # script "/usr/bin/systemctl is-active --quiet haproxy"   # The more intelligent way of checking the haproxy process
                                            # Simpler way of checking haproxy process:
                                            # script "/usr/bin/killall -0 haproxy"

            fall 2                          # 2 fails required for 'ilure

            rise 2                          # 2 OKs required to consider the process up after failure

            interval 1                      # check every X seconds

            weight -10                      # add 10 points rc=0
        }

        vrrp_instance CLUSTER_1 {
            state BACKUP            # Initial state, MASTER|BACKUP
                                    # MASTER on haproxy1, BACKUP on haproxy2, BACKUP on haproxy3, etc
                                    # NOTE that if the priority is 255, then the instance will transition immediately
                                    # to MASTER if state MASTER is specified; otherwise the instance will
                                    # wait between 3 and 4 advert intervals before it can transition,
                                    # depending on the priority

            interface eth1        # interface for inside_network, bound by vrrp.
                                    # Note: if using unicasting, the interface can be omitted as long
                                    #   as the unicast addresses are not IPv6 link local addresses (this is
                                    #   necessary, for example, if using asymmetric routing).
                                    #   If the interface is omitted, then all VIPs and eVIPs should specify
                                    #   the interface they are to be configured on, otherwise they will be
                                    #   added to the default interface.

            virtual_router_id 99    # Needs to be the same value in all nodes of the same cluster
                                    # HOWEVER, each cluster needs to have an UNIQUE ID

            priority 95             # The higher the priority the higher the chance to be promoted to MASTER
            advert_int 1            # Specify the VRRP Advert interval in seconds

            # authentication {        # Non compliant but good to have with unicast
            #     auth_type PASS
            #     auth_pass passw123
            # }

            unicast_src_ip 10.104.0.5       # The default IP for binding vrrpd is the primary IP
                                            # on the defined interface. If you want to hide the location of vrrpd,
                                            # use this IP as src_addr for multicast or unicast vrrp packets.

            unicast_peer {                  # Do not send VRRP adverts over a VRRP multicast group.
                                            # Instead it sends adverts to the following list of
                                            # ip addresses using unicast. It can be cool to use
                                            # the VRRP FSM and features in a networking
                                            # environment where multicast is not supported!
                                            # IP addresses specified can be IPv4 as well as IPv6.
                                            # If min_ttl and/or max_ttl are specified, the TTL/hop limit
                                            # of any received packet is checked against the specified
                                            # TTL range, and is discarded if it is outside the range.
                                            # Specifying min_ttl or max_ttl turns on check_unicast_src.
                10.104.0.6
            }

            unicast_fault_no_peer           # It is not possible to operate in unicast mode without any peers.
                                            # Until v2.2.4 keepalived would silently operate in multicast mode
                                            # if no peers were specified but a unicast keyword had been specified.
                                            # Using this keywork stops defaulting to multicast if no peers are
                                            # specified and puts the VRRP instance into fault state.

            virtual_ipaddress {
                134.209.111.138/24 brd + dev eth1 label eth1:0
            }

            track_script {          # Check that haproxy is up
                chk_patroni
            }
        }
        ```

5. Start `keepalived`:
 
    ```{.bash data-prompt="$"}
    $ sudo systemctl start keepalived
    ```

6. Check the `keepalived` status:
 
    ```{.bash data-prompt="$"}
    $ sudo systemctl status keepalived
    ```

Congratulations! You have successfully configured your HAProxy solution.  Now you can proceed to testing it.

## Next steps

[Test Patroni PostgreSQL cluster](ha-test.md){.md-button}