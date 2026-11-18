> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/17/llms.txt).

# Connect to the PostgreSQL server

With PostgreSQL server up and running, let’s connect to it.

By default, the `postgres` user and the `postgres` database are created in PostgreSQL upon its installation and initialization. This allows you to connect to the database as the `postgres` user.

1. Switch to the `postgres` user.

   ```
   $ sudo su postgres
   ```

1. Open the PostgreSQL interactive terminal `psql`:

   ```
   $ psql
   ```

   *Hint:* You can connect to `psql` as the `postgres` user in one go:

   ```
   $ sudo su - postgres -c psql
   ```

## Basic `psql` commands

While connected to PostgreSQL, let’s practice some basic `psql` commands to interact with the database:

1. List databases:

   ```
   $ \l
   ```

1. Display tables in the current database:

   ```
   $ \dt
   ```

1. Display columns in a table

   ```
   $ \d <table_name>
   ```

1. Switch databases

   ```
   $ \c <database_name>
   ```

1. Display users and roles

   ```
   $ \du
   ```

1. Exit the `psql` terminal:

   ```
   $ \q
   ```

To learn more about using `psql`, see [`psql`](https://www.postgresql.org/docs/current/app-psql.html) documentation.

Congratulations! You have connected to PostgreSQL and learned some essential `psql` commands.

## Next steps

[Manipulate data in PostgreSQL](https://docs.percona.com/postgresql/17/crud.html)
