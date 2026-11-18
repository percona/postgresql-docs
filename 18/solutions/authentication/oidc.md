> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/18/llms.txt).

# OIDC authentication

[OpenID Connect](https://openid.net/developers/how-connect-works/) (or OIDC) authentication allows you to authenticate using tokens issued by an external identity provider. Instead of managing database passwords, you can delegate authentication to centralized identity services.

Percona Distribution for PostgreSQL integrates OIDC authentication using the `pg_oidc_validator` library, which validates OIDC tokens during client authentication.

The library is compatible with any identity provider that implements the OIDC standard.

For configuration details and source code, see the [pg_oidc_validator project](https://github.com/Percona-Lab/pg_oidc_validator) .

Important

OIDC authentication relies on [PostgreSQL OAuth authentication](https://www.postgresql.org/docs/current/auth-oauth.html) , introduced in PostgreSQL 18.

## When to use OIDC authentication

OIDC authentication is useful when you want to:

- integrate PostgreSQL with an existing single sign-on (SSO) platform
- reduce the need to manage database passwords
- centralize identity management across applications and databases

Tip

OIDC authentication simplifies access management for PostgreSQL when using an identity provider that supports OpenID Connect.

## OIDC authentication architecture

OIDC authentication works as follows:

1. The client obtains an access token from an external identity provider
1. The client connects to PostgreSQL using OAuth authentication
1. PostgreSQL forwards the token to the `pg_oidc_validator` module
1. The validator verifies the token signature and claims
1. If validation succeeds, PostgreSQL allows the connection

The following diagram shows how OIDC authentication works between the client, the identity provider, and PostgreSQL:

```
sequenceDiagram
    participant Client
    participant IdP as Identity Provider (OIDC)
    participant PostgreSQL
    participant Validator as pg_oidc_validator

    Client->>IdP: Request authentication
    IdP-->>Client: Return OIDC access token

    Client->>PostgreSQL: Connect using OAuth token
    PostgreSQL->>Validator: Validate token
    Validator-->>PostgreSQL: Token valid / invalid

    PostgreSQL-->>Client: Connection allowed or rejected
```

Tip

Before configuring OIDC authentication, ensure that your PostgreSQL deployment can access the identity provider that issues OIDC tokens.

## Set up OIDC authentication

Follow these steps to set up OIDC authentication for your PostgreSQL database.

1. Install the `pg_oidc_validator` package.

   For more information, see the [Quickstart guide](https://docs.percona.com/postgresql/18/installing.html).

   Alternatively, you can build the extension from source:

   ```
   make USE_PGXS=1 install -j
   ```

   Note

   A C++23 compiler and standard library is required to build `pg_oidc_validator`.

1. Edit `postgresql.conf` and add the validator library:

   ```
   oauth_validator_libraries = 'pg_oidc_validator'
   ```

   Note

   This setting tells PostgreSQL to load the OIDC validator during startup.

1. Add an OAuth authentication rule to `pg_hba.conf`:

   ```
   host all all 192.168.1.0/24 oauth scope="pgadmin-a",issuer=https://oidc.example.com
   ```

   Where:

   - `oauth` enables OAuth authentication
   - `scope` is the required OIDC scope
   - `issuer` is the URL of the OIDC identity provider
