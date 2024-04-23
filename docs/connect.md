# Connect to the PostgreSQL server

With PostgreSQL server up and running, let's connect to it.

By default, the `postgres` user and the `postgres` database are created in PostgreSQL upon its installation and initialization. This allows you to connect to the database as the `postgres` user.

1. Switch to the `postgres` user.

    ```{.bash data-prompt="$"}
    $ sudo su postgres
    ```

2. Open the PostgreSQL interactive terminal `psql`:

    ```{.bash data-prompt="$"}
    $ psql
    ```

    <i info>:material-information: Hint:</i> You can connect to `psql` as the `postgres` user in one go: 
    
    ```{.bash data-prompt="$"}
    $ sudo su - postgres -c psql
    ```


## Basic `psql` commands

While connected to PostgreSQL, let's practice some basic `psql` commands to interact with the database:

1. List databases:

    ```{.bash data-prompt="$"}
    $ \l
    ```

2. Display tables in the current database:

    ```{.bash data-prompt="$"}
    $ \dt
    ```

3. Display columns in a table

    ```{.bash data-prompt="$"}
    $ \d <table_name>
    ```

4. Switch databases

    ```{.bash data-prompt="$"}
    $ \c <database_name>
    ```

5. Display users and roles

    ```{.bash data-prompt="$"}
    $ \du
    ```

6. Exit the `psql` terminal:

    ```{.bash data-prompt="$"}
    $ \q
    ```

To learn more about using `psql`, see [`psql` :octicons-link-external-16:](https://www.postgresql.org/docs/current/app-psql.html) documentation.

Congratulations! You have connected to PostgreSQL and learned some essential `psql` commands. 

## Next steps

[Manipulate data in PostgreSQL :material-arrow-right:](crud.md){.md-button}