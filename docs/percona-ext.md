# Percona-authored extensions

Percona-authored extensions provide additional capabilities that go beyond upstream PostgreSQL, enabling advanced observability and data-at-rest encryption. These extensions are developed and maintained by Percona and are designed to integrate seamlessly with Percona Server for PostgreSQL and Percona Distribution for PostgreSQL.

This page provides a high-level overview of the available Percona-authored extensions and the problems they are intended to solve. For detailed configuration and usage instructions, follow the documentation links provided for each extension below.

<div data-grid markdown>
<div data-banner markdown>

## :octicons-graph-16: pg_stat_monitor

An open-source query performance monitoring tool for PostgreSQL that brings more insight and details around query performance, planning statistics and metadata. It improves observability, enabling users to debug and tune query performance with precision.

[See the pg_stat_monitor documentation :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/index.html){.md-button}
</div>

<div data-banner markdown>

## :material-file-key-outline: pg_tde

An open-source extension designed to enhance PostgreSQL security by encrypting data files on disk. `pg_tde` protects data at rest by ensuring that database files cannot be read without the appropriate encryption keys. Encryption is transparent to applications and users at the SQL level, while key management is configured separately.

[See the pg_tde documentation :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html){.md-button}

</div>

<div data-banner markdown>

## :material-file-key-outline: pg_oidc_validator

An **experimental** OAuth validator library for PostgreSQL 18 that validates OpenID Connect (OIDC) JWT access tokens. It integrates with PostgreSQL’s OAuth framework to verify tokens issued by compliant OIDC providers.

**NOTE:** This library is still experimental and not intended for production use.

[Check the pg_oidc_validator GitHub repository :octicons-link-external-16:](https://github.com/Percona-Lab/pg_oidc_validator){.md-button}

</div>
</div>
