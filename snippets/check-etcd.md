3. Check the etcd cluster members. Use `etcdctl` for this purpose. Ensure that `etcdctl` interacts with etcd using API version 3 and knows which nodes, or endpoints, to communicate with. For this, we will define the required information as environment variables. Run the following commands on one of the nodes:

    ```
    export ETCDCTL_API=3
    HOST_1=10.104.0.1
    HOST_2=10.104.0.2
    HOST_3=10.104.0.3
    ENDPOINTS=$HOST_1:2379,$HOST_2:2379,$HOST_3:2379
    ```

4. Now, list the cluster members and output the result as a table as follows:
    
    ```{.bash data-prompt="$"}
    $ sudo etcdctl --endpoints=$ENDPOINTS -w table member list
    ```

    ??? example "Sample output"

        ```
        +------------------+---------+-------+------------------------+----------------------------+------------+
        |        ID        | STATUS  | NAME  |         PEER ADDRS     |        CLIENT ADDRS        | IS LEARNER |
        +------------------+---------+-------+------------------------+----------------------------+------------+
        | 4788684035f976d3 | started | node2 | http://10.104.0.2:2380 | http://192.168.56.102:2379 |      false |
        | 67684e355c833ffa | started | node3 | http://10.104.0.3:2380 | http://192.168.56.103:2379 |      false |
        | 9d2e318af9306c67 | started | node1 | http://10.104.0.1:2380 | http://192.168.56.101:2379 |      false |
        +------------------+---------+-------+------------------------+----------------------------+------------+
        ```

5. To check what node is currently the leader, use the following command

    ```{.bash data-prompt="$"}
    $ sudo etcdctl --endpoints=$ENDPOINTS -w table endpoint status
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
        |      ENDPOINT   |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
        +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
        | 10.104.0.1:2379 | 9d2e318af9306c67 |  3.5.16 |   20 kB |      true |      false |         2 |         10 |                 10 |        |
        | 10.104.0.2:2379 | 4788684035f976d3 |  3.5.16 |   20 kB |     false |      false |         2 |         10 |                 10 |        |
        | 10.104.0.3:2379 | 67684e355c833ffa |  3.5.16 |   20 kB |     false |      false |         2 |         10 |                 10 |        |
        +-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
        ```

        