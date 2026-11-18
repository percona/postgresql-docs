> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/16/llms.txt).

# Quickstart guide

This guide shows how to install and start Percona Distribution for PostgreSQL on Debian- and RHEL-based Linux systems. After completing this guide, you will have:

- PostgreSQL running locally
- A database named `test`
- A table named `customers`
- One inserted row you can query

## Fast path (2-minute install)

```
wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
sudo percona-release setup ppg-16  
sudo apt install percona-postgresql-16
sudo -i -u postgres psql
```

After psql starts, run the following SQL commands:

```
CREATE DATABASE test;
\c test
CREATE TABLE customers (first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100));
INSERT INTO customers VALUES ('John','Doe','john.doe@example.com');
SELECT * FROM customers;
\q
```

For a step-by-step explanation, continue below.

## Install on Debian / Ubuntu (APT)

1. Fetch the `percona-release` package:

   ```
   wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
   sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
   ```

1. Enable the repository and install the package:

   ```
   sudo percona-release setup ppg-16
   sudo apt install percona-postgresql-16
   ```

   The installation process automatically initializes and starts the default database.

   Note

   On Debian and Ubuntu systems, the `postgresql` service may show as `active (exited)`. This is expected.

1. Switch to the `postgres` user and open the psql interactive terminal:

   ```
   sudo -i -u postgres psql
   ```

1. Create a database and make a table in the database:

   ```
   CREATE DATABASE test;
   \c test
   CREATE TABLE customers (first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100));
   ```

1. Insert data in the customers table and query the data insertion:

   ```
   INSERT INTO customers VALUES ('John','Doe','john.doe@example.com');
   SELECT * FROM customers;
   \q
   ```

Congratulations! Percona Distribution for PostgreSQL is now running and you have created your first database.

For detailed installation steps and further instructions on Debian and Ubuntu, see the [Install Percona Distribution for PostgreSQL on Debian and Ubuntu](https://docs.percona.com/postgresql/16/apt.html).

For detailed installation steps and further instructions on Red Hat Enterprise Linux and derivatives, see the [Install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux and derivatives](https://docs.percona.com/postgresql/16/yum.html).

## What’s next

Now that your PostgreSQL server is running, you can explore additional capabilities of Percona Distribution for PostgreSQL.

### Learn PostgreSQL basics

Connect with `psql` and run SQL commands, manage users, roles, and configure authentication.

[Manipulate data in PostgreSQL](https://docs.percona.com/postgresql/16/crud.html)

### Enable extensions

Percona Distribution for PostgreSQL includes tested open source extensions, such as `pg_stat_monitor` for query performance monitoring, `pg_tde` for protecting data at rest and more.

[See Extensions](https://docs.percona.com/postgresql/16/extensions.html)

### Configure backups

For production deployments we recommend configuring backups.

[See Backup and disaster recovery in Percona](https://docs.percona.com/postgresql/16/solutions/backup-recovery.html)

### Configure high availability with Patroni

Deploy a highly available PostgreSQL cluster using Patroni to prevent service interruptions.

[See High Availability in PostgreSQL](https://docs.percona.com/postgresql/16/solutions/high-availability.html)
