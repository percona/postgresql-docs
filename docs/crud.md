# Manipulate data in PostgreSQL

On the previous step, you have [connected to PostgreSQL](connect.md) as the superuser `postgres`. Now, let's insert some sample data and operate with it in PostgreSQL.

## Create a database

Let's create the database `test`. Use the CREATE DATABASE command:

```sql
CREATE DATABASE test;
```

## Create a table

Let's create a sample table `Customers` in the `test` database using the following command:

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,  -- 'id' is an auto-incrementing integer
    first_name VARCHAR(50), -- 'first_name' is a string with a maximum length of 50 characters
    last_name VARCHAR(50),  -- 'last_name' is a string with a maximum length of 50 characters
    email VARCHAR(100)      -- 'email' is a string with a maximum length of 100 characters
);
```

<i info>:material-information: Hint:</i>Having issues with table creation? Check our [Troubleshooting guide](troubleshooting.md)

## Insert the data

Populate the table with the sample data as follows:

```sql
INSERT INTO customers (first_name, last_name, email)
VALUES 
    ('John', 'Doe', 'john.doe@example.com'),  -- Insert a new row
    ('Jane', 'Doe', 'jane.doe@example.com');
    ('Alice', 'Smith', 'alice.smith@example.com');
```

## Query data

Let's verify the data insertion by querying it:

```sql
SELECT * FROM customers;
```

??? example "Expected output"

    ```{.sql .no-copy}
    id | first_name | last_name |          email
    ----+------------+-----------+-------------------------
      1 | John       | Doe       | john.doe@example.com
      2 | Jane       | Doe       | jane.doe@example.com
      3 | Alice      | Smith     | alice.smith@example.com
    (3 rows)
    ```

## Update data

Let's update John Doe's record with a new email address.

1. Use the UPDATE command for that:

    ```sql
    UPDATE customers 
    SET email = 'john.doe@myemail.com'
    WHERE first_name = 'John' AND last_name = 'Doe';
    ```

2. Query the table to verify the updated data:

    ```sql
    SELECT * FROM customers WHERE first_name = 'John' AND last_name = 'Doe';
    ```

    ??? example "Expected output"   

        ```{.sql .no-copy}
         id | first_name | last_name |          email
        ----+------------+-----------+-------------------------
          2 | Jane       | Doe       | jane.doe@example.com
          3 | Alice      | Smith     | alice.smith@example.com
          1 | John       | Doe       | john.doe@myemail.com
        (3 rows)
        ```

## Delete data

Use the DELETE command to delete rows. For example, delete the record of Alice Smith:

```sql
DELETE FROM Customers WHERE first_name = 'Alice' AND last_name = 'Smith';
```

If you wish to delete the whole table, use the `DROP TABLE` command instead as follows:

```sql
DROP TABLE customers;
```

To delete the whole database, use the DROP DATABASE command:

```sql
DROP DATABASE test;
```

Congratulations! You have used basic create, read, update and delete (CRUD) operations to manipulate data in Percona Distribution for PostgreSQL. To deepen your knowledge, see the [data manipulation :octicons-link-external-16:](https://www.postgresql.org/docs/{{pgversion}}/dml.html) section in PostgreSQL documentation.

## Next steps

[What's next?](whats-next.md)(.md-button)