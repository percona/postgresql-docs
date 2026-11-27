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

    !!! note
        The `pgBackRest` documentation recommends a dedicated system user to own the repository. This guide uses the `postgres` user, because the Percona packages create the `pgBackRest` directories and the `pgbackrest` service for this user.

3. The default `pgBackRest` configuration file location is `/etc/pgbackrest/pgbackrest.conf`, but the packages still use the old path, `/etc/pgbackrest.conf`, which remains a valid alternative. Use the following command to replace its content, using the environment variables we created in a previous step:

    === ":material-debian: On Debian/Ubuntu"

        ```
        echo "
        [global] 
        # Server repo details
        repo1-path=/var/lib/pgbackrest
        # Bundle small files together and store only the changed parts of files in differential and incremental backups.
        repo1-bundle=y
        repo1-block=y
    
        # Retention: number of full backups to keep.
        # pgBackRest removes the WAL archives that are no longer needed when it expires the backups.
        repo1-retention-full=4
    
        # Server general options
        # Number of parallel processes for backup. Set it to the number of CPUs of the server, or less.
        process-max=4
        # Use Zstandard compression, which is much faster than the default gzip with a similar compression ratio.
        compress-type=zst
        log-level-console=info
        log-level-file=detail
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
        
        " | sudo tee /etc/pgbackrest.conf
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```
        echo "
        [global] 
        # Server repo details
        repo1-path=/var/lib/pgbackrest
        # Bundle small files together and store only the changed parts of files in differential and incremental backups.
        repo1-bundle=y
        repo1-block=y
    
        # Retention: number of full backups to keep.
        # pgBackRest removes the WAL archives that are no longer needed when it expires the backups.
        repo1-retention-full=4
    
        # Server general options
        # Number of parallel processes for backup. Set it to the number of CPUs of the server, or less.
        process-max=4
        # Use Zstandard compression, which is much faster than the default gzip with a similar compression ratio.
        compress-type=zst
        log-level-console=info
        log-level-file=detail
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
        
        " | sudo tee /etc/pgbackrest.conf
        ```

    Where:

    * `repo1-retention-full` specifies how many full backups to keep. When a full backup expires, the differential and incremental backups that depend on it are removed too, together with the WAL archives older than the oldest remaining full backup. A new full backup must complete before the oldest one expires, so plan the disk space for one more full backup than this value. See the [Retention :octicons-link-external-16:](https://pgbackrest.org/user-guide.html#retention) section of the pgBackRest user guide for details.
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

    !!! warning
        The CA and the certificates created here are valid for 365 days. When they expire, `pgBackRest` can no longer connect between the hosts, so WAL archiving and backups stop. Adjust the `-days` value to match your security policy and renew the certificates before they expire.

7. Remove temporary files, set ownership of the remaining files to the `postgres` user, and restrict their access:

    ```{.bash data-prompt="$"}
    $ sudo rm -f ${CA_PATH}/*.csr
    $ sudo chown postgres:postgres -R ${CA_PATH}
    $ sudo chmod 0600 ${CA_PATH}/*
    ```

### Start the `pgBackRest` service

The Percona packages provide a `systemd` service that runs the `pgBackRest` TLS server.

1. Check that the service is available:

    ```{.bash data-prompt="$"}
    $ systemctl list-unit-files '*pgbackrest*'
    ```

    The service is named `percona-pgbackrest` on Debian and Ubuntu, and `pgbackrest` on RHEL and derivatives. If it is not available on your system, create it as described in the [Setup TLS Server :octicons-link-external-16:](https://pgbackrest.org/user-guide.html#repo-host/setup-tls) section of the `pgBackRest` user guide.

2. Enable and start the service:

    === ":material-debian: On Debian/Ubuntu"

        ```{.bash data-prompt="$"}
        $ sudo systemctl enable --now percona-pgbackrest
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```{.bash data-prompt="$"}
        $ sudo systemctl enable --now pgbackrest
        ```

3. Check that the `pgBackRest` server is running. It listens on port `8432` by default:

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest server-ping
    ```

## Configure database servers

Run the following commands on `node1`, `node2`, and `node3`.

Make sure that `pgBackRest` is installed on these nodes. If it isn't, [install it](#install-pgbackrest) first.

1. Export environment variables to simplify the config file creation:

    ```{.bash data-prompt="$"}
    $ export NODE_NAME=`hostname -f`
    $ export SRV_NAME="backup"
    $ export CA_PATH="/etc/ssl/certs/pg_ha"
    ```

2. Create the certificates folder:

    ```{.bash data-prompt="$"}
    $ sudo mkdir -p ${CA_PATH}
    ```

3. Copy the `.crt`, `.key` certificate files and the `ca.crt` file from the backup server where they were created to every respective node. Then change the ownership to the `postgres` user and restrict their access. Use the following commands to achieve this:

    ```{.bash data-prompt="$"}
    $ sudo scp ${SRV_NAME}:${CA_PATH}/{$NODE_NAME.crt,$NODE_NAME.key,ca.crt} ${CA_PATH}/
    $ sudo chown postgres:postgres -R ${CA_PATH}
    $ sudo chmod 0600 ${CA_PATH}/*
    ```

    The `scp` command requires SSH access from the node to the backup server. You can use any other secure method to transfer the files.

    Once the files are copied to all the nodes, the backup server no longer needs the keys of the nodes. Remove them by running the following command on the `backup` node:

    ```{.bash data-prompt="$"}
    $ sudo rm -f ${CA_PATH}/${NODE1_NAME}.key ${CA_PATH}/${NODE2_NAME}.key ${CA_PATH}/${NODE3_NAME}.key
    ```

    The CA key (`ca.key`) is only needed to sign new certificates. Move it from the backup server to a safe location.

4. Replace the content of the `/etc/pgbackrest.conf` configuration file:

    === ":material-debian: On Debian/Ubuntu"

        ```ini title="pgbackrest.conf"
        echo "
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-type=tls
        repo1-host-cert-file=${CA_PATH}/${NODE_NAME}.crt
        repo1-host-key-file=${CA_PATH}/${NODE_NAME}.key
        repo1-host-ca-file=${CA_PATH}/ca.crt
    
        # general options
        # Number of parallel processes for restore and archive-get. Set it to the number of CPUs of the server, or less.
        process-max=4
        # Compress the archived WAL files with Zstandard, as on the backup server.
        compress-type=zst
        log-level-console=info
        log-level-file=detail
        # Archive and restore WAL files asynchronously, to improve throughput.
        archive-async=y
        spool-path=/var/spool/pgbackrest
    
        # tls server options
        tls-server-address=*
        tls-server-cert-file=${CA_PATH}/${NODE_NAME}.crt
        tls-server-key-file=${CA_PATH}/${NODE_NAME}.key
        tls-server-ca-file=${CA_PATH}/ca.crt
        tls-server-auth=${SRV_NAME}=cluster_1
    
        # Only log warnings and errors from archive-push to the console, to keep the PostgreSQL logs readable.
        [global:archive-push]
        log-level-console=warn
        # Number of parallel processes for archive-push. Start with 2, so that archiving doesn't affect the database.
        process-max=2

        [cluster_1]
        pg1-path=/var/lib/postgresql/{{pgversion}}/main
        " | sudo tee /etc/pgbackrest.conf
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```ini title="pgbackrest.conf"
        echo "
        [global]
        repo1-host=${SRV_NAME}
        repo1-host-type=tls
        repo1-host-cert-file=${CA_PATH}/${NODE_NAME}.crt
        repo1-host-key-file=${CA_PATH}/${NODE_NAME}.key
        repo1-host-ca-file=${CA_PATH}/ca.crt
    
        # general options
        # Number of parallel processes for restore and archive-get. Set it to the number of CPUs of the server, or less.
        process-max=4
        # Compress the archived WAL files with Zstandard, as on the backup server.
        compress-type=zst
        log-level-console=info
        log-level-file=detail
        # Archive and restore WAL files asynchronously, to improve throughput.
        archive-async=y
        spool-path=/var/spool/pgbackrest
    
        # tls server options
        tls-server-address=*
        tls-server-cert-file=${CA_PATH}/${NODE_NAME}.crt
        tls-server-key-file=${CA_PATH}/${NODE_NAME}.key
        tls-server-ca-file=${CA_PATH}/ca.crt
        tls-server-auth=${SRV_NAME}=cluster_1
    
        # Only log warnings and errors from archive-push to the console, to keep the PostgreSQL logs readable.
        [global:archive-push]
        log-level-console=warn
        # Number of parallel processes for archive-push. Start with 2, so that archiving doesn't affect the database.
        process-max=2

        [cluster_1]
        pg1-path=/var/lib/pgsql/{{pgversion}}/data
        " | sudo tee /etc/pgbackrest.conf
        ```

    The `archive-async` option enables asynchronous operation for the `archive-push` and `archive-get` commands. `pgBackRest` stores transient data for these commands in the `spool-path` directory. This directory is usually created during pgBackRest's installation process. If it's not there already, create it as follows:

    ```{.bash data-prompt="$"}
    $ sudo mkdir -p -m 750 /var/spool/pgbackrest
    $ sudo chown postgres:postgres /var/spool/pgbackrest
    ```

    The asynchronous processes log their activity to the `/var/log/pgbackrest/cluster_1-archive-push-async.log` and `/var/log/pgbackrest/cluster_1-archive-get-async.log` files.

5. Check that the `pgBackRest` service is available, as described for the [backup server](#start-the-pgbackrest-service). Then enable and start it:

    === ":material-debian: On Debian/Ubuntu"

        ```{.bash data-prompt="$"}
        $ sudo systemctl enable --now percona-pgbackrest
        ```

    === ":material-redhat: On RHEL/derivatives"

        ```{.bash data-prompt="$"}
        $ sudo systemctl enable --now pgbackrest
        ```

6. Check that the `pgBackRest` server is running:

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest server-ping
    ```

7. If you are using Patroni, change its configuration to use `pgBackRest` for archiving and restoring WAL files. Run this command only on one node, for example, on `node1`:

    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/patroni.yml edit-config
    ```

    This opens the editor for you.

8. Change the configuration as follows:

    !!! warning
        The following configuration is an example of PostgreSQL parameters used for pgBackRest integration. **Do not replace your existing Patroni configuration with this example.** Merge the relevant parameters into your current configuration and preserve any existing settings required for your environment.

    ```yaml
    postgresql:
      parameters:
        archive_command: pgbackrest --stanza=cluster_1 archive-push "%p"
        archive_mode: on
        archive_timeout: 600s
      recovery_conf:
        restore_command: pgbackrest --stanza=cluster_1 archive-get %f "%p"
    ```

9. Save the changes and confirm them. Patroni applies the new configuration to all nodes and reloads PostgreSQL automatically. Check the state of the cluster:

    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/patroni.yml list
    ```

    If a node shows a `Pending restart` flag, for example because `archive_mode` was not enabled before, restart the flagged nodes. In our example we use the `cluster_1` cluster name:

    ```{.bash data-prompt="$"}
    $ patronictl -c /etc/patroni/patroni.yml restart cluster_1 --pending
    ```

    !!! note
         When configuring a PostgreSQL server that is not managed by Patroni to archive/restore WALs from the `pgBackRest` server, edit the server's main configuration file directly and adjust the `archive_command` and `restore_command` variables as shown above.

## Create backups

Run the following commands on the **backup server**:

1. Create the stanza. A stanza is the configuration for a PostgreSQL database cluster that defines where it is located, how it will be backed up, archiving options, etc. 

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 stanza-create
    ```

2. Check that the configuration is correct and that WAL archiving works:

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 check
    ```

    Run the same command on the PostgreSQL nodes to verify that they can reach the repository.

3. Create a full backup

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 --type=full backup
    ```

    After every successful backup, `pgBackRest` automatically runs the `expire` command to remove the backups and WAL archives that are no longer needed, according to the retention settings defined in the configuration file. You don't need to remove old backups manually.

4. Check backup info

    ```{.bash data-prompt="$"}
    $ sudo -iu postgres pgbackrest --stanza=cluster_1 info
    ```

## Next steps

[Configure HAProxy :material-arrow-right:](ha-haproxy.md){.md-button}
