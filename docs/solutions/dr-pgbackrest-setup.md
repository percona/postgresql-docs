# Deploying backup and disaster recovery solution in Percona Distribution for PostgreSQL

This document provides instructions of how to set up and test the backup and disaster recovery solution in Percona Distribution for PostgreSQL with `pgBackRest`. For technical overview and architecture description of this solution, refer to [Backup and disaster recovery in Percona Distribution for PostgreSQL](backup-recovery.md).

## Deployment 

As the example configuration, we will use the nodes with the following IP addresses:

| **Node name**   | **Internal IP address** |
| --------------- | ----------------------- |
| pg-primary      | 10.104.0.3              |
| pg-repo         | 10.104.0.5              |
| pg-secondary    | 10.104.0.4              |

### Set up hostnames

In our architecture, the `pgBackRest` repository is located on a remote host. To allow communication among the nodes, passwordless SSH is required. To achieve this, properly setting up hostnames in the `/etc/hosts` files is very important.

1. Define the hostname for every server in the `/etc/hostname` file. The following are the examples of how the `/etc/hostname` file in three nodes looks like:

    ```
    cat /etc/hostname
    pg-primary
    ```

    ```
    cat /etc/hostname
    pg-repo
    ```

    ```
    cat /etc/hostname
    pg-secondary
    ```

2. For the nodes to communicate seamlessly across the network, resolve their hostnames to their IP addresses in the `/etc/hosts` file.  (Alternatively, you can make appropriate entries in your internal DNS servers)

   The `/etc/hosts` file  for the `pg-primary node` looks like this:

    ```
    127.0.1.1 pg-primary pg-primary
    127.0.0.1 localhost
    10.104.0.5 pg-repo
    ```

   The `/etc/hosts` file in the `pg-repo` node looks like this:
    
    ```
    127.0.1.1 pg-repo pg-repo
    127.0.0.1 localhost
    10.104.0.3 pg-primary
    10.104.0.4 pg-secondary
    ```

   The `/etc/hosts` file in the `pg-secondary` node is shown below:

    ```
    127.0.1.1 pg-secondary pg-secondary
    127.0.0.1 localhost
    10.104.0.3 pg-primary
    10.104.0.5 pg-repo
    ```

### Set up passwordless SSH

Before setting up passwordless SSH, ensure that the _postgres_ user in all three instances has a password. 

1. To set or change the password, run the following command **as a root user**:

    ```sh
    $ passwd postgres
    ```

2. Type the new password and confirm it. 

3. After setting up the password, edit the `/etc/ssh/sshd_config` file and ensure the `PasswordAuthentication` variable is set as `yes`. 

    ```
    PasswordAuthentication yes 
    ```

4. In the `pg-repo` node, restart the `sshd` service. Without the restart, the SSH server will not allow you to connect to it using a password while adding the keys.

    ```sh
    $ sudo service sshd restart
    ```


5. In the `pg-primary` node, generate an SSH key pair and add the public key to the `pg-repo` node. 

    !!! important

        Run the commands as the **postgres** user. 

    * Generate SSH keys:   

        ```sh
        $ ssh-keygen -t rsa
        Generating public/private rsa key pair.
        Enter file in which to save the key (/root/.ssh/id_rsa): 
        Enter passphrase (empty for no passphrase): 
        Enter same passphrase again: 
        Your identification has been saved in /root/.ssh/id_rsa
        Your public key has been saved in /root/.ssh/id_rsa.pub
        The key fingerprint is:
        ...
        ```

    * Copy the public key to the `pg-repo` node:

        ```sh
        $ ssh-copy-id -i ~/.ssh/id_rsa.pub postgres@pg-repo
        /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
        /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
        /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
        postgres@pg-repo's password: 

        Number of key(s) added: 1

        
        Now try logging into the machine, with:   "ssh 'postgres@pg-repo'"
        and check to make sure that only the key(s) you wanted were added.
        ```

6. To verify everything has worked as expected, run the following command from the `pg-primary` node. 

    ```sh
    $ ssh postgres@pg-repo
    ```

    You should be able to connect to the `pg-repo` terminal without a password.

7. Repeat the SSH connection from `pg-repo` to `pg-primary` to ensure that passwordless SSH is working. 
8. Set up bidirectional passwordless SSH between `pg-repo` and `pg-secondary` using the same method. This will allow `pg-repo` to recover the backups to `pg-secondary`. 

### Install Percona Distribution for PostgreSQL

Install Percona Distribution for PostgreSQL in the primary and the secondary nodes from Percona repository. 

