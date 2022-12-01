# Testing the Patroni PostgreSQL Cluster

This document covers the following scenarios to test the PostgreSQL cluster:

* replication, 
* connectivity, 
* failover, and 
* manual switchover.

### Testing replication 

1. Connect to the cluster and establish the `psql` session from a client machine that can connect to the HAProxy node. Use the HAProxy-demo node's public IP address:

    ```{.bash data-promp="$"}
    $ psql -U postgres -h 134.209.111.138 -p 5000
    ```

2. Run the following commands to create a table and insert a few rows:

    ```sql
    CREATE TABLE customer(name text,age integer);
    INSERT INTO CUSTOMER VALUES('john',30);
    INSERT INTO CUSTOMER VALUES('dawson',35);
    ```

3. To ensure that the replication is working, we can log in to each PostgreSQL node and run a simple SQL statement against the locally running instance:

    ```{.bash data-promp="$"}
    $ sudo psql -U postgres -c "SELECT * FROM CUSTOMER;"
    ```
    
    The results on each node should be the following:

    ```
      name  | age
    --------+-----
     john   |  30
     dawson |  35
    (2 rows)
    ```

### Testing failover

In a proper setup, client applications won't have issues connecting to the cluster, even if one or even two of the nodes go down. We will test the cluster for failover in the following scenarios:

#### Scenario 1. Intentionally stop the PostgreSQL on the primary node and verify access to PostgreSQL.

1. Run the following command on any node to check the current cluster status:

    ```{.bash data-promp="$"}
    $ sudo patronictl -c /etc/patroni/patroni.yml list

    + Cluster: stampede1 (7011110722654005156) -----------+
    | Member | Host  | Role    | State   | TL | Lag in MB |
    +--------+-------+---------+---------+----+-----------+
    | node1  | node1 | Leader  | running |  1 |           |
    | node2  | node2 | Replica | running |  1 |         0 |
    | node3  | node3 | Replica | running |  1 |         0 |
    +--------+-------+---------+---------+----+-----------+
    ```

2. `node1` is the current leader. Stop Patroni in `node1` to see how it changes the cluster:
    
    ```{.bash data-promp="$"}
    $ sudo systemctl stop patroni
    ```

3. Once the service stops in `node1`, check the logs in `node2` and `node3` using the following command: 

    ```{.bash data-promp="$"}
    $ sudo journalctl -u patroni.service -n 100 -f
    ```

    ??? admonition "Output"
        
        ```
        Sep 23 14:18:13 node03 patroni[10042]: 2021-09-23 14:18:13,905 INFO: no action. I am a secondary (node3) and following a leader (node1)
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,011 INFO: Got response from node2 http://node2:8008/patroni: {"state": "running", "postprimary_start_time": "2021-09-23 12:50:29.460027+00:00", "role": "replica", "server_version": 130003, "cluster_unlocked": true, "xlog": {"received_location": 67219152, "replayed_location": 67219152, "replayed_timestamp": "2021-09-23 13:19:50.329387+00:00", "paused": false}, "timeline": 1, "database_system_identifier": "7011110722654005156", "patroni": {"version": "2.1.0", "scope": "stampede1"}}
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,031 WARNING: Request failed to node1: GET http://node1:8008/patroni (HTTPConnectionPool(host='node1', port=8008): Max retries exceeded with url: /patroni (Caused by ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))))
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,038 INFO: Software Watchdog activated with 25 second timeout, timing slack 15 seconds
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,043 INFO: promoted self to leader by acquiring session lock
        Sep 23 14:18:20 node03 patroni[13641]: server promoting
        Sep 23 14:18:20 node03 patroni[10042]: 2021-09-23 14:18:20,049 INFO: cleared rewind state after becoming the leader
        Sep 23 14:18:21 node03 patroni[10042]: 2021-09-23 14:18:21,101 INFO: no action. I am (node3) the leader with the lock
        Sep 23 14:18:21 node03 patroni[10042]: 2021-09-23 14:18:21,117 INFO: no action. I am (node3) the leader with the lock
        Sep 23 14:18:31 node03 patroni[10042]: 2021-09-23 14:18:31,114 INFO: no action. I am (node3) the leader with the lock
        ...
        ```
  
    The logs in `node3` show that the requests to `node1` are failing, the watchdog is coming into action, and `node3` is promoting itself as the leader:

  
4. Verify that you can still access the cluster through the HAProxy instance and read data:

    ```{.bash data-promp="$"}
    $ psql -U postgres -h 10.104.0.6 -p 5000 -c "SELECT * FROM CUSTOMER;"

      name  | age
    --------+-----
     john   |  30
     dawson |  35
    (2 rows)
    ```


5. Restart the Patroni service in `node1`
    
    ```{.bash data-promp="$"}
    $ sudo systemctl start patroni
    ```

