# Installation overview

Percona Distribution for PostgreSQL packages PostgreSQL together with a curated set of open source extensions and tools that are tested to work together reliably.

This section explains how to install Percona Distribution for PostgreSQL on supported platforms.

Choose the installation method that best fits your environment:

- Package manager, **recommended** for most Linux systems  
- Docker, for quick evaluations or development  
- Kubernetes, for production Kubernetes environments  
- Tarballs, manual installation for custom environments (**not recommended** for mission-critical environments)

=== ":octicons-terminal-16: Package manager"

    Percona provides installation packages in `DEB` and `RPM` format for 64-bit Linux distributions. See the [Percona Software and Platform Lifecycle page :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql) for the full list of supported platforms and versions.

    If you are on Debian or Ubuntu, use `apt` for installation.

    If you are on Red Hat Enterprise Linux or compatible derivatives, use `yum`.

    [Install via apt :material-arrow-right:](apt.md){.md-button}
    [Install via yum :material-arrow-right:](yum.md){.md-button}

=== ":simple-docker: Docker"

    Run Percona Distribution for PostgreSQL in a Docker container for quick evaluation or development.

    Check below to get access to a detailed step-by-step guide.
    
    [Run in Docker :material-arrow-right:](docker/docker.md){.md-button}

=== ":simple-kubernetes: Kubernetes"

    Use the Percona Operator for Kubernetes to deploy and manage PostgreSQL clusters on Kubernetes.

    Check below to get access to a detailed step-by-step guide.

    [Get started with Percona Operator :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/quickstart.html){.md-button}

=== ":octicons-download-16: Tar download (not recommended)"

    Installing the package is the **recommended** method for a safe, secure, and reliable setup. If using this method is not an option, refer to the link below for step-by-step instructions on installing from tarballs using the provided download links.

    In this scenario, you must ensure that all dependencies are met. Failure to do so may result in errors or crashes.
    
    !!! note 

        This method is **not recommended** for mission-critical environments.

     [Install from tarballs :material-arrow-right:](tarball.md){.md-button}
