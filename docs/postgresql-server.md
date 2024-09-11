# Percona Server for PostgreSQL

Percona Server for PostgreSQL is a binary-compatible, drop-in replacement for PostgreSQL 17. It introduces additional features to the upstream server, including:

* Storage Manager (SMGR) API Exposure: Allows PostgreSQL extensions to integrate custom storage managers. This change was inspired by the [patchset](https://www.postgresql.org/message-id/flat/CAJ7c6TOqqrzjYsU6LgDkcJ0yVgzdkx2juJjgAjzP2jPOpZ1qUA%40mail.gmail.com#8e68cfc57fcac14c8e24b00b41e61baf) introduced to the community.
* WAL Read/Write API Exposure to hook into WAL read and write functions.

These modifications provide index-level and WAL encryption of indexes via the `pg_tde` extension. Note that these encryption features are experimental and under active development.

Percona Server and upstream PostgreSQL function identically enabling you to migrate from one to another. 

However, index-level encryption is available only with Percona Server for PostgreSQL. So if you encrypted indexes, you cannot switch to the upstream PostgreSQL without losing this data. [Learn more about TDE](https://percona-lab.github.io/pg_tde/main/)

[Get started :material-arrow-right:](installing.md){.md-button}