# Percona Distribution for PostgreSQL 19.0.1 ({{date.19_0_1}})

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 19.0.1 - a binary compatible, open source drop in replacement of [PostgreSQL Community 19.0](https://www.postgresql.org/docs/19/release-19.html).

This release introduces several major enhancements from PostgreSQL 19, such as:

- **`REPACK (CONCURRENTLY)`** to reclaim table bloat and reorder data without blocking reads or writes. `REPACK` replaces `VACUUM FULL` and `CLUSTER`, which remain available for compatibility.
- **Plan stability** with the new `pg_plan_advice` and `pg_stash_advice` extensions, which let you pin or adjust query plans without changing your application.
- **Smarter autovacuum** with parallel index vacuuming (`autovacuum_max_parallel_workers`) and a new scoring system to prioritize tables.
- **Simpler logical replication**: the effective WAL level is raised to `logical` automatically when you create the first logical replication slot, so no server restart is needed. Sequence values can now be replicated too.
- **Read-your-writes consistency on standbys** with the new `WAIT FOR LSN` command.
- **Developer improvements**, including `INSERT ... ON CONFLICT DO SELECT`, `COPY` output in JSON format, and `IGNORE NULLS` for window functions.
- **New monitoring views**: `pg_stat_lock`, `pg_stat_recovery`, and `pg_stat_autovacuum_scores`, plus an `IO` option for `EXPLAIN ANALYZE`.

!!! important "Changes to review before upgrading"

    * **If your cluster uses `pg_tde`**, you **must** use [`pg_tde_upgrade` :octicons-link-external-16:](https://docs.percona.com/pg-tde/command-line-tools/pg-tde-upgrade.html) instead of `pg_upgrade` for the major upgrade to 19. Running `pg_upgrade` on an encrypted cluster is not supported and results in data corruption: the server may start, but queries against encrypted tables fail. See [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md).
    * Just-in-time compilation (JIT) is now disabled by default. Enable it if you run many large analytical queries.
    * RADIUS authentication is no longer supported.
    * A successful `md5` password authentication now produces a warning. `md5` is deprecated, so consider moving to SCRAM authentication.
    * The `io_workers` setting is replaced by `io_min_workers` and `io_max_workers`.

For the complete list of changes, see the [PostgreSQL 19 release notes :octicons-link-external-16:](https://www.postgresql.org/docs/19/release-19.html).

## Release Highlights

This release continues to deliver Percona’s open source value-add components for enterprise use cases, `pg_tde` 2.3.0 for Transparent Data Encryption and more. See the full component list below for details.

!!! note
    `pg_tde` 2.3.0 requires Percona Distribution for PostgreSQL 19.0.1 or later. It is not supported on community PostgreSQL, because it depends on server-side changes that are only available in Percona Server for PostgreSQL.

To upgrade from earlier versions (e.g. Percona Distribution for PostgreSQL 18.x), follow the steps in [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md).

### Server meta-packages are no longer shipped

Starting with this release, Percona Distribution for PostgreSQL no longer ships the following meta-packages:

* `percona-ppg-server-19` (Debian/Ubuntu) and `percona-ppg-server19` (RHEL and derivatives)
* `percona-ppg-server-ha-19` (Debian/Ubuntu) and `percona-ppg-server-ha19` (RHEL and derivatives)

Install the server and the components you need as individual packages instead. See [Install on Debian and Ubuntu](../apt.md) and [Install on RHEL and derivatives](../yum.md) for the package names and commands.

### Tarball updates

The binary tarballs for x86_64 and ARM64 architectures have been updated in this release. The following libraries and components are bundled in tarballs:

- credcheck: 6.0
- etcd: 3.5.35
- haproxy: 2.8.31
- patroni: 4.1.5
- pgaudit: 19.0
- pgaudit_set_user: 4.3.0
- pgBackRest: 2.60.1
- pgbadger: 13.3
- pgbouncer: 1.26.1
- pg_cron: 1.6.8
- pg_gather: 33
- pg_oidc_validator: 1.1.0
- pgpool2: 4.7.3
- pg_repack: 1.5.3
- pg_stat_monitor: 2.4.1
- pg_tde: 2.3.0
- pgvector: 0.8.7
- postgis: 3.7.0
- postgres-common: 295
- wal2json: 2.7

See [Install Percona Distribution for PostgreSQL from binary tarballs](../tarball.md) for the download links.

## Known Issues

### For minor & major upgrades (RHEL only)

During an upgrade on RHEL, you may encounter the following error:

```bash
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

## Supplied third-party extensions

Review each extension’s release notes for What’s new, improvements, or bug fixes.

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension | Version | Description |
| --- | --- | --- |
| [credcheck :octicons-link-external-16:](https://github.com/HexaCluster/credcheck) | 6.0 | Enforces username and password policies during role creation, renaming, and password changes |
| [etcd :octicons-link-external-16:](https://etcd.io/) | 3.5.35 | A distributed, reliable key-value store for setting up highly available Patroni clusters |
| [python-etcd :octicons-link-external-16:](https://python-etcd.readthedocs.io/en/latest/) | 0.4.5 | A Python client library for interacting with etcd |
| [HAProxy :octicons-link-external-16:](https://www.haproxy.org/) | 2.8.31 | A high-availability and load-balancing solution |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) | 4.1.5 | A HA (High Availability) solution for PostgreSQL |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/) | 19.0 | A detailed session or object audit logging via the standard logging facility provided by PostgreSQL |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user) | 4.3.0 | Provides an additional layer of logging and control when unprivileged users must escalate roles for maintenance |
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/) | 2.60.1 | A backup and restore solution for PostgreSQL |
| [pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger) | 13.3 | A fast PostgreSQL log analyzer |
| [PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/) | 1.26.1 | A lightweight connection pooler for PostgreSQL |
| [pg_cron :octicons-link-external-16:](https://github.com/citusdata/pg_cron) | 1.6.8 | A simple cron-based job scheduler for PostgreSQL |
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather) | 33 | An SQL script for running diagnostics on the health of a PostgreSQL cluster |
| [pg_oidc_validator](https://github.com/Percona-Lab/pg_oidc_validator) | 1.1.0 | OAuth validator library for PostgreSQL 19 |
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) | 1.5.3 | Rebuilds PostgreSQL database objects |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | 2.4.1 | Collects and aggregates statistics for PostgreSQL and provides histogram information |
| [pg_tde :octicons-link-external-16:](https://github.com/percona/pg_tde) | 2.3.0 | A PostgreSQL extension that provides Transparent Data Encryption (TDE) to protect data at rest |
| [pgvector](https://github.com/pgvector/pgvector) | 0.8.7 | A vector similarity search extension for PostgreSQL |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.7.3 | A middleware between PostgreSQL server and client for high availability, connection pooling, and load balancing |
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis) | 3.7.0 | A spatial extension for PostgreSQL |
| [PostgreSQL Commons :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common) | 295 | PostgreSQL database-cluster manager. Supports multiple PostgreSQL versions and clusters simultaneously |
| [wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json) | 2.7 | A PostgreSQL logical decoding JSON output plugin |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/19/libpq.html) library. It contains "a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries."
