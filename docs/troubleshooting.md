# Troubleshooting guide

## Cannot create a table. Permission denied in schema `public`

Every database in PostgreSQL has a default schema called `public`. A schema stores database objects like tables, views, indexes and allows organizing them into logical groups.

When you create a table without specifying a schema name, it ends up in the `public` schema by default. 

Starting with PostgreSQL 15, non-database owners cannot access the `public` schema. Therefore, you can either grant privileges to the database for your user using the [GRANT :octicons-link-external-16:](https://www.postgresql.org/docs/{{pgvesrion}}/sql-grant.html) command or create your own schema to insert the data.

To create a schema, use the following statement:

```sql
CREATE SCHEMA demo;
```

To ensure all tables end up in your newly created schema, use the following statement ot set the schema:

```sql
CREATE SCHEMA demo;
```

Replace the `demo` name with your value.
