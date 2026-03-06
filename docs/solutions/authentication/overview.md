# Authentication

Centralized authentication allows you to manage database access using external identity systems instead of local PostgreSQL users.

Percona Distribution for PostgreSQL supports multiple authentication mechanisms that integrate with enterprise identity infrastructure.

## Available authentication methods

### LDAP authentication

Use LDAP directories such as OpenLDAP or Active Directory to centrally manage database users.

[LDAP authentication](ldap.md)

### OIDC authentication

Authenticate users using OpenID Connect identity providers such as Keycloak, Okta, or Microsoft Entra ID.

[OIDC authentication](oidc.md)
