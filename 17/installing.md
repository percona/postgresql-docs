> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/17/llms.txt).

# Installation overview

Percona Distribution for PostgreSQL packages PostgreSQL together with a curated set of open source extensions and tools that are tested to work together reliably.

This section explains how to install Percona Distribution for PostgreSQL on supported platforms.

Choose the installation method that best fits your environment:

- Package manager, **recommended** for most Linux systems
- Docker, for quick evaluations or development
- Kubernetes, for production Kubernetes environments
- Tarballs, manual installation for custom environments (**not recommended** for mission-critical environments)

**Package manager**

Percona provides installation packages in `DEB` and `RPM` format for 64-bit Linux distributions. See the [Percona Software and Platform Lifecycle page](https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql) for the full list of supported platforms and versions.

If you are on Debian or Ubuntu, use `apt` for installation.

If you are on Red Hat Enterprise Linux or compatible derivatives, use `yum`.

[Install via apt](https://docs.percona.com/postgresql/17/apt.html) [Install via yum](https://docs.percona.com/postgresql/17/yum.html)

**Docker**

Run Percona Distribution for PostgreSQL in a Docker container for quick evaluation or development.

Check below to get access to a detailed step-by-step guide.

[Run in Docker](https://docs.percona.com/postgresql/17/docker.html)

**Kubernetes**

Use the Percona Operator for Kubernetes to deploy and manage PostgreSQL clusters on Kubernetes.

Check below to get access to a detailed step-by-step guide.

[Get started with Percona Operator](https://docs.percona.com/percona-operator-for-postgresql/2.0/quickstart.html)

**Tar download (not recommended)**

Installing the package is the **recommended** method for a safe, secure, and reliable setup. If using this method is not an option, refer to the link below for step-by-step instructions on installing from tarballs using the provided download links.

In this scenario, you must ensure that all dependencies are met. Failure to do so may result in errors or crashes.

Note

This method is **not recommended** for mission-critical environments.

[Install from tarballs](https://docs.percona.com/postgresql/17/tarball.html)
