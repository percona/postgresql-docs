> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/19/llms.txt).

# Percona Server for PostgreSQL

Percona Server for PostgreSQL is a binary-compatible, open source drop-in replacement for PostgreSQL 19. It functions identically to upstream PostgreSQL, allowing you to [migrate](https://docs.percona.com/postgresql/19/migration.html) seamlessly between the two.

In addition to upstream functionality, Percona Server includes enhancements that enable advanced extension capabilities.

## Enhancements

- Storage Manager (SMGR) API exposure, which allows PostgreSQL extensions to integrate custom storage managers. This change was inspired by the following [patchset](https://www.postgresql.org/message-id/flat/CAJ7c6TOqqrzjYsU6LgDkcJ0yVgzdkx2juJjgAjzP2jPOpZ1qUA%40mail.gmail.com#8e68cfc57fcac14c8e24b00b41e61baf) introduced to the community.
- WAL Read/Write API exposure, which allows extensions to hook into WAL read and write operations.

These enhancements serve as the foundation for Percona-authored extensions, such as [`pg_tde`](https://docs.percona.com/pg-tde/index.html), which enables data-at-rest encryption.

For details about available extensions, see the [Percona-authored extensions topic](https://docs.percona.com/postgresql/19/percona-ext.html).

For a broader overview of integrated tooling and deployment guidance, start with the [Percona Distribution for PostgreSQL Quickstart guide](https://docs.percona.com/postgresql/19/quick-start.html).
