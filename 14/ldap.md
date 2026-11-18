> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/14/llms.txt).

# LDAP authentication

Percona’s PostgreSQL allows you to use LDAP, which uses a central authentication server for storing usernames, passwords and their resource permissions.

The LDAP authentication method in Percona Distribution for PortgreSQL is functionally the same as upstream PostgreSQL, check the documentation [here](https://www.postgresql.org/docs/14/auth-ldap.html) for more information.

## Set up LDAP authentication

Follow these steps to set up LDAP authentication for your PostgreSQL database.

1. Add in the `pg_hba.conf` file (usually located in `/data/db/...`) the `ldap` authentication method. For example:

   ```
   host all all 192.168.1.0/24 ldap ldapserver=ldap.example.com ldapport=389 ldapbinddn="cn=admin,dc=example,dc=com" ldapbindpasswd="password"
   ```

1. Add or modify the LDAP configuration parameters (`ldapbindpasswd`, `ldapbinddn`, and so on) in your `postgresql.conf` file.

   Tip

   You can directly add the parameters using the `ALTER SYSTEM` command in the psql command line. See a more in-depth list of LDAP configuration parameters [here](https://www.postgresql.org/docs/14/auth-ldap.html) .

1. Restart your PostgreSQL service to apply the changes.

1. Connect to your database as a superuser and create the roles that correspond to groups or users in your LDAP directory.

1. Grant appropriate permissions to these roles using [standard SQL GRANT statements](https://www.postgresql.org/docs/14/sql-grant.html) .

By following these steps, you have successfully integrated LDAP authentication into your environment.
