# Percona Server for PostgreSQL

Percona Server for PostgreSQL is a binary-compatible, open source drop-in replacement for PostgreSQL {{pgversion}}. It functions identically to upstream PostgreSQL, allowing you to [migrate](migration.md) seamlessly between the two.

In addition to upstream functionality, Percona Server includes enhancements that enable advanced extension capabilities.

## Enhancements

* Storage Manager (SMGR) API exposure, which allows PostgreSQL extensions to integrate custom storage managers. This change was inspired by the following [patchset :octicons-link-external-16:](https://www.postgresql.org/message-id/flat/CAJ7c6TOqqrzjYsU6LgDkcJ0yVgzdkx2juJjgAjzP2jPOpZ1qUA%40mail.gmail.com#8e68cfc57fcac14c8e24b00b41e61baf) introduced to the community.
* WAL Read/Write API exposure, which allows extensions to hook into WAL read and write operations.

These enhancements serve as the foundation for Percona-authored extensions, such as [`pg_tde`](https://docs.percona.com/pg-tde/index.html), which enables data-at-rest encryption.

These changes do not affect existing use cases and PostgreSQL behavior. They enable additional encryption features, such as index-level and Write-Ahead Logging (WAL) encryption, through the [`pg_tde` :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html) extension.

Percona Server and the upstream PostgreSQL operate identically, making migrations between the two straightforward.

For details about available extensions, see the [Percona-authored extensions topic](percona-ext.md).

For a broader overview of integrated tooling and deployment guidance, start with the [Percona Distribution for PostgreSQL Quickstart guide](quick-start.md).

!!! note

    The PostgreSQL Compatibility Index [(PCI)](https://pgscorecard.com/) test suite reported **100% compatibility**. PCI validates behavioral equivalence by running a suite of compatibility checks against upstream PostgreSQL.

    These results were obtained using [Percona Server for PostgreSQL 17.6.1 :octicons-link-external-16:](https://docs.percona.com/postgresql/17/index.html). [View the PCI test results here :octicons-link-external-16:](https://github.com/secp256k1-sha256/postgres-compatibility-index/blob/main/postgres-compatibility-index/outputs/Percona.json).
