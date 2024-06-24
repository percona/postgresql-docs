# Percona Distribution for PostgreSQL 16 Documentation

 Percona Distribution for PostgreSQL is a suite of open source software, tools and services required to deploy and maintain a reliable production cluster for PostgreSQL. It includes native PostgreSQL server, enhanced with extensions from open source community that are certified and tested to work together for high availability, backups, security, and monitoring that help ensure the cluster's peak performance. 
 
 Part of the solution, Percona Operator for PostgreSQL, makes it easy to orchestrate the cluster reliably and repeatably in Kubernetes.

[What's included in Percona Distribution for PostgreSQL? :material-arrow-right:](extensions.md){.md-button}

## What’s in it for you?

- No vendor lock in - all components of Percona Distribution for PostgreSQL are fully open source
- No guesswork on finding the right version of a component – they all undergo thorough testing to ensure compatibility
- Freely available reference architectures for solutions like high-availability, backups and disaster recovery 
- Spatial data handling support via PostGIS
- Monitoring of the database health, performance and infrastructure usage via open source [Percona Management and Monitoring :octicons-link-external-16:](https://www.percona.com/doc/percona-monitoring-and-management/2.x/index.html) with PostgreSQL-specific dashboards
- Run PostgreSQL on Kubernetes using open source [Percona Operator for PostgreSQL:octicons-link-external-16:](https://docs.percona.com/percona-operator-for-postgresql/2.0/index.html). It not only automates deployment and management of PostgreSQL clusters on Kubernetes, but also includes enterprise-ready features for high-availability, backup and restore, replication, logging, and more 

<div data-grid markdown><div data-banner markdown>

## :material-progress-download: Installation guides { .title }

Get started quickly with the step-by-step installation instructions.

[Quickstart guides :material-arrow-right:](installing.md){ .md-button }

</div><div data-banner markdown>

### :fontawesome-solid-gears: Solutions { .title }

Check our solutions to build the database infrastructure that meets the requirements of your organization - be it high-availability, disaster recovery or spatial data handling.

[Solutions :material-arrow-right:](solutions.md){ .md-button }

</div><div data-banner markdown>

### :material-frequently-asked-questions: Troubleshooting and FAQ { .title }

Our comprehensive resources will help you overcome challenges, from everyday issues to specific doubts.

[Troubleshooting :material-arrow-right:](troubleshooting.md){.md-button}

</div><div data-banner markdown>

### :loudspeaker: What's new? { .title }

Learn about the releases and changes in the Distribution.

[Release notes :material-arrow-right:](release-notes.md){.md-button}
</div>
</div>

* [Patroni](https://patroni.readthedocs.io/en/latest/) is an HA (High Availability) solution for PostgreSQL.

* [pgaudit](https://www.pgaudit.org/) provides detailed session or object
audit logging via the standard PostgreSQL logging facility

* [pgaudit set_user](https://github.com/pgaudit/set_user) - The `set_user` part of `pgAudit` extension provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks.

* [pgBackRest](https://pgbackrest.org/) is a backup and restore solution for
PostgreSQL

* [pgBadger](https://github.com/darold/pgbadger) - a fast PostgreSQL Log Analyzer.

* [PgBouncer](https://www.pgbouncer.org/) - a lightweight connection pooler for PostgreSQL

* [pg_gather](https://github.com/jobinau/pg_gather) - an SQL script to assess the health of PostgreSQL cluster by gathering performance and configuration data from PostgreSQL databases.

* [pgpool2](https://www.pgpool.net/mediawiki/index.php/Main_Page) - a middleware between PostgreSQL server and client for high availability, connection pooling and load balancing.

* [pg_repack](https://github.com/reorg/pg_repack) rebuilds
PostgreSQL database objects

* [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) collects and aggregates statistics for PostgreSQL and provides histogram information.

* [PostGIS](http://postgis.net/) allows storing and manipulating spacial data in PostgreSQL.

* [wal2json](https://github.com/eulerto/wal2json) - a PostgreSQL logical decoding JSON output plugin.

* A collection of [additional PostgreSQL contrib extensions](https://www.postgresql.org/docs/{{pgversion}}/contrib.html)



