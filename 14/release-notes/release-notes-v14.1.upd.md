> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/14/llms.txt).

# Percona Distribution for PostgreSQL 14.1 Update (2021-12-02)

|               |                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| Date:         | December 2, 2021                                                                                             |
| Installation: | [Installing Percona Distribution for PostgreSQL](https://www.percona.com/doc/postgresql/14/installing.html#) |

Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL installs PostgreSQL and complements it by a selection of extensions that enable solving essential practical tasks efficiently.

This update of Percona Distribution for PostgreSQL fixes the inability of a user to upgrade the `postgresql-common` package during the major upgrade to version 14.1 on DEB-based systems.

## Bugs Fixed

- [DISTPG-358](https://jira.percona.com/browse/DISTPG-358): “Device or resource busy” error during the major upgrade of PostgreSQL on Ubuntu
