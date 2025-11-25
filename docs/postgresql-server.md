# Percona Server for PostgreSQL

Percona Server for PostgreSQL is a binary-compatible, open source drop-in replacement for PostgreSQL 17. It introduces additional features on top of the upstream server, including:

* Storage Manager (SMGR) API Exposure: Allows PostgreSQL extensions to integrate custom storage managers. This change was inspired by the [patchset :octicons-link-external-16:](https://www.postgresql.org/message-id/flat/CAJ7c6TOqqrzjYsU6LgDkcJ0yVgzdkx2juJjgAjzP2jPOpZ1qUA%40mail.gmail.com#8e68cfc57fcac14c8e24b00b41e61baf) introduced to the community.
* WAL Read/Write API Exposure: Allows extensions to hook into WAL read and write functions.

These changes do not affect existing use cases and PostgreSQL behavior. They enable additional encryption features, such as index-level and Write-Ahead Logging (WAL) encryption, through the [`pg_tde` :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html) extension.

Percona Server and the upstream PostgreSQL operate identically, making migrations between the two straightforward.

[Get started :material-arrow-right:](installing.md){.md-button}

!!! note

    The PostgreSQL Compatibility Index [(PCI)](https://pgscorecard.com/) test suite reported **100% compatibility**. PCI validates behavioral equivalence by running a suite of compatibility checks against upstream PostgreSQL.

    These results were obtained using [Percona Server for PostgreSQL 17.6.1 :octicons-link-external-16:](https://docs.percona.com/postgresql/17/index.html). [View the PCI test results here :octicons-link-external-16:](https://github.com/secp256k1-sha256/postgres-compatibility-index/blob/main/postgres-compatibility-index/outputs/Percona.json).
