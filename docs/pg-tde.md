# pg_tde

!!! note

    This is the Alpha 1 version of the extension and is not recommended for production use yet. Please use it in testing environments only. 

## Overview

`pg_tde` stands for Transparent Data Encryption for PostgreSQL. This is an open-source extension designed to enhance PostgreSQL’s security by encrypting data files on disk.  The encryption is transparent for users allowing them to access and manipulate the data and not to worry about the encryption process.

Unlike traditional encryption methods that require significant changes to database schemas and applications, `pg_tde` seamlessly integrates with PostgreSQL, encrypting data at the table level without disrupting existing workflows. It uses the Advanced Encryption Standard (AES) encryption algorithm.

### Key features:

* Encryption of heap tables, including TOAST.
* Storage of encryption keys in either a Hashicorp Vault server or a local keyring file (primarily for development purposes).
* Configurable encryption settings per database: you can choose which tables to encrypt, achieving granular control over data protection.
* Replication support.
* Enhanced security through the ability to rotate master keys used for data encryption, reducing the risk of long-term exposure to potential attacks and aiding compliance with security standards like GDPR, HIPAA, and PCI DSS.

## Installation

This section provides instructions how to install `pg_tde` from Percona repositories using the package manager of your operating system. For other installation methods, refer to the [`pg_tde` documentation :octicons-link-external-16:](https://percona-lab.github.io/pg_tde/main/install.html#procedure).

=== ":material-debian: :material-debian: On Debian and Ubuntu"

    `pg_tde` packages are available for the following Linux distributions:

    * Ubuntu 20.04 (Focal Fossa)
    * Ubuntu 22.04 (Jammy Jellyfish)
    * Debian 10 (Buster)
    * Debian 11 (Bullseye)
    * Debian 12 (Bookworm)

    To install `pg_tde`, run the following commands as the root user or with the `sudo` privileges:

    1. [Install `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/installing.html) repository management tool.

    2. Enable the repository:

        ```{.bash data-prompt="$"}
        $ sudo percona-release enable-only ppg-16.2 testing
        ```     
    
    3. Install the package: 
       
        ```{.bash data-prompt="$"}
        $ sudo apt-get install percona-postgresql-16-pg-tde
        ```

=== ":material-redhat: On Red Hat Enterprise Linux and compatible derivatives"

    `pg_tde` packages are available for the following Linux distributions:

    * Red Hat Enterprise Linux and CentOS 7
    * Red Hat Enterprise Linux 8 and compatible derivatives
    * Red Hat Enterprise Linux 9 and compatible derivatives

    To install `pg_tde`, run the following commands as the root user or with the `sudo` privileges:

    1. Enable / disable modules:

        === "CentOS 7"

            Install the `epel-release` package:

            ```{.bash data-prompt="$"}
            $ sudo yum -y install epel-release
            $ sudo yum repolist
            ```

        === "RHEL8/Oracle Linux 8/Rocky Linux 8"

            Disable the ``postgresql``  and ``llvm-toolset``modules:    

            ```{.bash data-prompt="$"}
            $ sudo dnf module disable postgresql llvm-toolset
            ```

    2. [Install `percona-release`     :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/    installing.html) repository management tool.

    3. Enable the repository:

        ```{.bash data-prompt="$"}
        $ sudo percona-release enable-only ppg-16.2 testing
        ``` 

    4. Install the package:
        
        ```{.bash data-prompt="$"}
        $ sudo yum install percona-pg_tde_16
        ```

## Setup

`pg_tde` requires additional setup steps in order to use it with PostgreSQL. 
This section provides setup using the HashiCorp Vault server for storing encryption key as the recommended approach. Please see [`pg_tde` documentation :octicons-link-external-16:] for alternative configuration using a keyfile.

The setup of the Vault server is out of scope of this document. We're assuming you have the Vault server up and running and have the following information required for the setup:

* The secret access token to the Vault server
* The URL to access the Vault server
* (Optional) The CA file used for SSL verification


### Install the extension in PostgreSQL

1. Add `pg_tde` to `shared_preload_libraries`. 

   The recommended way to modify PostgreSQL configuration file is using the [ALTER SYSTEM :octicons-external-link-16:](https://www.postgresql.org/docs/15/sql-altersystem.html) command. [Connect to psql](connect.md) and use the following command:

    ```sql
    ALTER SYSTEM SET shared_preload_libraries = 'pg_tde';
    ```

2. Start or restart the `postgresql` instance to enable `pg_tde`. Use the following command for restart:


    === ":material-debian: On Debian and Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo systemctl restart postgresql.service
         ```


    === ":material-redhat: On Red Hat Enterprise Linux and derivatives"

         ```{.bash data-prompt="$"}
         $ sudo systemctl restart postgresql-{{pgversion}}
         ```

3. Install the extension in your PostgreSQL using the CREATE EXTENSION command. [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command. You must have the privileges of a superuser or a database owner to use this command. Connect to `psql` as a superuser for a database and run the following command:

    ```sql
    CREATE EXTENSION pg_tde;
    ```
    
    By default, the `pg_tde` extension is created for the currently used database. To enable data encryption in other databases, you must explicitly run the `CREATE EXTENSION` command against them. 

    !!! tip

        You can have the `pg_tde` extension automatically enabled for every newly created database. Modify the template `template1` database as follows: 

        ```
        psql -d template1 -c 'CREATE EXTENSION pg_tde;'
        ```

    After you enabled `pg_tde`, the [access method :octicons-external-link-16:](https://www.postgresql.org/docs/current/tableam.html) `pg_tde` is created for that database. 

### Key configuration

1. Set up a key provider for for the database where you have enabled the extension

   ```sql
   SELECT pg_tde_add_key_provider_vault_v2('provider-name',:'secret_token','url','mount','ca_path');
   ``` 

   where: 

   * `url` is the URL of the Vault server
   * `mount` is the mount point where the keyring should store the keys
   * `secret_token` is an access token with read and write access to the above mount point
   * [optional] `ca_path` is the path of the CA file used for SSL verification

2.  Add a master key

    ```sql
    SELECT pg_tde_set_master_key('name-of-the-master-key', 'provider-name');
    ```

## Usage

To check if the data is encrypted, do the following:

1. Create a table for the database where you have enabled `pg_tde` using the `pg_tde` access method:

    ```sql
    CREATE TABLE my_encrypted_table (
    id SERIAL PRIMARY KEY,
    sensitive_data TEXT
    ) USING pg_tde;
    ```

2. Insert some data ito it:

    ```sql
    INSERT INTO my_encrypted_table (sensitive_data)
    VALUES ('Sensitive data 1'), ('Sensitive data 2'), ('Sensitive data 3');
    ```

3. Check if the data is encrypted:

    ```sql
    SELECT pg_tde_is_encrypted('my_encrypted_table');
    ```

    The function returns `t` if the table is encrypted and `f` - if not.