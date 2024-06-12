# Migrate from PostgreSQL to Percona Distribution for PostgreSQL 


Percona Distribution for PostgreSQL includes the PostgreSQL database and additional extensions that have been selected to cover the needs of the enterprise and are guaranteed to work together. Percona Distribution for PostgreSQL is available as a software collection that is easy to deploy.

We encourage users to migrate from their PostgreSQL deployments based on community binaries to Percona Distribution for PostgreSQL. This document provides the migration instructions. 

Depending on your business requirements, you may migrate to Percona Distribution for PostgreSQL either [on the same server](#migrate-on-the-same-server) or [onto a different server](#migrate-on-a-different-server). 

## Migrate on the same server

=== "On Debian and Ubuntu Linux"

     >To ensure that your data is safe during the migration, we recommend to make a backup of your data and all configuration files (such as `pg_hba.conf`, `postgresql.conf`, `postgresql.auto.conf`) using the tool of your choice. The backup process is out of scope of this document. You can use `pg_dumpall` or other tools of your choice. For more information, see the blog post [PostgreSQL Upgrade Using pg_dumpall](https://www.percona.com/blog/postgresql-upgrade-using-pg_dumpall/) by _Avinash Vallarapu_, _Fernando Laudares Camargos_, _Jobin Augustine_ and _Nickolay Ihalainen_.

    Run **all** commands as root or via **sudo**:
    {.power-number}

     1. Stop the `postgresql` server   

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql.service
         ```

     2. Remove community packages

         ```{.bash data-prompt="$"}
         $ sudo apt-get --purge remove postgresql
         ```

      3. [Install percona-release :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/installing.html)
      4. Enable the repository

           ```{.bash data-prompt="$"}
           $ sudo percona-release setup ppg16
           ```

      5. [Install Percona Distribution for PostgreSQL packages](apt.md)
      6. (Optional) Restore the data from the backup.
      7. Start the `postgresql` service. The installation process starts and initializes the default cluster automatically. You can check its status with: 

          ```{.bash data-prompt="$"}
          $ sudo systemctl status postgresql
          ```         

         If `postresql` service is not started, start it manually:

           ```{.bash data-prompt="$"}
           $ sudo systemctl start postgresql.service
           ```


=== "On RHEL and derivatives"

       > To ensure that your data is safe during the migration, we recommend to make a backup of your data and all configuration files (such as `pg_hba.conf`, `postgresql.conf`, `postgresql.auto.conf`) using the tool of your choice. The backup process is out of scope of this document. You can use `pg_dumpall` or other tools of your choice. 

     Run **all** commands as root or via **sudo**:
    {.power-number}
    
    1. Stop the `postgresql` server   

          ```{.bash data-prompt="$"}
          $ sudo systemctl stop postgresql-16
          ```

      2. Remove community packages

         ```{.bash data-prompt="$"}
         $ sudo yum remove postgresql
         ```

      3. [Install percona-release :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/installing.html)
      4. Enable the repository

           ```{.bash data-prompt="$"}
           $ sudo percona-release setup ppg16
           ```

      5. [Install Percona Distribution for PostgreSQL packages](yum.md)
      6. (Optional) Restore the data from the backup.
      7. Start the `postgresql` service

          ```{.bash data-prompt="$"}
          $ sudo systemctl start postgresql-16
          ```


## Migrate on a different server

In this scenario, we will refer to the server with PostgreSQL Community as the "source" and to the server with Percona Distribution for PostgreSQL as the "target".

To migrate from PostgreSQL Community to Percona Distribution for PostgreSQL on a different server, do the following:

**On the source server**:
{.power-number}

1. Back up your data and all configuration files (such as `pg_hba.conf`, `postgresql.conf`, `postgresql.auto.conf`) using the tool of your choice.
2. Stop the `postgresql` service

    === "On Debian and Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql.service
         ```

    === "On RHEL and derivatives"

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql-16
         ```

3. Optionally, remove PostgreSQL Community packages 

**On the target server**:
{.power-number}

1. [Install percona-release :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/installing.html) 
2. Enable the repository

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup ppg16
    ```

3. [Install Percona Distribution for PostgreSQL packages](installing.md#installation-guidelines) on the target server.
4. Restore the data from the backup
5. Start `postgresql` service

    === "On Debian and Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo systemctl start postgresql.service
         ```

    === "On RHEL and derivatives"

         ```{.bash data-prompt="$"}
         $ sudo systemctl start postgresql-16
         ```