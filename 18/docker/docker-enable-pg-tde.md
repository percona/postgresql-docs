> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/18/llms.txt).

# Enable `pg_tde` for securing data at rest

Percona Distribution for PostgreSQL Docker image includes the `pg_tde` extension to provide data encryption.

Note

For more information about how `pg_tde` works, see the [pg_tde documentation](https://docs.percona.com/pg-tde/index.html) .

## Enable pg_tde

1. Start the container as shown in [Run in Docker](https://docs.percona.com/postgresql/18/docker/docker.html#start-container), adding the following option to the `docker run` command:

   ```
   -c shared_preload_libraries=pg_tde
   ```

1. Connect to the container and start the interactive `psql` session:

   ```
   docker exec -it container-name psql -U postgres
   ```

   Sample output

   ```
   psql (18.7 - Percona Server for PostgreSQL 18.7)
   Type "help" for help.

   postgres=#
   ```

1. Create the extension in the database where you want to encrypt data. This requires superuser privileges.

   ```
   CREATE EXTENSION pg_tde;
   ```

   Sample output

   ````
   ```{.text .no-copy}
   postgres=# CREATE EXTENSION pg_tde;
   CREATE EXTENSION
   ````

   ```
   ```

1. Add the key provider by using a keyring file. This setup is intended for development and stores the keys unencrypted in the specified data file. The below sample configuration is intended for testing and development purposes only.

   Note

   For production use, we **strongly recommend** setting up an external key management store and configure an external key provider. Refer to the [Setup](https://docs.percona.com/pg-tde/setup.html#key-provider-configuration) topic in the `pg_tde` documentation.

   Warning

   This example is for testing purposes only.

   ```
   SELECT pg_tde_add_database_key_provider_file('file-vault', '/tmp/pg_tde_test_001_basic.per');
   ```

1. Create the key:

   ```
   SELECT pg_tde_create_key_using_database_key_provider('test-db-key', 'file-vault');
   ```

1. Set the principal key:

   ```
   SELECT pg_tde_set_key_using_database_key_provider('test-db-key', 'file-vault');
   ```

1. Create a table with encryption enabled. Pass the `USING tde_heap` clause to the `CREATE TABLE` command:

   ```
   CREATE TABLE <table_name> (<field> <datatype>) USING tde_heap;
   ```

   CREATE TABLE example

   ```
   CREATE TABLE test_users (
       user_id INT,
       username VARCHAR(50),
       email VARCHAR(100),
       signup_date DATE
   ) USING tde_heap;
   ```

## Next steps

[Enable `pg_stat_monitor` for performance statistics](https://docs.percona.com/postgresql/18/docker/docker-enable-pg-stat-monitor.html)