6. Check the current cluster status:  

    
    ```{.bash data-promp="$"}
    $ sudo patronictl -c /etc/patroni/patroni.yml list

    + Cluster: stampede1 (7011110722654005156) -----------+
    | Member | Host  | Role    | State   | TL | Lag in MB |
    +--------+-------+---------+---------+----+-----------+
    | node1  | node1 | Replica | running |  2 |         0 |
    | node2  | node2 | Replica | running |  2 |         0 |
    | node3  | node3 | Leader  | running |  2 |           |
    +--------+-------+---------+---------+----+-----------+

    ```

As we see, `node3` remains the leader and the rest are replicas.

#### Scenario 2. Abrupt machine shutdown or power outage 

To emulate the power outage, let's kill the service in `node3` and see what happens in `node1` and `node2`. 

1. Identify the process ID of Patroni and then kill it with a `-9` switch. 

    ```{.bash data-promp="$"}
    $ ps aux | grep -i patroni

    postgres   10042  0.1  2.1 647132 43948 ?        Ssl  12:50   0:09 /usr/bin/python3 /usr/bin/patroni /etc/patroni/patroni.yml

    $ sudo kill -9 10042
    ```

2. Check the logs on `node2`: 

    ```{.bash data-promp="$"}
    $ sudo journalctl -u patroni.service -n 100 -f
    ```

    ??? admonition "Output"

        ```
        Sep 23 14:40:41 node02 patroni[10577]: 2021-09-23 14:40:41,656 INFO: no action. I am a secondary (node2) and following a leader (node3)
        …
        Sep 23 14:41:01 node02 patroni[10577]: 2021-09-23 14:41:01,373 INFO: Got response from node1 http://node1:8008/patroni: {"state": "running", "postprimary_start_time": "2021-09-23 14:25:30.076762+00:00", "role": "replica", "server_version": 130003, "cluster_unlocked": true, "xlog": {"received_location": 67221352, "replayed_location": 67221352, "replayed_timestamp": null, "paused": false}, "timeline": 2, "database_system_identifier": "7011110722654005156", "patroni": {"version": "2.1.0", "scope": "stampede1"}}
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,364 WARNING: Request failed to node3: GET http://node3:8008/patroni (HTTPConnectionPool(host='node3', port=8008): Max retries exceeded with url: /patroni (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x7f57e06dffa0>, 'Connection to node3 timed out. (connect timeout=2)')))
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,373 INFO: Software Watchdog activated with 25 second timeout, timing slack 15 seconds
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,385 INFO: promoted self to leader by acquiring session lock
        Sep 23 14:41:03 node02 patroni[15478]: server promoting
        Sep 23 14:41:03 node02 patroni[10577]: 2021-09-23 14:41:03,397 INFO: cleared rewind state after becoming the leader
        Sep 23 14:41:04 node02 patroni[10577]: 2021-09-23 14:41:04,450 INFO: no action. I am (node2) the leader with the lock
        Sep 23 14:41:04 node02 patroni[10577]: 2021-09-23 14:41:04,475 INFO: no action. I am (node2) the leader with the lock
        …
        … 
        ```
    
    `node2` realizes that the leader is dead, and promotes itself as the leader.

3. Try accessing the cluster using the HAProxy endpoint at any point in time between these operations. The cluster is still accepting connections.


### Manual switchover

Typically, a manual switchover is needed for planned downtime to perform maintenance activity on the leader node. Patroni provides the `switchover` command to manually switch over from the leader node. 

Run the following command on `node2` (the current leader node):

```{.bash data-promp="$"}
$ sudo patronictl -c /etc/patroni/patroni.yml switchover
```

Patroni asks the name of the current primary node and then the node that should take over as the switched-over primary. You can also specify the time at which the switchover should happen. To trigger the process immediately, specify the value _now_:


```
primary [node2]: node2
Candidate ['node1', 'node3'] []: node1
When should the switchover take place (e.g. 2021-09-23T15:56 )  [now]: now
Current cluster topology
+ Cluster: stampede1 (7011110722654005156) -----------+
| Member | Host  | Role    | State   | TL | Lag in MB |
+--------+-------+---------+---------+----+-----------+
| node1  | node1 | Replica | running |  3 |         0 |
| node2  | node2 | Leader  | running |  3 |           |
| node3  | node3 | Replica | stopped |    |   unknown |
+--------+-------+---------+---------+----+-----------+
Are you sure you want to switchover cluster stampede1, demoting current primary node2? [y/N]: y
2021-09-23 14:56:40.54009 Successfully switched over to "node1"
+ Cluster: stampede1 (7011110722654005156) -----------+
| Member | Host  | Role    | State   | TL | Lag in MB |
+--------+-------+---------+---------+----+-----------+
| node1  | node1 | Leader  | running |  3 |           |
| node2  | node2 | Replica | stopped |    |   unknown |
| node3  | node3 | Replica | stopped |    |   unknown |
+--------+-------+---------+---------+----+-----------+
```


Restart the Patroni service in `node2` (after the "planned maintenance"). The node rejoins the cluster as a secondary.