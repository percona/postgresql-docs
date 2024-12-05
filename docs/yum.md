# Install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux and derivatives

This document describes how to install Percona Distribution for PostgreSQL from Percona repositories on RPM-based distributions such as Red Hat Enterprise Linux and compatible derivatives. [Read more about Percona repositories](repo-overview.md).

## Platform specific notes

To install Percona Distribution for PostgreSQL, do the following:

### For Percona Distribution for PostgreSQL packages

=== "CentOS 7"

    Install the `epel-release` package:

    ```{.bash data-prompt="$"}
    $ sudo yum -y install epel-release
    $ sudo yum repolist
    ```

=== "RHEL8/Oracle Linux 8/Rocky Linux 8"

    Disable the ``postgresql`` module:    

    ```{.bash data-prompt="$"}
    $ sudo dnf module disable postgresql
    ```

### For `percona-postgresql{{pgversion}}-devel` package

You may need to install the `percona-postgresql{{pgversion}}-devel` package when working with some extensions or creating programs that interface with PostgreSQL database. This package requires dependencies that are not part of the Distribution, but can be installed from the specific repositories:

=== "RHEL8"

    ```{.bash data-prompt="$"}
    $ sudo yum --enablerepo=codeready-builder-for-rhel-8-rhui-rpms install perl-IPC-Run -y
    ```

=== "Rocky Linux 8"

    ```{.bash data-prompt="$"}
    $ sudo dnf install dnf-plugins-core
    $ sudo dnf config-manager --set-enabled powertools
    ```

=== "Oracle Linux 8"

    ```{.bash data-prompt="$"}
    $ sudo dnf config-manager --set-enabled ol8_codeready_builder install perl-IPC-Run -y
    ```

=== "Rocky Linux 9"

    ```{.bash data-prompt="$"}
    $ sudo dnf install dnf-plugins-core
    $ sudo dnf config-manager --set-enabled crb
    $ sudo dnf install perl-IPC-Run -y
    ```

=== "Oracle Linux 9"

    ```{.bash data-prompt="$"}
    $ sudo dnf config-manager --set-enabled ol9_codeready_builder install perl-IPC-Run -y
    ```


### For `percona-patroni` package

To install Patroni on Red Hat Enterprise Linux 9 and compatible derivatives, enable the `epel` repository

```{.bash data-prompt="$"}
$ sudo yum install epel-release
```

### For `pgpool2` extension

To install `pgpool2` on Red Hat Enterprise Linux and compatible derivatives, enable the codeready builder repository first to resolve dependencies conflict for `pgpool2`.

The following are commands for Red Hat Enterprise Linux 9 and derivatives. For Red Hat Enterprise Linux 8, replace the operating system version in the commands accordingly. 

=== "RHEL 9"

    ```{.bash data-prompt="$"}
    $ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-9-x86_64-rpms
    ```

=== "Rocky Linux 9"

    ```{.bash data-prompt="$"}
    $ sudo dnf config-manager --set-enabled crb
    ```

=== "Oracle Linux 9"

    ```{.bash data-prompt="$"}
    $ sudo dnf config-manager --set-enabled ol9_codeready_builder
    ```

### For PostGIS 

For Red Hat Enterprise Linux 8 and derivatives, replace the operating system version in the following commands accordingly.

=== "RHEL 9"  

    Run the following commands:
    {.power-number}

    1. Install `epel` repository

        ```{.bash data-prompt="$"}
        $ sudo yum install epel-release
        ```

    2. Enable the codeready builder repository to resolve dependencies conflict. 

        ```{.bash data-prompt="$"}
        $ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-9-x86_64-rpms
        ```

=== "Rocky Linux 9"

    Run the following commands:
    {.power-number}

    1. Install `epel` repository

        ```{.bash data-prompt="$"}
        $ sudo yum install epel-release
        ```

    2. Enable the codeready builder repository to resolve dependencies conflict.

        ```{.bash data-prompt="$"}
        $ sudo dnf install dnf-plugins-core
        $ sudo dnf config-manager --set-enabled crb
        ```

=== "Oracle Linux 9"

    Run the following commands:
    {.power-number}

    1. Install `epel` repository

        ```{.bash data-prompt="$"}
        $ sudo yum install epel-release
        ```

    2. Enable the codeready builder repository to resolve dependencies conflict.

        ```{.bash data-prompt="$"}
        $ sudo dnf config-manager --set-enabled ol9_codeready_builder
        ```

