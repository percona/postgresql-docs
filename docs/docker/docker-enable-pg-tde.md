# Enable `pg_tde` for securing data at rest

Percona Distribution for PostgreSQL Docker image includes the `pg_tde` extension to provide data encryption.

For more information, see the [pg_tde documentation :octicons-link-external-16:](https://docs.percona.com/pg-tde/index.html).

## Enable pg_tde {.power-number}

1. Start the container as shown in [Run in Docker](docker.md#start-container), adding the following option to the `docker run` command:

    ```{.bash data-prompt="$"}
    -c shared_preload_libraries=pg_tde
    ```

2. Connect to the container and start the interactive `psql` session:

    ```{.bash data-prompt="$"}
    docker exec -it container-name psql -U postgres
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        psql ({{pgsubversion}} - Percona Server for PostgreSQL {{dockertag}})
        Type "help" for help.

        postgres=#
        ```

3. Create the extension in the database where you want to encrypt data. This requires superuser privileges.

    ```sql
    CREATE EXTENSION pg_tde;
    ```

    ??? example "Sample output"

            ```{.text .no-copy}
            postgres=# CREATE EXTENSION pg_tde;
            CREATE EXTENSION
            ```

4. Add the key provider by using a keyring file. This setup is intended for development and stores the keys unencrypted in the specified data file. The below sample configuration is intended for testing and development purposes only.

    !!! note
         For production use, we **strongly recommend** setting up an external key management store and configure an external key provider. Refer to the [Setup :octicons-link-external-16:](https://docs.percona.com/pg-tde/setup.html#key-provider-configuration) topic in the `pg_tde` documentation.

    !!! warning
        This example is for testing purposes only.

    ```sql
    SELECT pg_tde_add_database_key_provider_file('file-vault', '/tmp/pg_tde_test_001_basic.per');
    ```

5. Create the key:

    ```sql
    SELECT pg_tde_create_key_using_database_key_provider('test-db-key', 'file-vault');
    ```

6. Set the principal key:

    ```sql
    SELECT pg_tde_set_key_using_database_key_provider('test-db-key', 'file-vault');
    ```

7. Create a table with encryption enabled. Pass the `USING tde_heap` clause to the `CREATE TABLE` command:

    ```sql
    CREATE TABLE <table_name> (<field> <datatype>) USING tde_heap;
    ```

    ??? example "CREATE TABLE example"

        ```{.sql .no-copy}
        CREATE TABLE test_users (
            user_id INT,
            username VARCHAR(50),
            email VARCHAR(100),
            signup_date DATE
        ) USING tde_heap;
        ```
