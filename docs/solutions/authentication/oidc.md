# OIDC authentication

[OpenID Connect :octicons-link-external-16:](https://openid.net/developers/how-connect-works/) (or OIDC) authentication allows you to authenticate using tokens issued by an external identity provider. Instead of managing database passwords, you can delegate authentication to centralized identity services.

Percona Distribution for PostgreSQL integrates OIDC authentication using the `pg_oidc_validator` library, which validates OIDC tokens during client authentication.

The library is compatible with any identity provider that implements the OIDC standard.

For configuration details and source code, see the [pg_oidc_validator project :octicons-link-external-16:](https://github.com/Percona-Lab/pg_oidc_validator).

!!! important
    OIDC authentication relies on [PostgreSQL OAuth authentication :octicons-link-external-16:](https://www.postgresql.org/docs/current/auth-oauth.html), introduced in PostgreSQL 18.

## When to use OIDC authentication

OIDC authentication is useful when you want to:

* integrate PostgreSQL with an existing single sign-on (SSO) platform
* reduce the need to manage database passwords
* centralize identity management across applications and databases

!!! tip
    OIDC authentication simplifies access management for PostgreSQL when using an identity provider that supports OpenID Connect.

## OIDC authentication architecture

OIDC authentication works as follows:

1. The client obtains an access token from an external identity provider
2. The client connects to PostgreSQL using OAuth authentication
3. PostgreSQL forwards the token to the `pg_oidc_validator` module
4. The validator verifies the token signature and claims
5. If validation succeeds, PostgreSQL allows the connection

The following diagram shows how OIDC authentication works between the client, the identity provider, and PostgreSQL:

--8<-- "diagrams/oidc/auth-flow.md"

!!! tip
    Before configuring OIDC authentication, ensure that your PostgreSQL deployment can access the identity provider that issues OIDC tokens.

## Set up OIDC authentication

Follow these steps to set up OIDC authentication for your PostgreSQL database.
{.power-number}

1. Install the `pg_oidc_validator` package.

    For more information, see the [Quickstart guide](../../installing.md).

    Alternatively, you can build the extension from source:

    ```bash
    make USE_PGXS=1 install -j
    ```

    !!! note
        A C++23 compiler and standard library is required to build `pg_oidc_validator`.

2. Edit `postgresql.conf` and add the validator library:

    ```ini
    oauth_validator_libraries = 'pg_oidc_validator'
    ```

    !!! note
        This setting tells PostgreSQL to load the OIDC validator during startup.

3. Add an OAuth authentication rule to `pg_hba.conf`:

    ```ini
    host all all 192.168.1.0/24 oauth scope="openid email",issuer=https://oidc.example.com
    ```

    Where:

    * `oauth` enables OAuth authentication
    * `scope` is the required OIDC scope
    * `issuer` is the URL of the OIDC identity provider