=== "RHEL UBI 9"

    Run the following commands:
    {.power-number}

    1. Configure the Oracle-Linux repository. Create the `/etc/yum.repos.d/oracle-linux-ol9.repo` file to install the required dependencies: 

        ```init title="/etc/yum.repos.d/oracle-linux-ol9.repo"
        [ol9_baseos_latest]
        name=Oracle Linux 9 BaseOS Latest ($basearch)
        baseurl=https://yum.oracle.com/repo/OracleLinux/OL9/baseos/latest/$basearch/
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
        gpgcheck=1
        enabled=1     

        [ol9_appstream]
        name=Oracle Linux 9 Application Stream ($basearch)
        baseurl=https://yum.oracle.com/repo/OracleLinux/OL9/appstream/$basearch/
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
        gpgcheck=1
        enabled=1     

        [ol9_codeready_builder]
        name=Oracle Linux 9 CodeReady Builder ($basearch) - Unsupported
        baseurl=https://yum.oracle.com/repo/OracleLinux/OL9/codeready/builder/$basearch/
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
        gpgcheck=1
        enabled=1
        ```

    2. Download the right GPG key for the Oracle Yum Repository:    

        ```{.bash data-prompt="$"}
        $ wget https://yum.oracle.com/RPM-GPG-KEY-oracle-ol9 -O /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
        ```    

    3. Install `epel` repository    

        ```{.bash data-prompt="$"}
        $ sudo yum install epel-release
        ```    

## Procedure

Run all the commands in the following sections as root or using the `sudo` command.

### Install dependencies

Install `curl` for [Telemetry](telemetry.md). We use it to better understand the use of our products and improve them.

```{.bash data-prompt="$"}
$ sudo yum -y install curl
```

### Configure the repository {.power-number}

1. Install the `percona-release` repository management tool to subscribe to Percona repositories:

    ```{.bash data-prompt="$"}
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

2. Enable the repository

   Percona provides [two repositories](repo-overview.md) for Percona Distribution for PostgreSQL. We recommend enabling the Major release repository to timely receive the latest updates. 

   ```{.bash data-prompt="$"}
   $ sudo percona-release setup ppg-{{pgversion}}
   ```

### Install packages

=== "Install using meta-package"

     The [meta package](repo-overview.md#percona-ppg-server){:target=”_blank”} enables you to install several components of the distribution in one go.
     
     ```{.bash data-prompt="$"}
     $ sudo yum install percona-ppg-server{{pgversion}}
     ```

=== "Install packages individually"
    
    Run the following commands:
    {.power-number}

     1. Install the PostgreSQL server package:

         ```{.bash data-prompt="$"}
         $ sudo yum install percona-postgresql{{pgversion}}-server
         ```

     2. Install the components:

        Install `pg_repack`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pg_repack{{pgversion}}
        ```

        Install `pgaudit`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgaudit{{pgversion}}
        ```

        Install `pgBackRest`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbackrest
        ```

        Install `Patroni`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-patroni
        ```

        [Install `pg_stat_monitor`](pg-stat-monitor.md):


        Install `pgBouncer`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbouncer
        ```

        Install `pgAudit-set_user`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgaudit{{pgversion}}_set_user
        ```

        Install `pgBadger`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pgbadger
        ```

        Install `wal2json`:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-wal2json{{pgversion}}
        ```

        Install PostgreSQL contrib extensions:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-postgresql{{pgversion}}-contrib
        ```

        Install HAProxy
        
        ```{.bash data-prompt="$"}
        $ sudo yum install percona-haproxy
        ```
        
        Install `pg_gather`

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pg_gather
        ```

        Install pgpool2

        1. Check the [platform specific notes](#for-pgpool2-extension)
        2. Install the extension

            ```{.bash data-prompt="$"}
            $ sudo yum install percona-pgpool-II-pg{{pgversion}}
            ```
            
Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](enable-extensions.md).

### Start the service

After the installation, the default database storage is not automatically initialized. To complete the installation and start Percona Distribution for PostgreSQL, initialize the database using the following command:

```{.bash data-prompt="$"}
$ /usr/pgsql-{{pgversion}}/bin/postgresql-{{pgversion}}-setup initdb
```

Start the PostgreSQL service:

```{.bash data-prompt="$"}
$ sudo systemctl start postgresql-{{pgversion}}
```

Congratulations! Your Percona Distribution for PostgreSQL is up and running.

## Next steps

[Enable extensions :material-arrow-right:](enable-extensions.md){.md-button}

[Connect to PostgreSQL :material-arrow-right:](connect.md){.md-button}
