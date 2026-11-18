> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/16/llms.txt).

# Migrate from PostgreSQL to Percona Distribution for PostgreSQL

Percona Distribution for PostgreSQL includes the PostgreSQL database and additional extensions that have been selected to cover the needs of the enterprise and are guaranteed to work together. Percona Distribution for PostgreSQL is available as a software collection that is easy to deploy.

We encourage users to migrate from their PostgreSQL deployments based on community binaries to Percona Distribution for PostgreSQL. This document provides the migration instructions.

Depending on your business requirements, you may migrate to Percona Distribution for PostgreSQL either [on the same server](#migrate-on-the-same-server) or [onto a different server](#migrate-on-a-different-server).

## Migrate on the same server

**On Debian and Ubuntu Linux**

> To ensure that your data is safe during the migration, we recommend to make a backup of your data and all configuration files (such as `pg_hba.conf`, `postgresql.conf`, `postgresql.auto.conf`) using the tool of your choice. The backup process is out of scope of this document. You can use `pg_dumpall` or other tools of your choice. For more information, see the blog post [PostgreSQL Upgrade Using pg_dumpall](https://www.percona.com/blog/postgresql-upgrade-using-pg_dumpall/) by *Avinash Vallarapu*, *Fernando Laudares Camargos*, *Jobin Augustine* and *Nickolay Ihalainen*.

Run **all** commands as root or via **sudo**:

1. Stop the `postgresql` server

   ```
   $ sudo systemctl stop postgresql.service
   ```

1. Remove community packages

   ```
   $ sudo apt-get --purge remove postgresql
   ```

1. [Install percona-release](https://docs.percona.com/percona-software-repositories/installing.html)

1. Enable the repository

   ```
   $ sudo percona-release setup ppg16
   ```

1. [Install Percona Distribution for PostgreSQL packages](https://docs.percona.com/postgresql/16/apt.html)

1. (Optional) Restore the data from the backup.

1. Start the `postgresql` service. The installation process starts and initializes the default cluster automatically. You can check its status with:

   ```
   $ sudo systemctl status postgresql
   ```

   If `postresql` service is not started, start it manually:

   ```
   $ sudo systemctl start postgresql.service
   ```

**On RHEL and derivatives**

> To ensure that your data is safe during the migration, we recommend to make a backup of your data and all configuration files (such as `pg_hba.conf`, `postgresql.conf`, `postgresql.auto.conf`) using the tool of your choice. The backup process is out of scope of this document. You can use `pg_dumpall` or other tools of your choice.

Run **all** commands as root or via **sudo**:

1. Stop the `postgresql` server

   ```
   $ sudo systemctl stop postgresql-16
   ```

1. Remove community packages

   ```
   $ sudo yum remove postgresql
   ```

1. [Install percona-release](https://docs.percona.com/percona-software-repositories/installing.html)

1. Enable the repository

   ```
   $ sudo percona-release setup ppg16
   ```

1. [Install Percona Distribution for PostgreSQL packages](https://docs.percona.com/postgresql/16/yum.html)

1. (Optional) Restore the data from the backup.

1. Start the `postgresql` service

   ```
   $ sudo systemctl start postgresql-16
   ```

## Migrate on a different server

In this scenario, we will refer to the server with PostgreSQL Community as the “source” and to the server with Percona Distribution for PostgreSQL as the “target”.

To migrate from PostgreSQL Community to Percona Distribution for PostgreSQL on a different server, do the following:

**On the source server**:

1. Back up your data and all configuration files (such as `pg_hba.conf`, `postgresql.conf`, `postgresql.auto.conf`) using the tool of your choice.

1. Stop the `postgresql` service

   **On Debian and Ubuntu**

   ```
   $ sudo systemctl stop postgresql.service
   ```

   **On RHEL and derivatives**

   ```
   $ sudo systemctl stop postgresql-16
   ```

1. Optionally, remove PostgreSQL Community packages

**On the target server**:

1. [Install percona-release](https://docs.percona.com/percona-software-repositories/installing.html)

1. Enable the repository

   ```
   $ sudo percona-release setup ppg16
   ```

1. [Install Percona Distribution for PostgreSQL packages](https://docs.percona.com/postgresql/16/installing.html) on the target server.

1. Restore the data from the backup

1. Start `postgresql` service

   **On Debian and Ubuntu**

   ```
   $ sudo systemctl start postgresql.service
   ```

   **On RHEL and derivatives**

   ```
   $ sudo systemctl start postgresql-16
   ```
