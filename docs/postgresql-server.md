# Percona Server for PostgreSQL

Percona Server for PostgreSQL is a binary-compatible, open source drop-in replacement for PostgreSQL 17. It introduces additional features to the upstream server, including:

* Storage Manager (SMGR) API Exposure: Allows PostgreSQL extensions to integrate custom storage managers. This change was inspired by the [patchset](https://www.postgresql.org/message-id/flat/CAJ7c6TOqqrzjYsU6LgDkcJ0yVgzdkx2juJjgAjzP2jPOpZ1qUA%40mail.gmail.com#8e68cfc57fcac14c8e24b00b41e61baf) introduced to the community.
* WAL Read/Write API Exposure to hook into WAL read and write functions.

These modifications have no impact on existing use cases and operation of PostgreSQL. They are required to enable additional encryption capabilities such as index-level and Write-Ahead Logging (WAL) encryption of indexes through the [`pg_tde` :octicons-link-external-16:](https://percona.github.io/pg_tde/main/index.html) extension. These encryption features provided by the `pg_tde` are still under active development and are planned for future releases.

Percona Server and upstream PostgreSQL function identically enabling you to migrate from one to another. 

[Get started :material-arrow-right:](installing.md){.md-button}