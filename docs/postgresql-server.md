# Percona Server for PostgreSQL

Percona Server for PostgreSQL is a binary-compatible, drop-in replacement for PostgreSQL 17. It introduces additional features to the upstream server, including:

* Storage Manager (SMGR) API Exposure: Allows PostgreSQL extensions to integrate custom storage managers. This change was inspired by the [patchset](https://www.postgresql.org/message-id/flat/CAJ7c6TOqqrzjYsU6LgDkcJ0yVgzdkx2juJjgAjzP2jPOpZ1qUA%40mail.gmail.com#8e68cfc57fcac14c8e24b00b41e61baf) introduced to the community.
* WAL Read/Write API Exposure to hook into WAL read and write functions.

These modifications are the preparations to provide index-level and WAL encryption of indexes via the [`pg_tde` :octicons-link-external-16:](https://percona-lab.github.io/pg_tde/main/) extension. These encryption features are still under active development and are planned for future releases.

Percona Server and upstream PostgreSQL function identically enabling you to migrate from one to another. 

[Get started :material-arrow-right:](installing.md){.md-button}