# Minor Upgrade of Percona Distribution for PostgreSQL

Minor releases of PostgreSQL include bug fixes and feature enhancements. We recommend that you keep your Percona Distribution for PostgreSQL updated to the latest minor version.

Though minor upgrades do not change the behavior, we recommend you to back up your data first, in order to be on the safe side.

Minor upgrade of Percona Distribution for PostgreSQL includes the following steps:


1. Stopping the `postgresql` cluster;


2. Installing new version packages;


3. Restarting the `postgresql` cluster.

!!! note

    These steps apply if you installed Percona Distribution for PostgreSQL from the Major Release repository. In this case, you are always upgraded to the latest available release.

    If you installed Percona Distribution for PostgreSQL from the Minor Release repository, you will need to enable a new version repository to upgrade.

    For more information about Percona repositories, refer to [Installing Percona Distribution for PostgreSQL](installing.md).

  Before the upgrade, update the **percona-release** utility to the latest version. This is required to install the new version packages of Percona Distribution for PostgreSQL. Refer to [Percona Software Repositories Documentation](https://www.percona.com/doc/percona-repo-config/percona-release.html#updating-percona-release-to-the-latest-version) for update instructions.

!!! important

    Run all commands as root or via **sudo**.

1. Stop the `postgresql` service.


    * On Debian / Ubuntu:

      ```
      $ sudo systemctl stop postgresql.service
      ```


    * On Red Hat Enterprise Linux / CentOS:

      ```
      $ sudo systemctl stop postgresql-12
      ```


2. Install new version packages. See [Installing Percona Distribution for PostgreSQL](installing.md).


3. Restart the `postgresql` service.


    * On Debian / Ubuntu:

      ```
      $ sudo systemctl start postgresql.service
      ```


    * On Red Hat Enterprise Linux / CentOS:

      ```
      $ sudo systemctl start postgresql-12
      ```

If you wish to upgrade Percona Distribution for PostgreSQL to the major version, refer to [Upgrading Percona Distribution for PostgreSQL from 11 to 12](major-upgrade.md).
