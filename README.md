# Percona Distribution for PostgreSQL documentation.

Welcome to Percona Distribution for PostgreSQL documentation!

## Overview

Percona Distribution for PostgreSQL is a collection of tools to assist you in managing your PostgreSQL database system. It includes Percona Server for PostgreSQL and a selection of extensions that enable solving essential practical tasks efficiently.

Percona Server for PostgreSQL is an open source binary-compatible drop-in replacement for PostgreSQL Community. Percona Server for PostgreSQL introduces additional features to the upstream server, including:

* Storage Manager (SMGR) API Exposure: Allows PostgreSQL extensions to integrate custom storage managers. This change was inspired by the [patchset](https://www.postgresql.org/message-id/flat/CAJ7c6TOqqrzjYsU6LgDkcJ0yVgzdkx2juJjgAjzP2jPOpZ1qUA%40mail.gmail.com#8e68cfc57fcac14c8e24b00b41e61baf) introduced to the community.
* WAL Read/Write API Exposure to hook into WAL read and write functions.

Percona Server and upstream PostgreSQL function identically enabling you to migrate from one to another. 
 
This repository contains the source files for [Percona Distribution for PostgreSQL documentation](https://www.percona.com/doc/postgresql/17/index.html). The documentation is written in [Markdown](https://www.markdownguide.org/) markup language and is created using [MkDocs Documentation Generator](https://www.mkdocs.org/). 

## Contributing

We welcome all contributions and are always looking for new members that are as dedicated to serving the community as we are. You can reach out to us using our [forums ](https://forums.percona.com/c/postgresql/25) and [Jira issue tracker ](https://jira.percona.com/projects/DISTPG/issues/DISTPG-16?filter=allopenissues). 

For how to contribute to documentation, read the [Contributing guide ](https://github.com/percona/postgresql-docs/blob/16/CONTRIBUTING.md).

## License

Percona Distribution for PostgreSQL documentation is licensed under the [PostgreSQL license ](https://opensource.org/licenses/postgresql).