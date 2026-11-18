> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/18/llms.txt).

# Percona Distribution for PostgreSQL 18.4.2 (2026-07-06)

Percona Distribution for PostgreSQL is a solution that includes PostgreSQL server and the collection of tools from PostgreSQL community. These tools are tested to work together and serve to assist you in deploying and managing PostgreSQL.

The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Observability, Spatial data handling, Performance and Scalability, and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 18.4.2 - a binary-compatible, open source drop-in replacement of [PostgreSQL Community 18.4](https://www.postgresql.org/docs/18/release-18-4.html).

## Release Highlights

Percona Distribution for PostgreSQL 18.4.2 is an out-of-cycle maintenance release that addresses an issue where TimescaleDB and Citus were not compilable with earlier Percona Server for PostgreSQL versions, and fixes high-severity CVEs for which fixes were available.

This release also updates bundled components, including `pg_tde` 2.2.1, and refreshes Docker images with fixes for high-severity CVEs where available.

Warning

Percona Server for PostgreSQL 18.4.2 and `pg_tde` 2.2.1 are only supported together. Combining either with an earlier version of the other is not supported.

To upgrade from an earlier version of Percona Distribution for PostgreSQL, follow the steps in [Upgrading Percona Distribution for PostgreSQL](https://docs.percona.com/postgresql/18/major-upgrade.html).

### Docker image updates

Docker images have been rebuilt to address high-severity CVEs where fixes were available.

## Known Issues

### For minor & major upgrades (RHEL only)

During an upgrade on RHEL, you may encounter the following error:

```
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

## Component updates

The following bundled components have been updated in this release:

| Component | Version |
| --------- | ------- |
| pg_tde    | 2.2.1   |
| PostGIS   | 3.5.7   |
| pgVector  | 0.8.3   |
| pgpool    | 4.7.2   |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/18/libpq.html) library. It contains a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.
