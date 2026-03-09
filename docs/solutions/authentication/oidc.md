# OIDC authentication

OpenID Connect (or OIDC) authentication allows you to authenticate using tokens issued by an external identity provider. Instead of managing database passwords, you can delegate authentication to centralized identity services.

Percona Distribution for PostgreSQL supports OIDC authentication through the `pg_oidc_validator` library. This library validates OIDC tokens during the PostgreSQL authentication process.

## When to use OIDC authentication

OIDC authentication is useful when you want to:

* integrate PostgreSQL with an existing single sign-on (SSO) platform
* reduce the need to manage database passwords
* centralize identity management across applications and databases

!!! tip
     OIDC authentication simplifies access management for PostgreSQL when using an identity provider that supports OpenID Connect.

## Authentication flow

The OIDC authentication works as follows:

1. The client obtains an access token from an external identity provider
2. The client connects to PostgreSQL using OAuth authentication
3. PostgreSQL forwards the token to the `pg_oidc_validator` module
4. The validator verifies the token signature and claims
5. If validation succeeds, PostgreSQL allows the connection

## Set up OIDC authentication

Follow these steps to set up OIDC authentication for your PostgreSQL database.
{.power-number}

1. Install the `pg_oidc_validator` package:

    For Debian/Ubuntu:

    ```bash
    sudo apt install pg-oidc-validator-pgdg{{pgversion}}
    ```

    For RHEL/Oracle Linux/Rocky Linux:

    ```bash
    sudo dnf install pg-oidc-validator-pgdg{{pgversion}}
    ```

2. Edit `postgresql.conf` and add the validator library:

    ```ini
    oauth_validator_libraries = 'pg_oidc_validator'
    ```

    !!! note
         This setting tells PostgreSQL to load the OIDC validator during startup.

3. Add an OAuth authentication rule to `pg_hba.conf`:

    ```ini
    host all all 192.168.1.0/24 oauth scope="openid",issuer=https://your-oidc-provider
    ```

    Where:

    * `oauth` enables OAuth authentication
    * `scope` is the required OIDC scope
    * `issuer` is the URL of the OIDC identity provider

4. Restart PostgreSQL for the changes to take effect:

    ```ini
    sudo systemctl restart postgresql
    ```

!!! important
     Percona Distribution for PostgreSQL does not issue OIDC tokens. You must obtain a valid access token from an external identity provider such as Keycloak, Okta, or Microsoft Entra ID before connecting.
