# Quickstart guide

Percona Distribution for PostgreSQL is the Percona server for PostgreSQL with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. [Read more](index.md).

This document aims to guide database application developers and DevOps engineers in getting started with Percona Distribution for PostgreSQL. Upon completion of this guide, you’ll have Percona Distribution for PostgreSQL installed and operational, and you’ll be able to:

* Connect to PostgreSQL using the `psql` interactive terminal 
* Interact with PostgreSQL with basic psql commands
* Manipulate data in PostgreSQL 
* Understand the next steps you can take as a database application developer or administrator to expand your knowledge of Percona Distribution for PostgreSQL

## Install Percona Distribution for PostgreSQL

You can select from multiple easy-to-follow installation options, but **we recommend using a Package Manager** for a convenient and quick way to try the software first.

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

=== ":octicons-download-16: Manual download"

    If you need to install Percona Distribution for PostgreSQL offline or as a non-superuser, check out the link below for a step-by-step guide and get access to the downloads directory.

    Note that for this scenario you must make sure that all dependencies are satisfied.

    [Install from tarballs :material-arrow-right:](tarball.md){.md-button}