1. [Install `percona-release`](https://www.percona.com/doc/percona-repo-config/installing.html).
2. Enable the repository:

    ```sh
    $ sudo percona-release setup ppg14
    ```

3. Install Percona Distribution for PostgreSQL packages

    === "On Debian and Ubuntu"

         ```sh
         $ sudo apt install percona-postgresql-14 -y
         ```
   
    === "On RedHat Enterprise Linux and derivatives"

         ```sh
         $ sudo yum install percona-postgresql14-server
         ```

### Configure PostgreSQL on the primary node for continuous backup

At this step, configure the PostgreSQL instance on the `pg-primary` node for continuous archiving of the WAL files. 

!!! note

       On Debian and Ubuntu, the path to the configuration file is `/etc/postgresql/14/main/postgresql.conf`.

       On RHEL and CentOS, the path to the configuration file is `/var/lib/pgsql/14/data/`.


1. Edit the `postgresql.conf` configuration file to include the following changes:

     ```
     archive_command = 'pgbackrest --stanza=prod_backup archive-push %p'
     archive_mode = on
     listen_addresses = '*'
     log_line_prefix = ''
     max_wal_senders = 3
     wal_level = replica
     ```

2. Once the changes are saved, restart PostgreSQL.

    ```sh
    $ sudo systemctl restart postgresql
    ```

### Install pgBackRest

Install `pgBackRest` in all three instances from Percona repository. Use the following command:

=== "On Debian / Ubuntu"
  
     ``` bash
     $ sudo apt-get install percona-pgbackrest
     ```

=== "On RHEL / derivatives"

     ``` bash
     $ sudo yum install percona-pgbackrest
     ```

### Create the `pgBackRest` configuration file

Run the following commands on all three nodes to set up the required configuration file for `pgBackRest`.

1. Configure a location and permissions for the `pgBackRest` log rotation:
 
     ```sh
     $ sudo mkdir -p -m 770 /var/log/pgbackrest
     $ sudo chown postgres:postgres /var/log/pgbackrest
     ```

2. Configure the location and permissions for the `pgBackRest` configuration file:

   ```sh
   $ sudo mkdir -p /etc/pgbackrest
   $ sudo mkdir -p /etc/pgbackrest/conf.d
   $ sudo touch /etc/pgbackrest/pgbackrest.conf
   $ sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
   $ sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
   $ sudo mkdir -p /home/pgbackrest
   $ sudo chmod postgres:postgres /home/pgbackrest
   ```

### Update `pgBackRest` configuration file in the primary node

Configure `pgBackRest` on the `pg-primary` node by setting up a stanza. A stanza is a set of configuration parameters that tells `pgBackRest` where to backup its files. Edit the `/etc/pgbackrest/pgbackrest.conf` file in the `pg-primary` node to include the following lines:


```
[global]
repo1-host=pg-repo 
repo1-host-user=postgres
process-max=2
log-level-console=info
log-level-file=debug

[prod_backup]
pg1-path=/var/lib/postgresql/14/main
```


You can see the `pg1-path` attribute for the `prod_backup` stanza has been set to the PostgreSQL data folder.


### Update `pgBackRest` configuration file in the remote backup repository node

Add a stanza for the `pgBackRest` in the `pg-repo` node. Edit the `/etc/pgbackrest/pgbackrest.conf` configuration file to include the following lines:

```
[global]
repo1-path=/home/pgbackrest/pg_backup
repo1-retention-full=2
process-max=2
log-level-console=info
log-level-file=debug
start-fast=y
stop-auto=y
 
[prod_backup]
pg1-path=/var/lib/postgresql/14/main
pg1-host=pg-primary
pg1-host-user=postgres
pg1-port = 5432
```

### Initialize `pgBackRest` stanza in the remote backup repository node

After the configuration files are set up, it’s now time to initialize the `pgBackRest` stanza. Run the following command in the remote backup repository node (`pg-repo`).


```sh
$ sudo -u postgres pgbackrest --stanza=prod_backup stanza-create
2021-11-07 11:08:18.157 P00   INFO: stanza-create command begin 2.36: --exec-id=155883-2277a3e7 --log-level-console=info --log-level-file=off --pg1-host=pg-primary --pg1-host-user=postgres --pg1-path=/var/lib/postgresql/14/main --pg1-port=5432 --repo1-path=/home/pgbackrest/pg_backup --stanza=prod_backup
2021-11-07 11:08:19.453 P00   INFO: stanza-create for stanza 'prod_backup' on repo1
2021-11-07 11:08:19.566 P00   INFO: stanza-create command end: completed successfully (1412ms)
```


Once the stanza is created successfully, you can try out the different use cases for disaster recovery.


## Testing Backup and Restore with `pgBackRest`

This section covers a few use cases where `pgBackRest` can back up and restore databases either in the same instance or a different node.


### Use Case 1: Create a backup with `pgBackRest`

1. To start our testing, let’s create a table in the `postgres` database in the `pg-primary` node and add some data.

    ```sql
    CREATE TABLE CUSTOMER (id integer, name text);
    INSERT INTO CUSTOMER VALUES (1,'john');
    INSERT INTO CUSTOMER VALUES (2,'martha');
    INSERT INTO CUSTOMER VALUES (3,'mary');

    ```

2. Take a full backup of the database instance. Run the following commands from the `pg-repo` node:


```sh
$ pgbackrest -u postgres  --stanza=prod_backup backup --type=full
```


If you want an incremental backup, you can omit the `type` attribute. By default, `pgBackRest` always takes an incremental backup except the first backup of the cluster which is always a full backup. 

If you need a differential backup,  use _diff_ for the `type` field:

```sh
$ pgbackrest -u postgres --stanza=prod_backup backup --type=diff
```

### Use Case 2: Restore a PostgreSQL Instance from a full backup

For testing purposes, let's "damage" the PostgreSQL instance. 

1. Run the following command in the `pg-primary` node to delete the main data directory.

    
    ```sh
    $ rm -rf /var/lib/postgresql/14/main/*
    ```

2. To restore the backup, run the following commands. 

    * Stop the `postgresql` instance

       ```sh
       $ sudo systemctl stop postgresql
       ```

    * Restore the backup:

       ```sh
       $ pgbackrest -u postgres --stanza=prod_backup restore
       ```

    * Start the `postgresql` instance

       ```sh
       $ sudo systemctl start postgresql
       ```


3. After the command executes successfully, you can access PostgreSQL from the `psql` command line tool and check if the table and data rows have been restored.


### Use Case 3: Point-In-Time Recovery

If your target PostgreSQL instance has an already existing data directory, the full restore option will fail. You will get an error message stating there are existing data files.  In this case, you can use the `--delta` option to restore only the corrupted files. 

For example, let's say one of your developers mistakenly deleted a few rows from a table. You can use `pgBackRest` to revert your database to a previous point in time to recover the lost rows.

To test this use case, do the following:

1. Take a timestamp when the database is stable and error-free. Run the following command from the `psql `prompt.
     
     ```sql
     SELECT CURRENT_TIMESTAMP;
            current_timestamp       
     -------------------------------
      2021-11-07 11:55:47.952405+00
     (1 row)

     ```

    Note down the above timestamp since we will use this time in the restore command. Note that in a real life scenario, finding the correct point in time when the database was error-free may require extensive investigation. It is also important to note that all changes after the selected point will be lost after the roll back. 

2. Delete one of the customer records added before.

     
     ```sql
     DELETE FROM CUSTOMER WHERE ID=3;
     ```


3. To recover the data, run a command with the noted timestamp as an argument. Run the commands below to recover the database up to that time.

    * Stop the `postgresql` instance

       ```sh
       $ sudo systemctl stop postgresql
       ```

    * Restore the backup

       ```sh
       $ pgbackrest -u postgres --stanza=prod_backup --delta \
       --type=time "--target= 2021-11-07 11:55:47.952405+00" \
       --target-action=promote restore
       ```

    * Start the `postgresql` instance

       ```sh
       $ sudo systemctl start postgresql
       ```


4. Check the database table to see if the record has been restored.


     ```sql
     SELECT * FROM customer;
      id |  name  
     ----+--------
       1 | john
       2 | martha
       3 | mary
     (3 rows)
     ```



### Use Case 4: Restoring to a Separate PostgreSQL Instance

Sometimes a PostgreSQL server may encounter hardware issues and become completely inaccessible. In such cases, we will need to recover the database to a separate instance where `pgBackRest` is not initially configured. To restore the instance to a separate host, you have to first install both PostgreSQL and `pgBackRest` in this host. 

In our test setup, we already have PostgreSQL and `pgBackRest` installed in the third node, `pg-secondary`. Change the `pgBackRest` configuration file in the `pg-secondary` node as shown below.


```
[global]
repo1-host=pg-repo
repo1-host-user=postgres
process-max=2
log-level-console=info
log-level-file=debug
 
[prod_backup]
pg1-path=/var/lib/postgresql/14/main
```

There should be bidirectional passwordless SSH communication between `pg-repo` and `pg-secondary`. Refer to the [Set up passwordless SSH](#set-up-passwordless-ssh) section for the steps, if you haven’t configured it. 


Stop the PostgreSQL instance

```sh
$ sudo systemctl stop postgresql
```

Restore the database backup from `pg-repo` to `pg-secondary`.

```sh
$ pgbackrest -u postgres --stanza=prod_backup --delta restore

2021-11-07 13:34:08.897 P00   INFO: restore command begin 2.36: --delta --exec-id=109728-d81c7b0b --log-level-console=info --log-level-file=debug --pg1-path=/var/lib/postgresql/14/main --process-max=2 --repo1-host=pg-repo --repo1-host-user=postgres --stanza=prod_backup
2021-11-07 13:34:09.784 P00   INFO: repo1: restore backup set 20211107-111534F_20211107-131807I, recovery will start at 2021-11-07 13:18:07
2021-11-07 13:34:09.786 P00   INFO: remove invalid files/links/paths from '/var/lib/postgresql/14/main'
2021-11-07 13:34:11.803 P00   INFO: write updated /var/lib/postgresql/14/main/postgresql.auto.conf
2021-11-07 13:34:11.819 P00   INFO: restore global/pg_control (performed last to ensure aborted restores cannot be started)
2021-11-07 13:34:11.819 P00   INFO: restore size = 23.2MB, file total = 937
2021-11-07 13:34:11.820 P00   INFO: restore command end: completed successfully (2924ms)
```

After the restore completes successfully, restart PostgreSQL:

```sh
$ sudo systemctl start postgresql
```


Check the database contents from the local `psql` shell. 

```sql
SELECT * FROM customer;
 id |  name  
----+--------
  1 | john
  2 | martha
  3 | mary
(3 rows)
```