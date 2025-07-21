# Percona Distribution for PostgreSQL 13.16 ({{date.13_16}})

[Installation](installing.md){.md-button}

Percona Distribution for PostgreSQL is a solution with the collection of tools from PostgreSQL community that are tested to work together and serve to assist you in deploying and managing PostgreSQL. The aim of Percona Distribution for PostgreSQL is to address the operational issues like High-Availability, Disaster Recovery, Security, Spatial data handling, Observability, Performance and Scalability and others that enterprises are facing.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 13.16](https://www.postgresql.org/docs/13/release-13-15.html).

## Release Highlights

* This release of Percona Distribution for PostgreSQL fixes security vulnerability [CVE-2024-7348](https://nvd.nist.gov/vuln/detail/CVE-2024-7348). 

* Percona Distribution for PostgreSQL packages and tarballs are now also available for ARM64 architectures. now includes the packages. Thus, users can not only run Percona Distribution for PostgreSQL in Docker containers on ARM-based workstations but also install the packages on those workstations. The ARM64 packages and tarballs are available for the following operating systems:

    * Red Hat Enterprise Linux 8 and compatible derivatives
    * Red Hat Enterprise Linux 9 and compatible derivatives
    * Ubuntu 20.04 (Focal Fossa)
    * Ubuntu 22.04 (Jammy Jellyfish)
    * Ubuntu 24.04 (Noble Numbat)
    * Debian 11
    * Debian 12

* Percona Distribution for PostgreSQL includes the enhanced telemetry feature and provides comprehensive information about how telemetry works, its components and metrics as well as updated methods how to disable telemetry. Read more in [Telemetry and data collection](telemetry.md)
* Percona Distribution for PostgreSQL includes pg_stat_monitor 2.1.0 that provides the ability to [disable the application name tracking for a query](https://docs.percona.com/pg-stat-monitor/configuration.html#pg_stat_monitorpgsm_track_application_names). This way you can optimize pg_stat_monitor's performance impact. 


----------------------------------------------------------------------------

The following is the list of extensions available in Percona Distribution for PostgreSQL.

| Extension           | Version        | Description                  |
| ------------------- | -------------- | ---------------------------- |
| [etcd](https://etcd.io/)| 3.5.15 | A distributed, reliable key-value store for setting up high available Patroni clusters |
|[HAProxy](http://www.haproxy.org/) | 2.8.10 | a high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | 3.3.2 | a HA (High Availability) solution for PostgreSQL |
| [PgAudit](https://www.pgaudit.org/)             | 1.5.2   | provides detailed session or object audit logging via the standard logging facility provided by PostgreSQL                |
| [pgAudit set_user](https://github.com/pgaudit/set_user)| 4.0.1 | provides an additional layer of logging and control when unprivileged users must escalate themselves to superusers or object owner roles to perform needed maintenance tasks.|
| [pgBackRest](https://pgbackrest.org/)           | 2.53    | a backup and restore solution for PostgreSQL       |
|[pgBadger](https://github.com/darold/pgbadger)   | 12.4     | a fast PostgreSQL Log Analyzer.|
|[pgbouncer](https://www.pgbouncer.org/)          |1.23.1    | a lightweight connection pooler for PostgreSQL|
| [pg_gather](https://github.com/jobinau/pg_gather)| v27     | an SQL script for running the diagnostics of the health of PostgreSQL cluster |
| [pgpool2](https://git.postgresql.org/gitweb/?p=pgpool2.git;a=summary) | 4.5.2 | a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.|
| [pg_repack](https://github.com/reorg/pg_repack) | 1.5.0   | rebuilds PostgreSQL database objects           |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor)|{{pgsmversion}} | collects and aggregates statistics for PostgreSQL and provides histogram information.|
| [PostGIS](https://github.com/postgis/postgis) | 3.3.6 | a spatial extension for PostgreSQL.|
| [PostgreSQL Common](https://salsa.debian.org/postgresql/postgresql-common)| 261 | PostgreSQL database-cluster manager. It provides a structure under which multiple versions of PostgreSQL may be installed and/or multiple clusters maintained at one time.|
|[wal2json](https://github.com/eulerto/wal2json)  |2.6       | a PostgreSQL logical decoding JSON output plugin|

Percona Distribution for PostgreSQL on Red Hat Enterprise Linux 8 and compatible derivatives also includes the following packages:

* `llvm` 17.0.6 packages. This fixes compatibility issues with LLVM from upstream.
* supplemental `python3-etcd` packages, which can be used for setting up Patroni clusters. 

                                                      
Percona Distribution for PostgreSQL is also shipped with the [libpq](https://www.postgresql.org/docs/13/libpq.html) library. It contains "a set of
library functions that allow client programs to pass queries to the PostgreSQL
backend server and to receive the results of these queries." 
