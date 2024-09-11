# Extensions

Percona Distribution for PostgreSQL is not only [Percona Server for PostgreSQL](postgresql-server.md). It also includes extensions - the add-ons that enhance the functionality of PostgreSQL database. By installing these extensions, you can modify and extend your database server with new features, functions, and data types.

Percona Distribution for PostgreSQL includes the extensions that have been tested to work together. These extensions encompass the following:

* [PostgreSQL contrib modules and utilities](contrib.md)
* [Extensions authored by Percona](percona-ext.md)
* [Third-party components](third-party.md)

Percona also supports [extra modules](https://repo.percona.com/ppg-17-extras/), not included in Percona Distribution for PostgreSQL but tested to work with it.

Additionally, see the list of [PostgreSQL software](https://www.percona.com/services/support/support-tiers-postgresql) covered by Percona Support.

## Install an extension

To use an extension, install it. Run the [`CREATE EXTENSION`](https://www.postgresql.org/docs/current/static/sql-createextension.html) command on the PostgreSQL node where you want the extension to be available. 

The user should be a superuser or have the `CREATE` privilege on the current database to be able to run the [`CREATE EXTENSION`](https://www.postgresql.org/docs/current/static/sql-createextension.html) command. Some extensions may require additional privileges depending on their functionality. To learn more, check the documentation for the desired extension.
