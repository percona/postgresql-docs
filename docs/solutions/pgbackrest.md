# pgBackRest setup

[pgBackRest :octicons-link-external-16:](https://pgbackrest.org/) is a tool used to perform PostgreSQL database backups, archiving, restoration, and point-in-time recovery.

In this solution, a [pgBackRest server on a dedicated host :octicons-link-external-16:](https://pgbackrest.org/user-guide-rhel.html#repo-host) is deployed. pgBackRest is also installed and configured on the PostgreSQL servers to perform backups and manage WAL archiving.

## Preparation

Make sure to complete the [initial setup](ha-init-setup.md) steps.

## Install pgBackRest

Install pgBackRest on all nodes: `node1`, `node2`, `node3`, and `backup`.

=== ":material-debian: On Debian/Ubuntu"

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-pgbackrest
    ```

=== ":material-redhat: On RHEL/derivatives"

    ```{.bash data-prompt="$"}
    $ sudo yum install percona-pgbackrest
    ```

## Configure a backup server

Do the following steps on the `backup` node.

### Create the configuration file

1. Create environment variables to simplify the config file creation:

    ```{.bash data-prompt="$"}
    export SRV_NAME="backup"
    export NODE1_NAME="node1"
    export NODE2_NAME="node2"
    export NODE3_NAME="node3"
    export CA_PATH="/etc/ssl/certs/pg_ha"
    ```

2. Create the `pgBackRest` repository, *if necessary*.

    A repository is where `pgBackRest` stores backups. In this example, the backups will be saved to `/var/lib/pgbackrest`.

    This directory is usually created during pgBackRest's installation process. If it's not there already, create it as follows:

    ```{.bash data-prompt="$"}
    $ sudo mkdir -p /var/lib/pgbackrest
    $ sudo chmod 750 /var/lib/pgbackrest
    $ sudo chown postgres:postgres /var/lib/pgbackrest
    ```

3. The default `pgBackRest` configuration file location is `/etc/pgbackrest/pgbackrest.conf`, but some systems continue to use the old path, `/etc/pgbackrest.conf`, which remains a valid alternative. If the former is not present in your system, create the latter.

    Go to the file's parent directory (either `cd /etc/` or `cd /etc/pgbackrest/`), and make a backup copy of it:

    ```{.bash data-prompt="$"}
    $ sudo cp pgbackrest.conf pgbackrest.conf.orig
    ```

4. Then use the following command to create a basic configuration file using the environment variables we created in a previous step. This example command adds the configuration file at the path `/etc/pgbackrest.conf`.  Make sure to specify the correct path for the configuration file on your system:

    === ":material-debian: On Debian/Ubuntu"

        ```
        echo "
        [global] 
    
        # Server repo details
        repo1-path=/var/lib/pgbackrest 
    
        ### Retention ###
        #  - repo1-retention-archive-type
        #  - If set to full pgBackRest will keep archive logs for the number of full backups defined by repo-retention-archive
        repo1-retention-archive-type=full 
    
        # repo1-retention-archive
        #  - Number of backups worth of continuous WAL to retain
        #  - NOTE: WAL segments required to make a backup consistent are always retained until the backup is expired regardless of how this option is configured
        #  - If this value is not set and repo-retention-full-type is count (default), then the archive to expire will default to the repo-retention-full
        # repo1-retention-archive=2 
    
        # repo1-retention-full
        #  - Full backup retention count/time.
        #  - When a full backup expires, all differential and incremental backups associated with the full backup will also expire. 
        #  - When the option is not defined a warning will be issued. 
        #  - If indefinite retention is desired then set the option to the max value. 
        repo1-retention-full=4 
    
        # Server general options
        process-max=4  # This depends on the number of CPU resources your server has. The recommended value should equal or be less than the number of CPUs. While more processes can speed up backups, they will also consume additional system resources.
        log-level-console=info
        #log-level-file=debug
        log-level-file=info
        start-fast=y
        delta=y
        backup-standby=y 
    
        ########## Server TLS options ##########
        tls-server-address=*
        tls-server-cert-file=${CA_PATH}/${SRV_NAME}.crt
        tls-server-key-file=${CA_PATH}/${SRV_NAME}.key
        tls-server-ca-file=${CA_PATH}/ca.crt 
    
        ### Auth entry ###
        tls-server-auth=${NODE1_NAME}=cluster_1
        tls-server-auth=${NODE2_NAME}=cluster_1
        tls-server-auth=${NODE3_NAME}=cluster_1 
    
        ### Clusters and nodes ###
        [cluster_1]
        pg1-host=${NODE1_NAME}
        pg1-host-port=8432
        pg1-port=5432
        pg1-path=/var/lib/postgresql/{{pgversion}}/main
        pg1-host-type=tls
        pg1-host-cert-file=${CA_PATH}/${NODE1_NAME}.crt
        pg1-host-key-file=${CA_PATH}/${NODE1_NAME}.key
        pg1-host-ca-file=${CA_PATH}/ca.crt
        pg1-socket-path=/var/run/postgresql 
     
        pg2-host=${NODE2_NAME}
        pg2-host-port=8432
        pg2-port=5432
        pg2-path=/var/lib/postgresql/{{pgversion}}/main
        pg2-host-type=tls
        pg2-host-cert-file=${CA_PATH}/${NODE2_NAME}.crt
        pg2-host-key-file=${CA_PATH}/${NODE2_NAME}.key
        pg2-host-ca-file=${CA_PATH}/ca.crt
        pg2-socket-path=/var/run/postgresql 
    
        pg3-host=${NODE3_NAME}
        pg3-host-port=8432
        pg3-port=5432
        pg3-path=/var/lib/postgresql/{{pgversion}}/main
        pg3-host-type=tls
        pg3-host-cert-file=${CA_PATH}/${NODE3_NAME}.crt
        pg3-host-key-file=${CA_PATH}/${NODE3_NAME}.key
        pg3-host-ca-file=${CA_PATH}/ca.crt
        pg3-socket-path=/var/run/postgresql
        
        " | sudo tee /etc/pgbackrest.conf
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```
        echo "
        [global] 
    
        # Server repo details
        repo1-path=/var/lib/pgbackrest 
    
        ### Retention ###
        #  - repo1-retention-archive-type
        #  - If set to full pgBackRest will keep archive logs for the number of full backups defined by repo-retention-archive
        repo1-retention-archive-type=full 
    
        # repo1-retention-archive
        #  - Number of backups worth of continuous WAL to retain
        #  - NOTE: WAL segments required to make a backup consistent are always retained until the backup is expired regardless of how this option is configured
        #  - If this value is not set and repo-retention-full-type is count (default), then the archive to expire will default to the repo-retention-full
        # repo1-retention-archive=2 
    
        # repo1-retention-full
        #  - Full backup retention count/time.
        #  - When a full backup expires, all differential and incremental backups associated with the full backup will also expire. 
        #  - When the option is not defined a warning will be issued. 
        #  - If indefinite retention is desired then set the option to the max value. 
        repo1-retention-full=4 
    
        # Server general options
        process-max=4  # This depends on the number of CPU resources your server has. The recommended value should equal or be less than the number of CPUs. While more processes can speed up backups, they will also consume additional system resources.
        log-level-console=info
        #log-level-file=debug
        log-level-file=info
        start-fast=y
        delta=y
        backup-standby=y 
    
        ########## Server TLS options ##########
        tls-server-address=*
        tls-server-cert-file=${CA_PATH}/${SRV_NAME}.crt
        tls-server-key-file=${CA_PATH}/${SRV_NAME}.key
        tls-server-ca-file=${CA_PATH}/ca.crt 
    
        ### Auth entry ###
        tls-server-auth=${NODE1_NAME}=cluster_1
        tls-server-auth=${NODE2_NAME}=cluster_1
        tls-server-auth=${NODE3_NAME}=cluster_1 
    
        ### Clusters and nodes ###
        [cluster_1]
        pg1-host=${NODE1_NAME}
        pg1-host-port=8432
        pg1-port=5432
        pg1-path=/var/lib/postgresql/{{pgversion}}/main
        pg1-host-type=tls
        pg1-host-cert-file=${CA_PATH}/${NODE1_NAME}.crt
        pg1-host-key-file=${CA_PATH}/${NODE1_NAME}.key
        pg1-host-ca-file=${CA_PATH}/ca.crt
        pg1-socket-path=/var/run/postgresql 
     
        pg2-host=${NODE2_NAME}
        pg2-host-port=8432
        pg2-port=5432
        pg2-path=/var/lib/postgresql/{{pgversion}}/main
        pg2-host-type=tls
        pg2-host-cert-file=${CA_PATH}/${NODE2_NAME}.crt
        pg2-host-key-file=${CA_PATH}/${NODE2_NAME}.key
        pg2-host-ca-file=${CA_PATH}/ca.crt
        pg2-socket-path=/var/run/postgresql 
    
        pg3-host=${NODE3_NAME}
        pg3-host-port=8432
        pg3-port=5432
        pg3-path=/var/lib/postgresql/{{pgversion}}/main
        pg3-host-type=tls
        pg3-host-cert-file=${CA_PATH}/${NODE3_NAME}.crt
        pg3-host-key-file=${CA_PATH}/${NODE3_NAME}.key
        pg3-host-ca-file=${CA_PATH}/ca.crt
        pg3-socket-path=/var/run/postgresql
        
        " | sudo tee /etc/pgbackrest.conf
        ```

    Where:

    * `pgX-host` specifies the hostname of the PostgreSQL node
    * `pgX-host-port` specifies the port used by the pgBackRest server daemon on that node. The default pgBackRest server port is `8432`
    * `pgX-port` specifies the PostgreSQL server port (default `5432`)
    * `pgX-path` specifies the PostgreSQL data directory on the node

    The `pgX` prefix is repeated for each PostgreSQL node in the cluster (for example `pg1`, `pg2`, `pg3`).

    The numbering (`pg1`, `pg2`, `pg3`) represents individual PostgreSQL nodes defined in the cluster stanza.

    !!! note
         The option `backup-standby=y` above indicates the backups should be taken from a standby server. If you are operating with a primary only, or if your secondaries are not configured with `pgBackRest`, set this option to `n`.

### Create the certificate files

Run the following commands as a root user or with `sudo` privileges

1. Create the folder to store the certificates:

    ```{.bash data-prompt="$"}
    $ sudo mkdir -p /etc/ssl/certs/pg_ha
    ```

2. Create the environment variable to simplify further configuration

    ```{.bash data-prompt="$"}
    $ export CA_PATH="/etc/ssl/certs/pg_ha"
    ```

3. Create the CA certificates and keys

    ```{.bash data-prompt="$"}
    $ sudo openssl req -new -x509 -days 365 -nodes -out ${CA_PATH}/ca.crt -keyout ${CA_PATH}/ca.key -subj "/CN=root-ca"
    ```

4. Create the certificate and keys for the backup server

    ```{.bash data-prompt="$"}
    $ sudo openssl req -new -nodes -out ${CA_PATH}/${SRV_NAME}.csr -keyout ${CA_PATH}/${SRV_NAME}.key -subj "/CN=${SRV_NAME}"
    ```

5. Create the certificates and keys for each PostgreSQL node

    ```{.bash data-prompt="$"}
    $ sudo openssl req -new -nodes -out ${CA_PATH}/${NODE1_NAME}.csr -keyout ${CA_PATH}/${NODE1_NAME}.key -subj "/CN=${NODE1_NAME}"
    $ sudo openssl req -new -nodes -out ${CA_PATH}/${NODE2_NAME}.csr -keyout ${CA_PATH}/${NODE2_NAME}.key -subj "/CN=${NODE2_NAME}"
    $ sudo openssl req -new -nodes -out ${CA_PATH}/${NODE3_NAME}.csr -keyout ${CA_PATH}/${NODE3_NAME}.key -subj "/CN=${NODE3_NAME}"
    ```

6. Sign all certificates with the `root-ca` key

    ```{.bash data-prompt="$"}
    $ sudo openssl x509 -req -in ${CA_PATH}/${SRV_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${SRV_NAME}.crt
    $ sudo openssl x509 -req -in ${CA_PATH}/${NODE1_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${NODE1_NAME}.crt
    $ sudo openssl x509 -req -in ${CA_PATH}/${NODE2_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${NODE2_NAME}.crt
    $ sudo openssl x509 -req -in ${CA_PATH}/${NODE3_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${NODE3_NAME}.crt
    ```

7. Remove temporary files, set ownership of the remaining files to the `postgres` user, and restrict their access:

    ```{.bash data-prompt="$"}
    $ sudo rm -f ${CA_PATH}/*.csr
    $ sudo chown postgres:postgres -R ${CA_PATH}
    $ sudo chmod 0600 ${CA_PATH}/*
    ```

### Create the `pgbackrest` daemon service

1. Create the `systemd` unit file at the path `/etc/systemd/system/pgbackrest.service`

    ```ini title="/etc/systemd/system/pgbackrest.service"
    [Unit]
    Description=pgBackRest Server
    After=network.target

    [Service]
    Type=simple
    User=postgres
    Restart=always
    RestartSec=1
    ExecStart=/usr/bin/pgbackrest server
    #ExecStartPost=/bin/sleep 3
    #ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
    ExecReload=/bin/kill -HUP $MAINPID

    [Install]
    WantedBy=multi-user.target
    ```

2. Make `systemd` aware of the new service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl daemon-reload
    ```

3. Enable `pgBackRest`:

    ```{.bash data-prompt="$"}
    $ sudo systemctl enable --now pgbackrest.service
    ```

## Configure database servers

Run the following commands on `node1`, `node2`, and `node3`.

1. Install `pgBackRest` package

    === ":material-debian: On Debian/Ubuntu"

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-pgbackrest
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbackrest
        ```

2. Export environment variables to simplify the config file creation:

    ```{.bash data-prompt="$"}
    $ export NODE_NAME=`hostname -f`
    $ export SRV_NAME="backup"
    $ export CA_PATH="/etc/ssl/certs/pg_ha"
    ```

3. Create the certificates folder:

    ```{.bash data-prompt="$"}
    $ sudo mkdir -p ${CA_PATH}
    ```

4. Copy the `.crt`, `.key` certificate files and the `ca.crt` file from the backup server where they were created to every respective node. Then change the ownership to the `postgres` user and restrict their access. Use the following commands to achieve this:

    ```{.bash data-prompt="$"}
    $ sudo scp ${SRV_NAME}:${CA_PATH}/{$NODE_NAME.crt,$NODE_NAME.key,ca.crt} ${CA_PATH}/
    $ sudo chown postgres:postgres -R ${CA_PATH}
    $ sudo chmod 0600 ${CA_PATH}/* 
    ```

5. Make a copy of the configuration file. The path to it can be either `/etc/pgbackrest/pgbackrest.conf` or `/etc/pgbackrest.conf`:

    ```{.bash data-prompt="$"}
    $ sudo cp pgbackrest.conf pgbackrest.conf.orig
    ```

6. Create the configuration file. This example command adds the configuration file at the path `/etc/pgbackrest.conf`. Make sure to specify the correct path for the configuration file on your system:

    === ":material-debian: On Debian/Ubuntu"

        ```ini title="pgbackrest.conf"
        echo "
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-user=postgres
        repo1-host-type=tls
        repo1-host-cert-file=${CA_PATH}/${NODE_NAME}.crt
        repo1-host-key-file=${CA_PATH}/${NODE_NAME}.key
        repo1-host-ca-file=${CA_PATH}/ca.crt
    
        # general options
        process-max=6
        log-level-console=info
        log-level-file=debug
    
        # tls server options
        tls-server-address=*
        tls-server-cert-file=${CA_PATH}/${NODE_NAME}.crt
        tls-server-key-file=${CA_PATH}/${NODE_NAME}.key
        tls-server-ca-file=${CA_PATH}/ca.crt
        tls-server-auth=${SRV_NAME}=cluster_1
    
        [cluster_1]
        pg1-path=/var/lib/postgresql/{{pgversion}}/main
        " | sudo tee /etc/pgbackrest.conf
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```ini title="pgbackrest.conf"
        echo "
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-user=postgres
        repo1-host-type=tls
        repo1-host-cert-file=${CA_PATH}/${NODE_NAME}.crt
        repo1-host-key-file=${CA_PATH}/${NODE_NAME}.key
        repo1-host-ca-file=${CA_PATH}/ca.crt
    
        # general options
        process-max=6
        log-level-console=info
        log-level-file=debug
    
        # tls server options
        tls-server-address=*
        tls-server-cert-file=${CA_PATH}/${NODE_NAME}.crt
        tls-server-key-file=${CA_PATH}/${NODE_NAME}.key
        tls-server-ca-file=${CA_PATH}/ca.crt
        tls-server-auth=${SRV_NAME}=cluster_1
    
        [cluster_1]
        pg1-path=/var/lib/pgsql/{{pgversion}}/data
        " | sudo tee /etc/pgbackrest.conf
        ```

7. Create the pgbackrest `systemd` unit file at the path `/etc/systemd/system/pgbackrest.service`

    ```ini title="/etc/systemd/system/pgbackrest.service"
    [Unit]
    Description=pgBackRest Server
    After=network.target

    [Service]
    Type=simple
    User=postgres
    Restart=always
    RestartSec=1
    ExecStart=/usr/bin/pgbackrest server
    #ExecStartPost=/bin/sleep 3
    #ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
    ExecReload=/bin/kill -HUP $MAINPID

    [Install]
    WantedBy=multi-user.target
    ```

8. Reload `systemd` and start the service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable --now pgbackrest
    ```

    The pgBackRest daemon listens on port `8432` by default:

    ```{.bash data-prompt="$"}
    $ netstat -taunp | grep '8432'
    ```

    ??? example "Sample output"

        ```{text .no-copy}
        Active Internet connections (servers and established)
        Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
        tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      1/systemd           
        tcp        0      0 0.0.0.0:8432            0.0.0.0:*               LISTEN      40224/pgbackrest
        ```

9. If you are using Patroni, change its configuration to use `pgBackRest` for archiving and restoring WAL files. Run this command only on one node, for example, on `node1`:

    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/patroni.yml edit-config
    ```

    This opens the editor for you.

10. Change the configuration as follows:

    ```yaml title="/etc/patroni/patroni.yml"
    postgresql:
      parameters:
        archive_command: pgbackrest --stanza=cluster_1 archive-push /var/lib/postgresql/{{pgversion}}/main/pg_wal/%f
        archive_mode: true
        archive_timeout: 600s
        hot_standby: true
        logging_collector: 'on'
        max_replication_slots: 10
        max_wal_senders: 5
        max_wal_size: 10GB
        wal_keep_segments: 10
        wal_level: logical
        wal_log_hints: true
      recovery_conf:
        recovery_target_timeline: latest
        restore_command: pgbackrest --config=/etc/pgbackrest.conf --stanza=cluster_1 archive-get %f "%p"
      use_pg_rewind: true
      use_slots: true
    retry_timeout: 10
    slots:
      percona_cluster_1:
        type: physical
    ttl: 30
    ```

11. Reload the changed configurations. Provide the cluster name or the node name for the following command. In our example we use the `cluster_1` cluster name:

    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/patroni.yml restart cluster_1
    ```

    It may take a while to reload the new configuration.

    !!! note
         When configuring a PostgreSQL server that is not managed by Patroni to archive/restore WALs from the `pgBackRest` server, edit the server's main configuration file directly and adjust the `archive_command` and `restore_command` variables as shown above.

## Create backups

Run the following commands on the **backup server**:

1. Create the stanza. A stanza is the configuration for a PostgreSQL database cluster that defines where it is located, how it will be backed up, archiving options, etc. 

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 stanza-create
    ```

2. Create a full backup

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 --type=full backup
    ```

3. Check backup info

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 info
    ```

4. Expire (remove) a backup:

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 expire --set=<BACKUP_ID>
    ```

## Next steps

[Configure HAProxy :material-arrow-right:](ha-haproxy.md){.md-button}
