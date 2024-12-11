# Install the software

## Install Percona Distribution for PostgreSQL

Run the following commands as root or with `sudo` privileges.

=== "On Debian / Ubuntu"

    1. Disable the upstream `postgresql-{{pgversion}}` package.
    
    2. Install the `percona-release` repository management tool

        --8<-- "percona-release-apt.md"
    
    
    3. Enable the repository

        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ppg{{pgversion}}
        ```   

    4. Install Percona Distribution for PostgreSQL package

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-postgresql-{{pgversion}}
        ```

=== "On RHEL and derivatives"

    1. Check the [platform specific notes](../yum.md#for-percona-distribution-for-postgresql-packages)

    2. Install the `percona-release` repository management tool

        --8<-- "percona-release-yum.md"
    
    3. 3. Enable the repository

        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ppg{{pgversion}}
        ```   

    4. Install Percona Distribution for PostgreSQL package

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-postgresql{{pgversion}}-server
        ```
    
    !!! important    

        **Don't** initialize the cluster and start the `postgresql` service. The cluster initialization and setup are handled by Patroni during the bootsrapping stage.

## Install Patroni, etcd, pgBackRest

=== "On Debian / Ubuntu"

    1. Install some Python and auxiliary packages to help with Patroni and etcd
    
        ```{.bash data-prompt="$"}
        $ sudo apt install python3-pip python3-dev binutils
        ```

    2. Install etcd, Patroni, pgBackRest packages:    

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-patroni \
        etcd etcd-server etcd-client \
        percona-pgbackrest
        ```

    3. Stop and disable all installed services:
    
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop {etcd,patroni,postgresql-{{pgversion}}}
        $ sudo systemctl disable {etcd,patroni,postgresql-{{pgversion}}}
        ```

    4. Even though Patroni can use an existing Postgres installation, remove the data directory to force it to initialize a new Postgres cluster instance.

       ```{.bash data-prompt="$"}
       $ sudo systemctl stop postgresql
       $ sudo rm -rf /var/lib/postgresql/{{pgversion}}/main
       ```

=== "On RHEL and derivatives"

    1. Install some Python and auxiliary packages to help with Patroni and etcd
    
        ```{.bash data-prompt="$"}
        $ sudo yum install python3-pip python3-devel binutils
        ```

    2. Install etcd, Patroni, pgBackRest packages. Check [platform specific notes for Patroni](../yum.md#for-percona-patroni-package):

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-patroni \
        etcd python3-python-etcd\
        percona-pgbackrest
        ```

    3. Stop and disable all installed services:
    
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop {etcd,patroni,postgresql}
        $ systemctl disable {etcd,patroni,postgresql}
        ```
        