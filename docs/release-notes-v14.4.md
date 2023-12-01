# Percona Distribution for PostgreSQL 14.4 (2022-06-27)


| Release date:     | June 27, 2022                                                    |
|:--------------|:----------------------------------------------------------------|
| **Installation**: | [Installing Percona Distribution for PostgreSQL](installing.md) |


Percona Distribution for PostgreSQL is a collection of tools to assist you in managing PostgreSQL. Percona Distribution for PostgreSQL
installs PostgreSQL and complements it by a selection of extensions that
enable solving essential practical tasks efficiently.

This release of Percona Distribution for PostgreSQL is based on [PostgreSQL 14.4](https://www.postgresql.org/docs/release/14.4/). It fixes the issue with all PostgreSQL 14 versions that could cause silent data corruption when using the `CREATE INDEX CONCURRENTLY` or `REINDEX CONCURRENTLY` commands. Learn how to detect and fix silent data corruption in your indexes in the [upstream documentation](https://www.postgresql.org/about/news/postgresql-144-released-2470/).

This release also includes the following bug fixes:

* Query plan memorization fixes
* Fixes for queries in which a "whole-row variable" references the result of a function that returns a domain over composite type
* Fixed the "variable not found in subplan target list" planner error using a `sub-SELECT` that is referenced in a `GROUPING` function
* Fixed error checking in `COPY FROM` when the database encoding is `SQL_ASCII` but the client encoding is a multi-byte encoding.
* Reported implicitly-created operator families (generated by `CREATE OPERATOR CLASS`) to event triggers.
* Prevented triggering `wal_receiver_timeout` on a standby during logical replication of large transactions.
* Removed incorrect TLS private key file ownership check in `libpq`.
* Prevented crash after server connection loss in `pg_amcheck`.

Find the full list of changes in the [PostgreSQL 14.4 release notes](https://www.postgresql.org/docs/release/14.4/). 

