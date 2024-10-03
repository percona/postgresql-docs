# pgBackRest setup

[pgBackRest :octicons-link-external-16:](https://pgbackrest.org/) is a backup tool used to perform PostgreSQL database backup, archiving, restoration, and point-in-time recovery. While it can be used for local backups, this procedure shows how to deploy a [pgBackRest server running on a dedicated host :octicons-link-external-16:](https://pgbackrest.org/user-guide-rhel.html#repo-host) and how to configure PostgreSQL servers to use it for backups and archiving.

You also need a backup storage to store the backups. It can either be a remote storage such as AWS S3, S3-compatible storages or Azure blob storage, or a filesystem-based one. 

## Configure backup server

To make things easier when working with some templates, run the commands below  as the root user. Run the following command to switch to the root user:
    
```{.bash data-prompt="$"}
$ sudo su -
```

### Install pgBackRest

1. Enable the repository with [percona-release :octicons-link-external-16:](https://www.percona.com/doc/percona-repo-config/index.html)

    ```{.bash data-prompt="$"}
    $ percona-release setup ppg-{{pgversion}}       
    ```

2. Install pgBackRest package

    === ":material-debian: On Debian/Ubuntu"

        ```{.bash data-prompt="$"}
        $ apt install percona-pgbackrest
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```{.bash data-prompt="$"}
        $ yum install percona-pgbackrest
        ```

### Create the configuration file

1. Create environment variables to simplify the config file creation:

    ```{.bash data-prompt="$"}
    export SRV_NAME="bkp-srv"
    export NODE1_NAME="node-1"
    export NODE2_NAME="node-2"
    export NODE3_NAME="node-3"
    export CA_PATH="/etc/ssl/certs/pg_ha"
    ```

2. Create the `pgBackRest` repository, *if necessary*

    A repository is where `pgBackRest` stores backups. In this example, the backups will be saved to `/var/lib/pgbackrest`.

    This directory is usually created during pgBackRest's installation process. If it's not there already, create it as follows:

    ```{.bash data-prompt="$"}
    $ mkdir -p /var/lib/pgbackrest
    $ chmod 750 /var/lib/pgbackrest
    $ chown postgres:postgres /var/lib/pgbackrest
    ```

3. The default `pgBackRest` configuration file location is `/etc/pgbackrest/pgbackrest.conf`, but some systems continue to use the old path, `/etc/pgbackrest.conf`, which remains a valid alternative. If the former is not present in your system, create the latter.

    Access the file's parent directory (either `cd /etc/` or `cd /etc/pgbackrest/`), and make a backup copy of it:

    ```{.bash data-prompt="$"}
    $ cp pgbackrest.conf pgbackrest.conf.bak
    ```

    Then use the following command to create a basic configuration file using the environment variables we created in a previous step:

    === ":material-debian: On Debian/Ubuntu"

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
        pg1-host-cert-file=${CA_PATH}/${SRV_NAME}.crt
        pg1-host-key-file=${CA_PATH}/${SRV_NAME}.key
        pg1-host-ca-file=${CA_PATH}/ca.crt
        pg1-socket-path=/var/run/postgresql 
     
        pg2-host=${NODE2_NAME}
        pg2-host-port=8432
        pg2-port=5432
        pg2-path=/var/lib/postgresql/{{pgversion}}/main
        pg2-host-type=tls
        pg2-host-cert-file=${CA_PATH}/${SRV_NAME}.crt
        pg2-host-key-file=${CA_PATH}/${SRV_NAME}.key
        pg2-host-ca-file=${CA_PATH}/ca.crt
        pg2-socket-path=/var/run/postgresql 
    
        pg3-host=${NODE3_NAME}
        pg3-host-port=8432
        pg3-port=5432
        pg3-path=/var/lib/postgresql/{{pgversion}}/main
        pg3-host-type=tls
        pg3-host-cert-file=${CA_PATH}/${SRV_NAME}.crt
        pg3-host-key-file=${CA_PATH}/${SRV_NAME}.key
        pg3-host-ca-file=${CA_PATH}/ca.crt
        pg3-socket-path=/var/run/postgresql
        EOF
        ```

    === ":material-redhat: On RHEL/derivatives"

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
        pg1-path=/var/lib/pgsql/{{pgversion}}/data
        pg1-host-type=tls
        pg1-host-cert-file=${CA_PATH}/${SRV_NAME}.crt
        pg1-host-key-file=${CA_PATH}/${SRV_NAME}.key
        pg1-host-ca-file=${CA_PATH}/ca.crt
        pg1-socket-path=/var/run/postgresql 
     
        pg2-host=${NODE2_NAME}
        pg2-host-port=8432
        pg2-port=5432
        pg2-path=/var/lib/pgsql/{{pgversion}}/data
        pg2-host-type=tls
        pg2-host-cert-file=${CA_PATH}/${SRV_NAME}.crt
        pg2-host-key-file=${CA_PATH}/${SRV_NAME}.key
        pg2-host-ca-file=${CA_PATH}/ca.crt
        pg2-socket-path=/var/run/postgresql 
    
        pg3-host=${NODE3_NAME}
        pg3-host-port=8432
        pg3-port=5432
        pg3-path=/var/lib/pgsql/{{pgversion}}/data
        pg3-host-type=tls
        pg3-host-cert-file=${CA_PATH}/${SRV_NAME}.crt
        pg3-host-key-file=${CA_PATH}/${SRV_NAME}.key
        pg3-host-ca-file=${CA_PATH}/ca.crt
        pg3-socket-path=/var/run/postgresql
        EOF
        ```

    *NOTE*: The option `backup-standby=y` above indicates the backups should be taken from a standby server. If you are operating with a primary only, or if your secondaries are not configured with `pgBackRest`, set this option to `n`.

### Create the certificate files
   
1. Create the folder to store the certificates:

    ```{.bash data-prompt="$"}
    $ mkdir -p ${CA_PATH}
    ```
    
2. Create the certificates and keys

    ```{.bash data-prompt="$"}
    $ openssl req -new -x509 -days 365 -nodes -out ${CA_PATH}/ca.crt -keyout ${CA_PATH}/ca.key -subj "/CN=root-ca"
    ```

3. Create the certificate for the backup and the PostgreSQL servers

    ```{.bash data-prompt="$"}
    $ for node in ${SRV_NAME} ${NODE1_NAME} ${NODE2_NAME} ${NODE3_NAME}
    do
    openssl req -new -nodes -out ${CA_PATH}/$node.csr -keyout ${CA_PATH}/$node.key -subj "/CN=$node";
    done
    ```

4. Sign the certificates with the `root-ca` key

    ```{.bash data-prompt="$"}
    $ for node in ${SRV_NAME} ${NODE1_NAME} ${NODE2_NAME} ${NODE3_NAME}
    do
    openssl x509 -req -in ${CA_PATH}/$node.csr -days 365 -CA ${CA_PATH}/ca.crt -CAkey ${CA_PATH}/ca.key -CAcreateserial -out ${CA_PATH}/$node.crt;
    done
    ```

5. Remove temporary files, set ownership of the remaining files to the `postgres` user, and restrict their access:

    ```{.bash data-prompt="$"}
    $ rm -f ${CA_PATH}/*.csr
    $ chown postgres:postgres -R ${CA_PATH}
    $ chmod 0600 ${CA_PATH}/*
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
    
2. Reload, start, and enable the service

    ```{.bash data-prompt="$"}
    $ systemctl daemon-reload
    $ systemctl start pgbackrest.service
    $ systemctl enable pgbackrest.service
    ```

## Configure database servers

Run the following commands on `node1`, `node2`, and `node3`.

1. Install pgBackRest package

    === ":material-debian: On Debian/Ubuntu"

        ```{.bash data-prompt="$"}
        $ apt install percona-pgbackrest
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```{.bash data-prompt="$"}
        $ yum install percona-pgbackrest
    
2. Export environment variables to simplify the config file creation:

    ```{.bash data-prompt="$"}
    $ export NODE_NAME=`hostname -f`
    $ export SRV_NAME="bkp-srv"
    $ export CA_PATH="/etc/ssl/certs/pg_ha"
    ```
    
3. Create the certificates folder:

    ```{.bash data-prompt="$"}
    $ mkdir -p ${CA_PATH}
    ```

4. Copy the `.crt`, `.key` certificate files and the `ca.crt` file from the backup server where they were created to every respective node. Then change the ownership to the `postgres` user and restrict their access. Use the following commands to achieve this:

    ```{.bash data-prompt="$"}
    $ scp ${SRV_NAME}:${CA_PATH}/{$NODE_NAME.crt,$NODE_NAME.key,ca.crt} ${CA_PATH}/
    $ chown postgres:postgres -R ${CA_PATH}
    $ chmod 0600 ${CA_PATH}/* 
    ```
   
5. Edit or create the configuration file which, as explained above, can be either at the `/etc/pgbackrest/pgbackrest.conf` or `/etc/pgbackrest.conf` path:

    === ":material-debian: On Debian/Ubuntu"

        ```ini title="pgbackrest.conf"
        cat <<EOF > pgbackrest.conf
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-user=postgres
        repo1-host-type=tls
        repo1-host-cert-file=${CA_PATH}/${NODE_NAME}.crt
        repo1-host-key-file=${CA_PATH}/${NODE_NAME}.key
        repo1-host-ca-file=${CA_PATH}/ca.crt
    
        # general options
        process-max=16
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
        EOF
        ```


    === ":material-redhat: On RHEL/derivatives"

        ```ini title="pgbackrest.conf"
        cat <<EOF > pgbackrest.conf
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-user=postgres
        repo1-host-type=tls
        repo1-host-cert-file=${CA_PATH}/${NODE_NAME}.crt
        repo1-host-key-file=${CA_PATH}/${NODE_NAME}.key
        repo1-host-ca-file=${CA_PATH}/ca.crt
    
        # general options
        process-max=16
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
        EOF
        ```

6. Create the pgbackrest `systemd` unit file at the path `/etc/systemd/system/pgbackrest.service`

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

7. Reload, start, and enable the service

    ```{.bash data-prompt="$"}
    $ systemctl daemon-reload
    $ systemctl start pgbackrest
    $ systemctl enable pgbackrest
    ```

    The pgBackRest daemon listens on port `8432` by default:

    ```{.bash data-prompt="$"}
    $ netstat -taunp
    Active Internet connections (servers and established)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
    tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      1/systemd           
    tcp        0      0 0.0.0.0:8432            0.0.0.0:*               LISTEN      40224/pgbackrest
    ```

8. If you are using Patroni, change its configuration to use `pgBackRest` for archiving and restoring WAL files. Run this command only on one node, for example, on `node1`: 

    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/patroni.yml edit-config
    ```
    
    === ":material-debian: On Debian/Ubuntu"

        ```yaml title="/etc/patroni/patroni.yml"
        postgresql:
          (...)
          parameters:
            (...)
            archive_command: pgbackrest --stanza=cluster_1 archive-push /var/lib/postgresql/{{pgversion}}/main/pg_wal/%f
            (...)
          recovery_conf:
            (...)
            restore_command: pgbackrest --config=/etc/pgbackrest.conf --stanza=cluster_1 archive-get %f %p
            (...)
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```yaml title="/etc/patroni/patroni.yml"
        postgresql:
          (...)
          parameters:
            archive_command: pgbackrest --stanza=cluster_1 archive-push /var/lib/pgsql/{{pgversion}}/data/pg_wal/%f
            (...)
          recovery_conf:
            restore_command: pgbackrest --config=/etc/pgbackrest.conf --stanza=cluster_1 archive-get %f %p
            (...)
        ```
   
    Reload the changed configurations:

    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/postgresql.yml reload
    ```

    <info>:material-information: Note:</i> When configuring a PostgreSQL server that is not managed by Patroni to archive/restore WALs from the `pgBackRest` server, edit the server's main configuration file directly and adjust the `archive_command` and `restore_command` variables as shown above.

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

[Test PostgreSQL cluster](ha-test.md){.md-button}
