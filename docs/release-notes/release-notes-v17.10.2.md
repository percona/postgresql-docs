# Percona Distribution for PostgreSQL 17.10.2 ({{date.17_10_2}})

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 17.10.2 - a binary-compatible, open source drop-in replacement of [PostgreSQL Community 17.10](https://www.postgresql.org/docs/17/release-17-10.html).

## Release Highlights

Percona Distribution for PostgreSQL 17.10.2 is an out-of-cycle maintenance release that updates bundled components, including `pg_tde` 2.2.1, and refreshes Docker images with fixes for high-severity CVEs where available.

!!! note
    `pg_tde` 2.2.1 is not compatible with Percona Distribution for PostgreSQL versions earlier than 17.10.

To upgrade from an earlier version of Percona Distribution for PostgreSQL, follow the steps in [Upgrading Percona Distribution for PostgreSQL](../major-upgrade.md).

### Docker image updates

Docker images have been rebuilt to address high-severity CVEs where fixes were available.

## Known Issues

### For minor & major upgrades (RHEL only)

During an upgrade on RHEL, you may encounter the following error:

```bash
Unknown Error occurred: Transaction test error:
  file /usr/share/postgresql-common/server/postgresql.mk from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
  file /usr/share/postgresql-common/t/040_upgrade.t from install of percona-postgresql-common conflicts with file from package percona-postgresql-common-dev
```

To resolve this, remove the `percona-postgresql-common-dev` package and reinstall it with the new intended upgraded PPG/PSP server.

## Component updates

The following bundled components have been updated in this release:

| Component | Version |
|-----------|---------|
| pg_tde | 2.2.1 |
| PostGIS | 3.5.7 |
| pgVector | 0.8.3 |
| pgpool | 4.7.2 |

For Red Hat Enterprise Linux 8 and compatible derivatives, Percona Distribution for PostgreSQL also includes the supplemental `python3-etcd` 0.4.5 packages, which are used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.
