> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/15/llms.txt).

# Install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux and derivatives

This document describes how to install Percona Distribution for PostgreSQL from Percona repositories on RPM-based distributions such as Red Hat Enterprise Linux and compatible derivatives. [Read more about Percona repositories](https://docs.percona.com/postgresql/15/repo-overview.html).

## Platform specific notes

To install Percona Distribution for PostgreSQL, do the following:

### For Percona Distribution for PostgreSQL packages

**CentOS 7**

Install the `epel-release` package:

```
$ sudo yum -y install epel-release
$ sudo yum repolist
```

**RHEL8/Oracle Linux 8/Rocky Linux 8**

Disable the `postgresql` module:

```
$ sudo dnf module disable postgresql
```

### For `percona-postgresql15-devel` package

You may need to install the `percona-postgresql15-devel` package when working with some extensions or creating programs that interface with PostgreSQL database. This package requires dependencies that are not part of the Distribution, but can be installed from the specific repositories:

**RHEL8**

```
$ sudo yum --enablerepo=codeready-builder-for-rhel-8-rhui-rpms 
$ sudo dnf install perl-IPC-Run -y
```

**Rocky Linux 8**

```
$ sudo dnf install dnf-plugins-core
$ sudo dnf config-manager --set-enabled powertools
```

**Oracle Linux 8**

```
$ sudo dnf config-manager --set-enabled ol8_codeready_builder 
$ sudo dnf install perl-IPC-Run -y
```

**RHEL9**

```
$ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-9-rhui-rpms
$ sudo dnf install perl-IPC-Run -y
```

If the required packages are not available in RHEL repos, install EPEL:

```
$ sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
$ sudo dnf install perl-IPC-Run -y
```

**Rocky Linux 9**

```
$ sudo dnf install dnf-plugins-core
$ sudo dnf config-manager --set-enabled crb
$ sudo dnf install perl-IPC-Run -y
```

**Oracle Linux 9**

```
$ sudo dnf config-manager --set-enabled ol9_codeready_builder 
$ sudo dnf install perl-IPC-Run -y
```

**RHEL10**

```
$ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-10-rhui-rpms
$ sudo dnf install perl-IPC-Run -y
```

If the required packages are not available in RHEL repos, install EPEL:

```
$ sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
$ sudo dnf install perl-IPC-Run -y
```

**Rocky Linux 10**

```
$ sudo dnf install dnf-plugins-core
$ sudo dnf config-manager --set-enabled crb
$ sudo dnf install perl-IPC-Run -y
```

**Oracle Linux 10**

```
$ sudo dnf config-manager --set-enabled ol10_codeready_builder 
$ sudo dnf install perl-IPC-Run -y
```

### For `percona-patroni` package

To install Patroni on Red Hat Enterprise Linux 9 and compatible derivatives, enable the `epel` repository

```
$ sudo yum install epel-release
```

### For `pgpool2` extension

To install `pgpool2` on Red Hat Enterprise Linux and compatible derivatives, enable the codeready builder repository first to resolve dependencies conflict for `pgpool2`.

The following are commands for Red Hat Enterprise Linux 9 and derivatives. For Red Hat Enterprise Linux 8, replace the operating system version in the commands accordingly.

**RHEL 9**

```
$ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-9-x86_64-rpms
```

**Rocky Linux 9**

```
$ sudo dnf config-manager --set-enabled crb
```

**Oracle Linux 9**

```
$ sudo dnf config-manager --set-enabled ol9_codeready_builder
```

### For PostGIS

For Red Hat Enterprise Linux 8 and derivatives, replace the operating system version in the following commands accordingly.

**RHEL 8**

Run the following commands:

1. Install DNF plugin utilities

   ```
   $ sudo dnf install dnf-plugins-core
   ```

1. Install the EPEL repository

   ```
   $ sudo dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
   ```

1. Enable the CodeReady Builder repository to resolve dependency conflicts

   ```
   $ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-8-rhui-rpms
   ```

1. Disable the default PostgreSQL module

   ```
   $ sudo dnf module disable postgresql
   ```

**RHEL 9**

Run the following commands:

1. Install DNF plugin utilities

   ```
   $ sudo dnf install dnf-plugins-core
   ```

1. Install the EPEL repository

   ```
   $ sudo dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
   ```

1. Enable the CodeReady Builder repository to resolve dependency conflicts

   ```
   $ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-9-rhui-rpms
   ```

**Oracle Linux 8**

Run the following commands:

1. Install the EPEL repository

   ```
   $ sudo dnf install -y epel-release
   ```

1. Install DNF plugin utilities

   ```
   $ sudo dnf install dnf-plugins-core
   ```

1. Enable the CodeReady Builder repository to resolve dependency conflicts

   ```
   $ sudo dnf config-manager --set-enabled ol8_codeready_builder
   ```

1. (Alternative) Install the latest EPEL release

   ```
   $ sudo dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
   ```

1. Disable the default PostgreSQL module

   ```
   $ sudo dnf module disable postgresql
   ```

**Oracle Linux 9**

Run the following commands:

1. Install the EPEL repository

   ```
   $ sudo dnf install -y epel-release
   ```

1. Install DNF plugin utilities

   ```
   $ sudo dnf install dnf-plugins-core
   ```

1. Enable the CodeReady Builder repository to resolve dependency conflicts

   ```
   $ sudo dnf config-manager --set-enabled ol9_codeready_builder
   ```

**Rocky Linux 8**

Run the following commands:

1. Install the EPEL release package

   ```
   $ sudo dnf install -y epel-release
   ```

1. Install DNF plugin utilities

   ```
   $ sudo dnf install dnf-plugins-core
   ```

1. Enable the PowerTools repository

   ```
   $ sudo dnf config-manager --set-enabled powertools
   ```

1. Disable the default PostgreSQL module

   ```
   $ sudo dnf module disable postgresql
   ```

**Rocky Linux 9**

Run the following commands:

1. Install the EPEL repository

   ```
   $ sudo dnf install -y epel-release
   ```

1. Install DNF plugin utilities

   ```
   $ sudo dnf install dnf-plugins-core
   ```

1. Enable the CodeReady Builder repository to resolve dependency conflicts

   ```
   $ sudo dnf config-manager --set-enabled crb
   ```

**RHEL UBI 9**

Run the following commands:

1. Configure the Oracle-Linux repository. Create the `/etc/yum.repos.d/oracle-linux-ol9.repo` file to install the required dependencies:

   /etc/yum.repos.d/oracle-linux-ol9.repo

   ```
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

1. Download the right GPG key for the Oracle Yum Repository:

   ```
   $ wget https://yum.oracle.com/RPM-GPG-KEY-oracle-ol9 -O /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
   ```

1. Install `epel` repository

   ```
   $ sudo yum install epel-release
   ```

## Procedure

Run all the commands in the following sections as root or using the `sudo` command.

### Install dependencies

Install `curl` for [Telemetry](https://docs.percona.com/postgresql/15/telemetry.html). We use it to better understand the use of our products and improve them.

```
$ sudo yum -y install curl
```

### Configure the repository

1. Install the `percona-release` repository management tool to subscribe to Percona repositories:

   ```
   $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
   ```

1. Enable the repository

Percona provides [two repositories](https://docs.percona.com/postgresql/15/repo-overview.html) for Percona Distribution for PostgreSQL. We recommend enabling the Major release repository to timely receive the latest updates.

```
$ sudo percona-release setup ppg-15
```

### Install packages

**Install using meta-package (deprecated)**

The [meta package](https://docs.percona.com/postgresql/15/repo-overview.html#percona-ppg-server) enables you to install several components of the distribution in one go.

```
$ sudo yum install percona-ppg-server15
```

**Install packages individually**

Run the following commands:

1. Install the PostgreSQL server package:

   ```
   $ sudo yum install percona-postgresql15-server
   ```

1. Install the components:

   Install `pg_repack`:

   ```
   $ sudo yum install percona-pg_repack15
   ```

   Install `pgaudit`:

   ```
   $ sudo yum install percona-pgaudit15
   ```

   Install `pgBackRest`:

   ```
   $ sudo yum install percona-pgbackrest
   ```

   Install `Patroni`:

   ```
   $ sudo yum install percona-patroni
   ```

   [Install `pg_stat_monitor`](https://docs.percona.com/pg-stat-monitor/install.html)

   Install `pgBouncer`:

   ```
   $ sudo yum install percona-pgbouncer
   ```

   Install `pgAudit-set_user`:

   ```
   $ sudo yum install percona-pgaudit15_set_user
   ```

   Install `pgBadger`:

   ```
   $ sudo yum install percona-pgbadger
   ```

   Install `wal2json`:

   ```
   $ sudo yum install percona-wal2json15
   ```

   Install PostgreSQL contrib extensions:

   ```
   $ sudo yum install percona-postgresql15-contrib
   ```

   Install HAProxy:

   ```
   $ sudo yum install percona-haproxy
   ```

   Install `pg_gather`:

   ```
   $ sudo yum install percona-pg_gather
   ```

   Install pgpool2:

   1. Check the [platform specific notes](#for-pgpool2-extension)

   1. Install the extension

      ```
      $ sudo yum install percona-pgpool-II-pg15
      ```

   Install pgvector package suite:

   ```
   $ sudo yum install percona-pgvector_15 percona-pgvector_15-debuginfo percona-pgvector_15-debugsource percona-pgvector_15-llvmjit
   ```

   Some extensions require additional setup in order to use them with Percona Distribution for PostgreSQL. For more information, refer to [Enabling extensions](https://docs.percona.com/postgresql/15/enable-extensions.html).

### Start the service

After the installation, the default database storage is not automatically initialized. To complete the installation and start Percona Distribution for PostgreSQL, initialize the database using the following command:

```
$ /usr/pgsql-15/bin/postgresql-15-setup initdb
```

Start the PostgreSQL service:

```
$ sudo systemctl start postgresql-15
```

Congratulations! Your Percona Distribution for PostgreSQL is up and running.

## Next steps

[Enable extensions](https://docs.percona.com/postgresql/15/enable-extensions.html)

[Connect to PostgreSQL](https://docs.percona.com/postgresql/15/connect.html)
