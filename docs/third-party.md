# Third-party components

Percona Distribution for PostgreSQL is supplied with the set of third-party open source components and tools that provide additional functionality such as high-availability or disaster recovery, without the need of modifying PostgreSQL core code. These components are included in the Percona Distribution for PostgreSQL repository and are tested to work together.


| Name | Superuser privileges | Description |
|------|---------------------|-------------|
| [etcd](https://etcd.io/)| Required | A distributed, reliable key-value store for setting up high available Patroni clusters |
| [HAProxy](http://www.haproxy.org/) | Required | A high-availability and load-balancing solution |
| [Patroni](https://patroni.readthedocs.io/en/latest/) | Required | An HA (High Availability) solution for PostgreSQL |
| [pgAudit](https://www.pgaudit.org/) | Required | Provides detailed session or object audit logging via the standard PostgreSQL logging facility |
| [pgAudit set_user](https://github.com/pgaudit/set_user) | Required | The `set_user` part of `pgAudit` extension provides an additional layer of logging and control when unprivileged users must escalate themselves to superuser or object owner roles in order to perform needed maintenance tasks |
| [pgBackRest](https://pgbackrest.org/) | Required | A backup and restore solution for PostgreSQL |
| [pgBadger](https://github.com/darold/pgbadger) | Required | A fast PostgreSQL Log Analyzer |
| [PgBouncer](https://www.pgbouncer.org/) | Required | A lightweight connection pooler for PostgreSQL |
| [pg_gather](https://github.com/jobinau/pg_gather) | Required | An SQL script to assess the health of PostgreSQL cluster by gathering performance and configuration data from PostgreSQL databases |
| [pgpool2](https://www.pgpool.net/mediawiki/index.php/Main_Page) | Required | A middleware between PostgreSQL server and client for high availability, connection pooling and load balancing |
| [pg_repack](https://github.com/reorg/pg_repack) | Required | Rebuilds PostgreSQL database objects |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | Required | Collects and aggregates statistics for PostgreSQL and provides histogram information |
| [PostGIS](http://postgis.net/) | Required | Allows storing and manipulating spacial data in PostgreSQL |
|[pgvector :octicons-link-external-16:](https://github.com/pgvector/pgvector)| Required | An  extension that enables you to use PostgreSQL as a vector database|
|[wal2json](https://github.com/eulerto/wal2json)|Required| A PostgreSQL logical decoding JSON output plugin.|