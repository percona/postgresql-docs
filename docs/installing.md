# Quickstart guide

This guide shows how to install and start Percona Distribution for PostgreSQL on Debian- and RHEL-based Linux systems. After completing this guide, you will have:

- PostgreSQL running locally
- A database named `test`
- A table named `customers`
- One inserted row you can query

## Fast path (2-minute install)

```{.bash data-prompt="$"}
wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
sudo percona-release setup ppg-18  sudo apt install percona-postgresql-18sudo -i -u postgres psql
```

After psql starts, run the following SQL commands:

```sql
CREATE DATABASE test;
\c test
CREATE TABLE customers (first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100));
INSERT INTO customers VALUES ('John','Doe','john.doe@example.com');
SELECT * FROM customers;
\q
```

For a step-by-step explanation, continue below.

## Install on Debian / Ubuntu (APT) {.power-number}

1. Fetch the `percona-release` package:

     ```{.bash data-prompt="$"}
     wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
     sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
     ```

2. Enable the repository and install the package:

     ```{.bash data-prompt="$"}
     sudo percona-release setup ppg-18
     sudo apt install percona-postgresql-18
     ```

    The installation process automatically initializes and starts the default database.

3. Switch to the `postgres` user and open the psql interactive terminal:

     ```{.bash data-prompt="$"}
     sudo -i -u postgres
     psql
     ```

4. Create a database and make a table in the database:

     ```sql
     CREATE DATABASE test;
     \c test
     CREATE TABLE customers (first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100));
     ```

5. Insert data in the customers table and query the data insertion:

     ```sql
     INSERT INTO customers (first_name, last_name, email) VALUES ('John', 'Doe', 'john.doe@example.com');
     SELECT * FROM customers;
     \q
     ```

Congratulations! Percona Distribution for PostgreSQL is now running and you have created your first database.

For detailed installation steps and further instructions on Debian and Ubuntu, see the [Install Percona Distribution for PostgreSQL on Debian and Ubuntu](apt.md).

For detailed installation steps and further instructions on Red Hat Enterprise Linux and derivatives, see the [Install Percona Distribution for PostgreSQL on Red Hat Enterprise Linux and derivatives](yum.md).

## What's next

Now that your PostgreSQL server is running, you can explore additional capabilities of Percona Distribution for PostgreSQL.

<div data-grid markdown><div data-banner markdown>

### Learn PostgreSQL basics { .title }

Connect with `psql` and run SQL commands, manage users, roles, and configure authentication.

[Manipulate data in PostgreSQL :material-arrow-right:](crud.md){ .md-button }

</div><div data-banner markdown>

### Enable extensions { .title }

Percona Distribution for PostgreSQL includes tested open source extensions, such as `pg_stat_monitor` for query performance monitoring, `pg_tde` for protecting data at rest and more.

[See Extensions :material-arrow-right:](extensions.md){ .md-button }

</div><div data-banner markdown>

### Configure backups { .title }

For production deployments we recommend configuring backups.

[See Backup and disaster recovery in Percona :material-arrow-right:](solutions/backup-recovery.md){.md-button}
</div><div data-banner markdown>

### Configure high availability with Patroni { .title }

Deploy a highly available PostgreSQL cluster using Patroni to prevent service interruptions.

[See High Availability in PostgreSQL :material-arrow-right:](solutions/high-availability.md){.md-button}

</div>
</div>
