# LDAP Authentication

When a client application or a user that runs the client application connects to the database, it must identify themselves. The process of validating the client's identity and determining whether this client is permitted to access the database it has requested is called **authentication**. 

Percona Distribution for PortgreSQL supports several [authentication methods](https://www.postgresql.org/docs/15/auth-methods.html), including the [LDAP authentication](https://www.postgresql.org/docs/14/auth-ldap.html). The use of LDAP is to provide a central place for authentication - meaning the LDAP server stores usernames and passwords and their resource permissions. 

The LDAP authentication in Percona Distribution for PortgreSQL is implemented the same way as in upstream PostgreSQL.