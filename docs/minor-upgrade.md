# Minor Upgrade of Percona Distribution for PostgreSQL

Minor releases of PostgreSQL include bug fixes and feature enhancements. We recommend that you keep your Percona Distribution for PostgreSQL updated to the latest minor version.

Though minor upgrades do not change the behavior, we recommend you to back up your data first, in order to be on the safe side.

Minor upgrade of Percona Distribution for PostgreSQL includes the following steps:

1. Stop the `postgresql` cluster

2. Update `percona-release`
3. Install new version packages

4. Restart the `postgresql` cluster.

!!! note

    These steps apply if you installed Percona Distribution for PostgreSQL from the Major Release repository. In this case, you are always upgraded to the latest available release.

    If you installed Percona Distribution for PostgreSQL from the Minor Release repository, you will need to enable a new version repository to upgrade.

    For more information about Percona repositories, refer to [Installing Percona Distribution for PostgreSQL](installing.md).

## Before you start

1. [Update the `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/updating.html) utility to the latest version. This is required to install the new version packages of Percona Distribution for PostgreSQL.

2. Starting with version 17.2.1, `pg_tde` is part of the Percona Server for PostgreSQL package. If you installed `pg_tde` from its dedicated package, do the following to avoid conflicts during the upgrade:

    * Drop the extension using the `DROP EXTENSION` with `CASCADE` command.

       <i warning>:material-alert: Warning:</i> The use of the `CASCADE` parameter deletes all tables that were created in the database with `pg_tde` enabled and also all dependencies upon the encrypted table (e.g. foreign keys in a non-encrypted table used in the encrypted one).

       ```sql
       DROP EXTENSION pg_tde CASCADE
       ```

    * Uninstall the `percona-postgresql-17-pg-tde` package for Debian/Ubuntu or the `percona-pg_tde_17` package for RHEL and derivatives.

## Procedure

Run **all** commands as root or via **sudo**:
{.power-number}

1. Stop the `postgresql` service.

    === ":material-debian: On Debian / Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql.service
         ```

    === ":material-redhat: On Red Hat Enterprise Linux / derivatives"

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop postgresql-17
         ```

2. [Update `percona-release` to the latest version](https://docs.percona.com/percona-software-repositories/updating.html).

3. Install new version packages. See [Installing Percona Distribution for PostgreSQL](installing.md).

4. Restart the `postgresql` service.

    === ":material-debian: On Debian / Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo systemctl start postgresql.service
         ```

    === ":material-redhat: On Red Hat Enterprise Linux / derivatives"

         ```{.bash data-prompt="$"}
         $ sudo systemctl start postgresql-17
         ```

!!! note "For minor upgrades (RHEL only)"

    During a minor upgrade on RHEL, you may encounter the following error:

    ```
    Unknown Error occurred: Transaction test error:
    file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
    file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
    ```

    To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

If you wish to upgrade Percona Distribution for PostgreSQL to the major version, refer to [Upgrading Percona Distribution for PostgreSQL from 17 to 18](major-upgrade.md).
