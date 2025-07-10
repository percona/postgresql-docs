# Initial setup for high availability

This guide provides instructions on how to set up a highly available PostgreSQL cluster with Patroni. This guide relies on the provided [architecture](ha-architecture.md) for high-availability.

## Considerations

1. This is an example deployment where etcd runs on the same host machines as the Patroni and PostgreSQL and there is a single dedicated HAProxy host. Alternatively etcd can run on different set of nodes. 

    If etcd is deployed on the same host machine as Patroni and PostgreSQL, separate disk system for etcd and PostgreSQL is recommended due to performance reasons.

2. For this setup, we will use the nodes that have the following IP addresses:


    | Node name     | Public IP address | Internal IP address
    |---------------|-------------------|--------------------
    | node1         | 157.230.42.174    | 10.104.0.7
    | node2         | 68.183.177.183    | 10.104.0.2
    | node3         | 165.22.62.167     | 10.104.0.8
    | HAProxy1      | 112.209.126.159   | 10.104.0.6
    | HAProxy2      | 134.209.111.138   | 10.104.0.5
    | HAProxy3      | 134.60.204.27     | 10.104.0.3
    | backup        | 97.78.129.11      | 10.104.0.9

    We also need a virtual IP address for HAProxy: `203.0.113.1`


!!! important

    We recommend not to expose the hosts/nodes where Patroni / etcd / PostgreSQL are running to public networks due to security risks.  Use Firewalls, Virtual networks, subnets or the like to protect the database hosts from any kind of attack. 

## Configure name resolution

It’s not necessary to have name resolution, but it makes the whole setup more readable and less error prone. Here, instead of configuring a DNS, we use a local name resolution by updating the file `/etc/hosts`. By resolving their hostnames to their IP addresses, we make the nodes aware of each other’s names and allow their seamless communication.

Run the following commands on each node.

1. Set the hostname for nodes. Change the node name to `node1`, `node2`,  `node3`, `HAProxy1`, `HAProxy2` and `backup`, respectively:

    ```{.bash data-prompt="$"}
    $ sudo hostnamectl set-hostname node1
    ```

2. Modify the `/etc/hosts` file of each node to include the hostnames and IP addresses of the remaining nodes. Add the following at the end of the `/etc/hosts` file on all nodes:   

    ```text 
    # Cluster IP and names

    10.104.0.7 node1    
    10.104.0.2 node2    
    10.104.0.8 node3    
    10.104.0.6 HAProxy1 
    10.104.0.5 HAProxy2 
    10.104.0.3 HAProxy3
    10.104.0.9 backup   
    ```

## Configure Percona repository

To install the software from Percona, you need to subscribe to Percona repositories. To do this, you require `percona-release` - the repository management tool. 

Run the following commands on each node as the root user or with `sudo` privileges.

1. Install `percona-release`

    === ":material-debian: On Debian and Ubuntu"

        --8<-- "percona-release-apt.md"

    === ":material-redhat: On RHEL and derivatives"

        --8<-- "percona-release-yum.md"

2. Enable the repository:

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup ppg{{pgversion}} 
    ```

## Next steps

[Set up etcd :material-arrow-right:](ha-etcd-config.md){.md-button}