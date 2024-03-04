# pgBackRest setup

[pgBackRest](https://pgbackrest.org/) is a backup tool used to perform PostgreSQL database backup, archiving, restoration, and point-in-time recovery. While it can be used for local backups, this procedure shows how to deploy a [pgBackRest server running on a dedicated host](https://pgbackrest.org/user-guide-rhel.html#repo-host) and how to configure PostgreSQL servers to use it for backups and archiving.

You also need a backup storage to store the backups. It can either be a remote storage such as AWS S3, S3-compatible storages or Azure blob storage, or a filesystem-based one. 

## Configure backup server

### Install pgBackRest

1. Enable the repository with [percona-release](https://www.percona.com/doc/percona-repo-config/index.html)

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup ppg-16       
    ```

2. Install pgBackRest package

    === "Debian/Ubuntu"

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-pgbackrest
        ```

    === "RHEL/derivatives"

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbackrest
        ```

### Create the configuration file

1. Create environment variables to simplify the config file creation:

    ```bash
    export SRV_NAME="bkp-srv"
    export NODE1_NAME="node-1"
    export NODE2_NAME="node-2"
    export NODE3_NAME="node-3"
    ```

2. Create the `pgBackRest` repository, *if necessary*

    A repository is where `pgBackRest` stores backups. In this example, the backups will be saved to `/var/lib/pgbackrest`.
    This directory is usually created during pgBackRest's installation process. If it's not there already:

    ```{.bash data-prompt="$"}
    $ sudo mkdir -p /var/lib/pgbackrest
    $ sudo chmod 750 /var/lib/pgbackrest
    $ sudo chown postgres:postgres /var/lib/pgbackrest
    ```

3. The default `pgBackRest` configuration file location is `/etc/pgbackrest/pgbackrest.conf` but some systems continue to use the old default file, `/etc/pgbackrest.conf`, which remains a valid alternative. If the former is not present in your system, create the latter.

    Access the file's parent directory (either `cd /etc/` or `cd /etc/pgbackrest/`), make a backup copy of it:

    ```
    cp pgbackrest.conf pgbackrest.conf.orig
    ```

    Then use the following command to create a basic configuration file using the environment variables we created in a previous step:

    === "Debian/Ubuntu"

        ```
        cat <<EOF > pgbackrest.conf
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
        process-max=12
        log-level-console=info
        #log-level-file=debug
        log-level-file=info
        start-fast=y
        delta=y
        backup-standby=y 
    
        ########## Server TLS options ##########
        tls-server-address=*
        tls-server-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        tls-server-key-file=/pg_ha/certs/${SRV_NAME}.key
        tls-server-ca-file=/pg_ha/certs/ca.crt 
    
        ### Auth entry ###
        tls-server-auth=${NODE1_NAME}=cluster_1
        tls-server-auth=${NODE2_NAME}=cluster_1
        tls-server-auth=${NODE3_NAME}=cluster_1 
    
        ### Clusters and nodes ###
        [cluster_1]
        pg1-host=${NODE1_NAME}
        pg1-host-port=8432
        pg1-port=5432
        pg1-path=/var/lib/postgresql/16/main
        pg1-host-type=tls
        pg1-host-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        pg1-host-key-file=/pg_ha/certs/${SRV_NAME}.key
        pg1-host-ca-file=/pg_ha/certs/ca.crt
        pg1-socket-path=/var/run/postgresql 
     
        pg2-host=${NODE2_NAME}
        pg2-host-port=8432
        pg2-port=5432
        pg2-path=/var/lib/postgresql/16/main
        pg2-host-type=tls
        pg2-host-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        pg2-host-key-file=/pg_ha/certs/${SRV_NAME}.key
        pg2-host-ca-file=/pg_ha/certs/ca.crt
        pg2-socket-path=/var/run/postgresql 
    
        pg3-host=${NODE3_NAME}
        pg3-host-port=8432
        pg3-port=5432
        pg3-path=/var/lib/postgresql/16/main
        pg3-host-type=tls
        pg3-host-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        pg3-host-key-file=/pg_ha/certs/${SRV_NAME}.key
        pg3-host-ca-file=/pg_ha/certs/ca.crt
        pg3-socket-path=/var/run/postgresql
        EOF
        ```

    === "RHEL/derivatives"

        ```
        cat <<EOF > pgbackrest.conf
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
        process-max=12
        log-level-console=info
        #log-level-file=debug
        log-level-file=info
        start-fast=y
        delta=y
        backup-standby=y 
    
        ########## Server TLS options ##########
        tls-server-address=*
        tls-server-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        tls-server-key-file=/pg_ha/certs/${SRV_NAME}.key
        tls-server-ca-file=/pg_ha/certs/ca.crt 
    
        ### Auth entry ###
        tls-server-auth=${NODE1_NAME}=cluster_1
        tls-server-auth=${NODE2_NAME}=cluster_1
        tls-server-auth=${NODE3_NAME}=cluster_1 
    
        ### Clusters and nodes ###
        [cluster_1]
        pg1-host=${NODE1_NAME}
        pg1-host-port=8432
        pg1-port=5432
        pg1-path=/var/lib/pgsql/16/data
        pg1-host-type=tls
        pg1-host-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        pg1-host-key-file=/pg_ha/certs/${SRV_NAME}.key
        pg1-host-ca-file=/pg_ha/certs/ca.crt
        pg1-socket-path=/var/run/postgresql 
     
        pg2-host=${NODE2_NAME}
        pg2-host-port=8432
        pg2-port=5432
        pg2-path=/var/lib/pgsql/16/data
        pg2-host-type=tls
        pg2-host-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        pg2-host-key-file=/pg_ha/certs/${SRV_NAME}.key
        pg2-host-ca-file=/pg_ha/certs/ca.crt
        pg2-socket-path=/var/run/postgresql 
    
        pg3-host=${NODE3_NAME}
        pg3-host-port=8432
        pg3-port=5432
        pg3-path=/var/lib/pgsql/16/data
        pg3-host-type=tls
        pg3-host-cert-file=/pg_ha/certs/${SRV_NAME}.crt
        pg3-host-key-file=/pg_ha/certs/${SRV_NAME}.key
        pg3-host-ca-file=/pg_ha/certs/ca.crt
        pg3-socket-path=/var/run/postgresql
        EOF
        ```

    *NOTE*: The option `backup-standby=y` above indicates the backups should be taken from a standby server. If you are operating with a primary only, or if your secondaries are not configured with `pgBackRest`, set this option to `n`.

4. Create the `systemd` unit file at the path `/etc/systemd/system/pgbackrest.service`

    ```ini title="/etc/systemd/system/pgbackrest.service"
    [Unit]
    Description=pgBackRest Server
    After=network.target
    StartLimitIntervalSec=0

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

### Create the certificate files

1. Define the variable for the certificates path. For example, `/pg_ha/certs`:

    ```bash
    export CA_PATH="/pg_ha/certs"
    ```
    
2. Create the folder where to store the certificates:

    ```bash
    sudo mkdir -p ${CA_PATH}
    ```
    
3. Create the certificates and keys

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres openssl req -new -x509 -days 365 -nodes -out ${CA_PATH}/ca.crt -keyout ${CA_PATH}/ca.key -subj "/CN=root-ca"
    ```

4. Create the certificate for the backup server

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres openssl req -new -nodes -out ${CA_PATH}/${SRV_NAME}.csr -keyout ${CA_PATH}/${SRV_NAME}.key -subj "/CN=${SRV_NAME}"
    ```

5. Create the certificates for each node: `node1`, `node2`, `node3`

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres openssl req -new -nodes -out ${CA_PATH}/${NODE1_NAME}.csr -keyout ${CA_PATH}/${NODE1_NAME}.key -subj "/CN=${NODE1_NAME}"
    $ sudo -iu postgres openssl req -new -nodes -out ${CA_PATH}/${NODE2_NAME}.csr -keyout ${CA_PATH}/${NODE2_NAME}.key -subj "/CN=${NODE2_NAME}"
    $ sudo -iu postgres openssl req -new -nodes -out ${CA_PATH}/${NODE3_NAME}.csr -keyout ${CA_PATH}/${NODE3_NAME}.key -subj "/CN=${NODE3_NAME}"
    ```

6. Sign the certificates with the `root-ca` key

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres openssl x509 -req -in ${CA_PATH}/${SRV_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${SRV_NAME}.crt
    $ sudo -iu postgres openssl x509 -req -in ${CA_PATH}/${NODE1_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${NODE1_NAME}.crt
    $ sudo -iu postgres openssl x509 -req -in ${CA_PATH}/${NODE2_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${NODE2_NAME}.crt
    $ sudo -iu postgres openssl x509 -req -in ${CA_PATH}/${NODE3_NAME}.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/${NODE3_NAME}.crt
    ```

7. Remove temporary files, set ownership of the remaining files to the postgres user, and restrict their access:

    ```{.bash data-prompt="$"}
    $ sudo rm ${CA_PATH}/*.csr
    $ sudo chown postgres:postgres -R ${CA_PATH}
    $ sudo chomode 0600 ${CA_PATH}/*
    ``` 

8. Reload, enable, and start the service

    ```{.bash data-prompt="$"}
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable --now pgbackrest
    ```

## Configure database servers

Run the following commands on `node1`, `node2` and `node3`.

1. Install pgBackRest package

    === "Debian/Ubuntu"

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-pgbackrest
        ```

    === "RHEL/derivatives"

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbackrest
    
2. Export environment variables to simplify config file creation:

    ```bash
    export NODE_NAME=`hostname -f`
    export SRV_NAME="bkp-srv"
    ```
    
3. Create the certificates folder:

    ```{.bash data-prompt="$"}
    $ export CA_PATH="/pg_ha/certs"
    $ sudo mkdir -p ${CA_PATH}
    ```

4. You'll have to copy the respective node's `.crt` and `.key` certificate files as well as the `ca.crt` file over from the backup server where they have been created, something like:

    ```bash
    sudo scp ${SRV_NAME}:${CA_PATH}/{$NODE_NAME.crt,$NODE_NAME.key,ca.crt} ${CA_PATH}/
    sudo chown postgres:postgres -R ${CA_PATH}
    sudo chmod 0600 ${CA_PATH}/* 
    ```
   
5. Edit/create the configuration file which, as explained above, can be either `/etc/pgbackrest/pgbackrest.conf` or `/etc/pgbackrest.conf`:

    === "Debian/Ubuntu"

        ```ini title="pgbackrest.conf"
        cat <<EOF > pgbackrest.conf
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-user=postgres
        repo1-host-type=tls
        repo1-host-cert-file=/pg_ha/certs/${NODE_NAME}.crt
        repo1-host-key-file=/pg_ha/certs/${NODE_NAME}.key
        repo1-host-ca-file=/pg_ha/certs/ca.crt
    
        # general options
        process-max=16
        log-level-console=info
        log-level-file=debug
    
        # tls server options
        tls-server-address=*
        tls-server-cert-file=/pg_ha/certs/${NODE_NAME}.crt
        tls-server-key-file=/pg_ha/certs/${NODE_NAME}.key
        tls-server-ca-file=/pg_ha/certs/ca.crt
        tls-server-auth=${SRV_NAME}=cluster_1
    
        [cluster_1]
        pg1-path=/var/lib/postgresql/16/main
        EOF
        ```


    === "RHEL/derivatives"

        ```ini title="pgbackrest.conf"
        cat <<EOF > pgbackrest.conf
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-user=postgres
        repo1-host-type=tls
        repo1-host-cert-file=/pg_ha/certs/${NODE_NAME}.crt
        repo1-host-key-file=/pg_ha/certs/${NODE_NAME}.key
        repo1-host-ca-file=/pg_ha/certs/ca.crt
    
        # general options
        process-max=16
        log-level-console=info
        log-level-file=debug
    
        # tls server options
        tls-server-address=*
        tls-server-cert-file=/pg_ha/certs/${NODE_NAME}.crt
        tls-server-key-file=/pg_ha/certs/${NODE_NAME}.key
        tls-server-ca-file=/pg_ha/certs/ca.crt
        tls-server-auth=${SRV_NAME}=cluster_1
    
        [cluster_1]
        pg1-path=/var/lib/pgsql/16/data
        EOF
        ```

6. Create the `systemd` unit file at the path `/etc/systemd/system/pgbackrest.service`

    ```ini title="/etc/systemd/system/pgbackrest.service"
    [Unit]
    Description=pgBackRest Server
    After=network.target
    StartLimitIntervalSec=0

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

7. Reload, enable, and start the service

    ```{.bash data-prompt="$"}
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable --now pgbackrest
    ```

    The pgBackRest daemon listens on port `8432` by default:
    ```{.bash data-prompt="$"}
    $ sudo netstat -taunp
    Active Internet connections (servers and established)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
    tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      1/systemd           
    tcp        0      0 0.0.0.0:8432            0.0.0.0:*               LISTEN      40224/pgbackrest
    ```

9. Change Patroni configuration to use pgBackRest. Run this command on one node only, for example, on `node1`. Edit the `/etc/patroni/patroni.yml` file :

    === "Debian/Ubuntu"

        ```yaml title="/etc/patroni/patroni.yml"
        loop_wait: 10
        maximum_lag_on_failover: 1048576
        postgresql:
          parameters:
            archive_command: pgbackrest --stanza=cluster_1 archive-push /var/lib/postgresql/16/main/pg_wal/%f
            archive_mode: true
            archive_timeout: 1800s
            hot_standby: true
            logging_collector: 'on'
            max_replication_slots: 10
            max_wal_senders: 5
            wal_keep_size: 4096
            wal_level: logical
            wal_log_hints: true
          recovery_conf:
            recovery_target_timeline: latest
            restore_command: pgbackrest --config=/etc/pgbackrest.conf --stanza=cluster_1 archive-get %f %p
          use_pg_rewind: true
          use_slots: true
        retry_timeout: 10
        slots:
          percona_cluster_1:
            type: physical
        ttl: 30
        ```

    === "RHEL/derivatives"

        ```yaml title="/etc/patroni/patroni.yml"
        loop_wait: 10
        maximum_lag_on_failover: 1048576
        postgresql:
          parameters:
            archive_command: pgbackrest --stanza=cluster_1 archive-push /var/lib/pgsql/16/data/pg_wal/%f
            archive_mode: true
            archive_timeout: 1800s
            hot_standby: true
            logging_collector: 'on'
            max_replication_slots: 10
            max_wal_senders: 5
            wal_keep_size: 4096
            wal_level: logical
            wal_log_hints: true
          recovery_conf:
            recovery_target_timeline: latest
            restore_command: pgbackrest --config=/etc/pgbackrest.conf --stanza=cluster_1 archive-get %f %p
          use_pg_rewind: true
          use_slots: true
        retry_timeout: 10
        slots:
          percona_cluster_1:
            type: physical
        ttl: 30
        ```

    *NOTE*: When configuring a PostgreSQL server that is not managed by Patroni to archive/restore WALs from a pgBackRest server, edit it's main configuration file directly and adjust the `archive_command` and `restore_command` variables as shown above.

## Create backups

Run the following commands on the **backup server**

1. Create the stanza. A stanza is the configuration for a PostgreSQL database cluster that defines where it is located, how it will be backed up, archiving options, etc. 

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 stanza-create
    ```

2. Create a full backup

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 --type=full backup
    ```

3. Create an incremental backup

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 --type=incr backup
    ```

4. Check backup info
    
    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 info
    ```

5. Expire (remove) a backup. Be careful with removal, because removing a full backup also removes dependent incremental backups 

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 expire --set=20230617-021338F
    ```

[Test PostgreSQL cluster](ha-test.md){.md-button}
