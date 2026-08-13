# Percona-authored extensions

<div data-grid markdown>
<div data-banner markdown>

### :octicons-graph-16: pg_stat_monitor 

A query performance monitoring tool for PostgreSQL that brings more insight and details around query performance, planning statistics and metadata. It improves observability, enabling users to debug and tune query performance with precision.

[pg_stat_monitor documentation :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/index.html){.md-button}
</div>

<div data-banner markdown>

### :material-file-key-outline: pg_tde

An open-source extension designed to enhance PostgreSQL’s security by encrypting data files on disk. The encryption is transparent for users allowing them to access and manipulate the data and not to worry about the encryption process.

[pg_tde documentation :octicons-link-external-16:](https://percona.github.io/pg_tde/main/index.html){.md-button}

</div>
</div>

## Tech Preview: pg_tde built into Percona Server for PostgreSQL 16

!!! warning "Tech Preview"

    This is a **Tech Preview** feature. Percona doesn't recommend Tech Preview features for production environments. We provide them to give users early access to new functionality and the opportunity to provide feedback while the feature is still under development. There is no commitment to support them long-term, and the feature may change or be removed without notice.

[`pg_tde` :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html) is included natively in Percona Server for PostgreSQL (PSP) 16.15, available as a Tech Preview through a dedicated testing repository and `perconalab` Docker images. See [Tech Preview: PSP 16 testing repository](repo-overview.md#tech-preview-psp-16-testing-repository) for packages, or [Tech Preview: Percona Server for PostgreSQL 16 with pg_tde](docker.md#tech-preview-percona-server-for-postgresql-16-with-pg_tde) for Docker images.

The following component versions are bundled with this Tech Preview:

| Component | Version |
| --------- | ------- |
| `pg_tde` | 2.2.1 |
| `pg_stat_monitor` | 2.3.2 |
| `pgaudit` | 16.1 |
| `pg_repack` | 1.5.3 |
| `pgBackRest` | 2.58.0 |
| `Patroni` | 4.1.3 |
| `pgBadger` | 13.2 |
| `PgBouncer` | 1.25.2 |
| `Pgpool-II` | 4.7.2 |
| `wal2json` | 2.6 |
| `set_user` | 4.2.0 |
| `HAProxy` | 2.8.23 |
| `etcd` | 3.5.30 |
| `pgvector` | 0.8.3 |
| `PostGIS` | 3.5.7 |
| `pg_cron` | 1.6.7 |
| `pg_gather` | 33 |
| `percona-pg-telemetry` | 1.2 |
