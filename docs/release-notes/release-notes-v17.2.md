# Percona Distribution for PostgreSQL 17.2.1 ({{date.17_2}})

--8<-- "release-notes-intro.md"

This release of Percona Distribution for PostgreSQL is based on Percona Server for PostgreSQL 17.2.1 - a binary compatible, open source drop in replacement of [PostgreSQL Community 17.2](https://www.postgresql.org/docs/17/release-17-2.html).

## Release Highlights

* This release includes fixes for [CVE-2024-10978](https://www.postgresql.org/support/security/CVE-2024-10978/) and for certain PostgreSQL extensions that break because they depend on the modified Application Binary Interface (ABI). These regressions were introduced in PostgreSQL 17.1, 16.5, 15.9, 14.14, 13.17, and 12.21. For this reason, the release of Percona Distribution for PostgreSQL 17.1.1 has been skipped.
* Percona Distribution for PostgreSQL includes [`pgvector` :octicons-link-external-16:](https://github.com/pgvector/pgvector) - an open source extension that enables you to use PostgreSQL as a vector database. It brings vector data type and vector operations (mainly similarity search) to PostgreSQL. You can install `pgvector` from repositories, tarballs, and it is also available as a Docker image.
* The new version of `pg_tde` extension features index encryption and the support of storing encryption keys in KMIP-compatible servers. These feature come with the Beta version of the `tde_heap` access method. Learn more in the [pg_tde release notes :octicons-link-external-16:](https://docs.percona.com/pg-tde/release-notes/beta2.html)
* The `pg_tde` extension itself is now a part of the Percona Server for PostgreSQL server package and a Docker image. If you installed the extension before, from its individual package, uninstall it first to avoid conflicts during the upgrade. See the [Minor Upgrade of Percona Distribution for PostgreSQL](../minor-upgrade.md#before-you-start) for details.

   For how to run `pg_tde` in Docker, check the [Enable encryption](../docker.md#enable-encryption) section in the documentation.

*  Percona Distribution for PostgreSQL now statically links `llvmjit.so` library for Red Hat Enterprise Linux 8 and 9 and compatible derivatives. This resolves the conflict between the LLVM version required by Percona Distribution for PostgreSQL and the one supplied with the operating system. This also enables you to use the LLVM modules supplied with the operating system for other software you require.
* Percona Monitoring and Management (PMM) 2.43.2 is now compatible with `pg_stat_monitor` 2.1.0 to monitor PostgreSQL 17.

------------------------------------------------------------------------------


The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [etcd](https://etcd.io/)| 3.5.16 | A distributed, reliable key-value store for setting up high available Patroni clusters |
|[HAProxy :octicons-link-external-16:](http://www.haproxy.org/) | 2.8.11 | a high-availability and load-balancing solution |
| [Patroni :octicons-link-external-16:](https://patroni.readthedocs.io/en/latest/) | 4.0.3 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit :octicons-link-external-16:](https://www.pgaudit.org/)             | 17.0   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user :octicons-link-external-16:](https://github.com/pgaudit/set_user)| 4.1.0 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles in order to perform needed maintenance tasks.|
| [pgBackRest :octicons-link-external-16:](https://pgbackrest.org/)           | 2.54.0    | a backup and restore solution for PostgreSQL       |
|[pgBadger :octicons-link-external-16:](https://github.com/darold/pgbadger)   | 12.4     | a fast PostgreSQL Log Analyzer.|
|[PgBouncer :octicons-link-external-16:](https://www.pgbouncer.org/)          |1.23.1    | a lightweight connection pooler for PostgreSQL|
| [pg_gather :octicons-link-external-16:](https://github.com/jobinau/pg_gather)| v28     | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2 :octicons-link-external-16:](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.5.4 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack :octicons-link-external-16:](https://github.com/reorg/pg_repack) | 1.5.1   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor :octicons-link-external-16:](https://github.com/percona/pg_stat_monitor)|{{pgsmversion}} | collects and aggregates statistics for PostgreSQL and provides histogram information.|
|[pgvector :octicons-link-external-16:](https://github.com/pgvector/pgvector)| v0.8.0 | A vector similarity search for PostgreSQL|
| [PostGIS :octicons-link-external-16:](https://github.com/postgis/postgis) | 3.3.7 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common :octicons-link-external-16:](https://salsa.debian.org/postgresql/postgresql-common)| 265 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[wal2json :octicons-link-external-16:](https://github.com/eulerto/wal2json)  |2.6       | a PostgreSQL logical decoding JSON output plugin|

For Red Hat Enterprise Linux 8 and 9 and compatible derivatives, Percona Distribution for PostgreSQL also includes the following packages:

* `llvm` 17.0.6 packages. This fixes compatibility issues with LLVM from upstream.
* supplemental `python3-etcd` 0.4.5 packages, which can be used for setting up Patroni clusters.

Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/17/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries."
