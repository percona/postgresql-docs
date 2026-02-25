# Quickstart guide

In this guide you will learn to install Percona Distribution for PostgreSQL with tested open source extensions and tooling designed to work together reliably on Debian and RHEL. This guide quickly gets you up and running with:

* Install Percona Distribution for PostgreSQL using a Package Manager
* Connect to PostgreSQL using the `psql` interactive terminal
* Interact with PostgreSQL with basic commands
* Manipulate data in PostgreSQL

## Preconditions

Install `curl` for [Telemetry](telemetry.md), this is optional.

    ```{.bash data-prompt="$"}
    $ sudo apt install curl
    ```

## Install on Debian / Ubuntu (APT) {.power-number}

1. Fetch the `percona-release` package:

    ```{.bash data-prompt="$"}
    wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
    sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
    ```

2. Enable the repository and install the package:

    ```{.bash data-prompt="$"}
    sudo percona-release setup ppg-18
    sudo apt install percona-postgresql-18
    ```

    The installation process automatically initializes and starts the default database.

3. Switch to a postgres user and open the psql interactive terminal:

    ```{.bash data-prompt="$"}
    sudo su postgres
    psql
    ```

4. Create a database and make a table in the database:

    ```{.bash data-prompt="$"}
    CREATE DATABASE test;
    CREATE TABLE customers (first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100));
    ```

5.  Insert data in the customers table and query the data insertion:

    ```{.bash data-prompt="$"}
    INSERT INTO customers (first_name, last_name, email) VALUES ('John', 'Doe', 'john.doe@example.com');
    SELECT * FROM customers;
    ```

Congratulations! You have installed Percona Distribution for PostgreSQL and created your first database. For detailed installation steps and further instructions, see the [Install Percona Distribution for PostgreSQL on Debian and Ubuntu](apt.md).

## Install on RHEL / Rocky / Alma (YUM)

## Install Percona Distribution for PostgreSQL

You can select from multiple easy-to-follow installation options, however **we strongly recommend using a Package Manager** for a convenient and quick way to try the software first.

=== ":octicons-terminal-16: Package manager"

    Percona provides installation packages in `DEB` and `RPM` format for 64-bit Linux distributions. Find the full list of supported platforms and versions on the [Percona Software and Platform Lifecycle page :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql).

    If you are on Debian or Ubuntu, use `apt` for installation.

    If you are on Red Hat Enterprise Linux or compatible derivatives, use `yum`.

    [Install via apt :material-arrow-right:](apt.md){.md-button}
    [Install via yum :material-arrow-right:](yum.md){.md-button}

=== ":simple-docker: Docker"

    Get our image from Docker Hub and spin up a cluster on a Docker container for quick evaluation.

    Check below to get access to a detailed step-by-step guide.
    
    [Run in Docker :material-arrow-right:](docker.md){.md-button}

=== ":simple-kubernetes: Kubernetes"

    **Percona Operator for Kubernetes** is a controller introduced to simplify complex deployments that require meticulous and secure database expertise.

    Check below to get access to a detailed step-by-step guide.

    [Get started with Percona Operator :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/quickstart.html){.md-button}

=== ":octicons-download-16: Tar download (not recommended)"

    If installing the package (the **recommended** method for a safe, secure, and reliable setup) is not an option, refer to the link below for step-by-step instructions on installing from tarballs using the provided download links.

    In this scenario, you must ensure that all dependencies are met. Failure to do so may result in errors or crashes.
    
    !!! note 

        This method is **not recommended** for mission-critical environments.
    [Install from tarballs :material-arrow-right:](tarball.md){.md-button}
