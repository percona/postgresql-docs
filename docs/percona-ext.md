# Percona-authored extensions

Percona-authored extensions provide additional capabilities that go beyond upstream PostgreSQL, enabling advanced observability and data-at-rest encryption. These extensions are developed and maintained by Percona and are designed to integrate seamlessly with Percona Server for PostgreSQL and Percona Distribution for PostgreSQL.

This page provides a high-level overview of the available Percona-authored extensions and the problems they are intended to solve. For detailed configuration and usage instructions, follow the documentation links provided for each extension below.

<div data-grid markdown>
<div data-banner markdown>

## :octicons-graph-16: pg_stat_monitor

A query performance monitoring tool for PostgreSQL that brings more insight and details around query performance, planning statistics and metadata. It improves observability, enabling users to debug and tune query performance with precision.

[pg_stat_monitor documentation :octicons-link-external-16:](https://docs.percona.com/pg-stat-monitor/index.html){.md-button}
</div>

<div data-banner markdown>

## :material-file-key-outline: pg_tde

An open-source extension designed to enhance PostgreSQL’s security by encrypting data files on disk. The encryption is transparent for users, allowing them to access and manipulate data without managing encryption details.

You can also use `pg_tde` to enforce encryption at the database level, ensuring that all newly created data is encrypted without requiring per-table changes.

[For configuration details, see the pg_tde documentation. :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html){.md-button}

</div>
</div>
