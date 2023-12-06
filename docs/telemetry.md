# Telemetry on Percona Distribution for PostgreSQL

Percona telemetry fills in the gaps in our understanding of how you use Percona Distribution for PostgreSQL to improve our products. Participation in this anonymous program is optional. You can opt-out if you prefer to not share this information.

## What information is collected

Currently, telemetry is added only to the Percona packages and Docker images. It collects only information about the installation environment. Future releases may add additional telemetry metrics.

Be assured that access to this raw data is rigorously controlled. Percona does not collect personal data. All data is anonymous and cannot be traced to a specific user. To learn more about our privacy practices, read the [Percona Privacy statement].

The following is an example of the collected data:

```json
[{"id" : "c416c3ee-48cd-471c-9733-37c2886f8231",
"product_family" : "PRODUCT_FAMILY_POSTGRESQL",
"instanceId" : "6aef422e-56a7-4530-af9d-94cc02198343",
"createTime" : "2023-11-01T10:46:23Z",
"metrics":
[{"key" : "deployment","value" : "PACKAGE"},
{"key" : "pillar_version","value" : "13.13"},
{"key" : "OS","value" : "Oracle Linux Server 8.8"},
{"key" : "hardware_arch","value" : "x86_64 x86_64"}]}]
```

## Disable telemetry

Starting with Percona Distribution for PostgreSQL 13.13, telemetry is enabled by default. If you decide not to send usage data to Percona, you can set the `PERCONA_TELEMETRY_DISABLE=1` environment variable for either the root user or in the operating system prior to the installation process.

=== "Debian-derived distribution"

    Add the environment variable before the install process.

    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 apt install percona-postgresql-{{pgversion}}
    ```

=== "Red Hat-derived distribution"

    Add the environment variable before the install process.
    
    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 yum install percona-postgresql{{pgversion}}-server
    ```

=== "DOCKER"

    Add the environment variable when running a command in a new container.
    
    ```{.bash data-prompt="$"}
    $ docker run --name container-name -e POSTGRES_PASSWORD=secret -e PERCONA_TELEMETRY_DISABLE=1 -d percona/percona-distribution-postgresql:tag 
    ```

[Percona Privacy statement]: https://www.percona.com/privacy-policy#h.e34c40q8sb1a