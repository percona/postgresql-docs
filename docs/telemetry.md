
# Telemetry and data collection

Percona collects usage data to improve its software. The telemetry feature helps us identify popular features, detect problems, and plan future improvements. All collected data is anonymized so that it can't be traced back to any individual user.

Currently, telemetry is added only to the Percona packages and to Docker images. It is enabled by default so you must be running the latest version of `percona-release` to install Percona Distribution for PostgreSQL packages or update it to the latest version.

## What information is collected

Telemetry collects the following information:

* The information about the installation environment when you install the software.
* The information about the operating system such as name, architecture, the list of Percona packages. See more in the [Telemetry Agent section](#telemetry-agent).
* The metrics from the database instance. See more in the [percona_pg_telemetry section](#percona_pg_telemetry).

## What is NOT collected

Percona protects your privacy and doesn't collect any personal information about you like database names, user names or credentials or any user-entered values. 

All collected data is anonymous, meaning it can't be traced back to any individual user. To learn more about how Percona handles your data, read the [Percona Privacy statement](https://www.percona.com/privacy-policy).

You control whether to share this information. Participation in this program is completely voluntary. If don't want to share anonymous data, you can [disable telemetry](#disable-telemetry). 

## Why telemetry matters

Benefits for Percona:

| Advantages                  | Description                                                                                                                                                         |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| See how people use your software | Telemetry collects anonymous data on how users interact with our software. This tells developers which features are popular, which ones are confusing, and if anything is causing crashes. |
| Identify issues early       | Telemetry can catch bugs or performance problems before they become widespread. |

Benefits for users in the long run:

| Advantages                | Description                                                                                                         |
|---------------------------|---------------------------------------------------------------------------------------------------------------------|
| Faster bug fixes          | With telemetry data, developers can pinpoint issues affecting specific use cases and prioritize fixing them quickly.  |
| Improved features           | Telemetry helps developers understand user needs and preferences. This allows them to focus on features that will be genuinely useful and improve your overall experience. |
| Improved user experience  | By identifying and resolving issues early, telemetry helps create a more stable and reliable software experience for everyone. |

## Telemetry components

Percona collects information using the following components:

* Telemetry script that sends the information about the software and the environment where it is installed. This information is collected only once during the installation.

* The `percona_pg_telemetry` extension collects the necessary metrics directly from the database and stores them in a Metrics File.

* The Metrics File stores the metrics and is a standalone file located on the database host's file system.

* The Telemetry Agent is an independent process running on your database host's operating system and carries out the following tasks:

    * Collects OS-level metrics

    * Reads the Metrics File, adds the OS-level metrics

    * Sends the full set of metrics to the Percona Platform

    * Collects the list of installed Percona packages using the local package manager

The telemetry also uses the Percona Platform with the following components:

* Telemetry Service - offers an API endpoint for sending telemetry. The service handles incoming requests. This service saves the data into Telemetry Storage.

* Telemetry Storage - stores all telemetry data for the long term.

### `percona_pg_telemetry`

`percona_pg_telemetry` is an extension to collect telemetry data in PostgreSQL. It is added to Percona Distribution for PostgreSQL and is automatically loaded when you install a PostgreSQL server.

`percona_pg_telemetry` collects metrics from the database instance daily to the Metrics File. It creates a new Metrics File for each collection. You can find the Metrics File in its [location](#location) to inspect what data is collected. 

Before generating a new file, the `percona_pg_telemetry` deletes the Metrics Files that are older than seven days. This process ensures that only the most recent week's data is maintained.

The `percona_pg_telemetry` extension creates a file in the local file system using a timestamp and a randomly generated token as the name with a `.json` extension.

### Metrics File

The Metrics File is a JSON file with the metrics collected by the `percona_pg_telemetry` extension. 

#### Locations 

Percona stores the Metrics File in one of the following directories on the local file system. The location depends on the product.

* Telemetry root path - `/usr/local/percona/telemetry`

* PostgreSQL root path - `${telemetry root path}/pg/`

* Percona Server for MongoDB has two root paths since telemetry is enabled both for the `mongod` and `mongos` instances. The paths are the following:  

    * `mongod` root path -  `${telemetry root path}/psmdb/`
    * `mongos` root path -  `${telemetry root path}/psmdbs/`

* PS root path -   `${telemetry root path}/ps/`

* PXC root path - `${telemetry root path}/pxc/`

Percona archives the telemetry history in `${telemetry root path}/history/`.

#### Metrics File format

The Metrics File uses the JavaScript Object Notation (JSON) format. Percona reserves the right to extend the current set of JSON structure attributes in the future.

The following is an example of the collected data generated by the `percona_pg_telemetry` extension:    

```{.json .no-copy}
{
"db_instance_id": "7310358902660071382",
"pillar_version": "{{dockertag}}",
"uptime": "36",
"databases_count": "2",
"settings": [
  {
    "key": "setting",
    "value": [
      {
        "key": "name",
        "value": "allow_in_place_tablespaces"
      },
      {
        "key": "unit",
        "value": "NULL"
      },
      {
        "key": "setting",
        "value": "off"
      },
      {
        "key": "reset_val",
        "value": "off"
      },
      {
        "key": "boot_val",
        "value": "off"
      }
    ]
  },
  ...
],
"databases": [
  {
    "key": "database",
    "value": [
      {
        "key": "database_oid",
        "value": "5"
      },
      {
        "key": "database_size",
        "value": "7820895"
      },
      {
        "key": "active_extensions",
        "value": [
          {
            "key": "extension_name",
            "value": "plpgsql"
          },
          {
            "key": "extension_name",
            "value": "pg_tde"
          },
          {
            "key": "extension_name",
            "value": "percona_pg_telemetry"
          }
        ]
      }
    ]
  }
]
}
```


### Telemetry Agent

The Percona Telemetry Agent runs as a dedicated OS daemon process `percona-telemetry-agent`. It creates, reads, writes, and deletes JSON files in the [`${telemetry root path}`](#locations). You can find the agent's log file at `/var/log/percona/telemetry-agent.log`.

The agent does not send anything if there are no Percona-specific files in the target directory.

The following is an example of a Telemetry Agent payload:

```json
{
  "reports": [
    {
      "id": "B5BDC47B-B717-4EF5-AEDF-41A17C9C18BB",
      "createTime": "2023-09-01T10:56:49Z",
      "instanceId": "B5BDC47B-B717-4EF5-AEDF-41A17C9C18BA",
      "productFamily": "PRODUCT_FAMILY_POSTGRESQL",
      "metrics": [
        {
          "key": "OS",
          "value": "Ubuntu"
        },
        {
          "key": "pillar_version",
          "value": "{{dockertag}}"
        }
      ]
    }
  ]
}
```

The agent sends information about the database and metrics.

| Key | Description |
|---|---|
| "id" | A generated Universally Unique Identifier (UUID) version 4 |
| "createTime" | UNIX timestamp |
| "instanceId" | The DB Host ID. The value can be taken from the `instanceId`, the `/usr/local/percona/telemetry_uuid` or generated as a UUID version 4 if the file is absent. |
| "productFamily" | The value from the file path |
| "metrics" | An array of key:value pairs collected from the Metrics File.

The following operating system-level metrics are sent with each check:

| Key | Description |
|---|---|
| "OS" | The name of the operating system |
| "hardware_arch" | The type of process used in the environment |
| "deployment" | How the application was deployed. <br> The possible values could be "PACKAGE" or "DOCKER". |
| "installed_packages" | A list of the installed Percona packages.|

The information includes the following:

* Package name

* Package version - the same format as Red Hat Enterprise Linux or Debian

* Package repository - if possible

The package names must fit the following pattern:

* `percona-*`

* `Percona-*`

* `proxysql*`

* `pmm`

* `etcd*`

* `haproxy`

* `patroni`

* `pg*`

* `postgis`

* `wal2json`

## Disable telemetry 

Telemetry is enabled by default when you install the software. It is also included in the software packages (Telemetry Subsystem and Telemetry Agent) and enabled by default.

If you don't want to send the telemetry data, here's how: 

### Disable the telemetry collected during the installation

If you decide not to send usage data to Percona when you install the software, you can set the `PERCONA_TELEMETRY_DISABLE=1` environment variable for either the root user or in the operating system prior to the installation process.

=== "Debian-derived distribution"

    Add the environment variable before the installation process.

    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 apt install percona-ppg-server-14
    ```

=== "Red Hat-derived distribution"

    Add the environment variable before the installation process.
    
    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 yum install percona-ppg-server14
    ```

=== "Docker"

    Add the environment variable when running a command in a new container.
    
    ```{.bash data-prompt="$"}
    $ docker run -d --name pg --restart always \
      -e PERCONA_TELEMETRY_DISABLE=1 \
      percona/percona-distribution-postgresql:<TAG>-multi
    ```

    The command does the following:

    * `docker run` - This is the command to run a Docker container.
    * `-d` - This flag specifies that the container should run in detached mode (in the background).
    * `--name pg` - Assigns the name "pg" to the container.
    * `--restart always` - Configures the container to restart automatically if it stops or crashes.
    * `-e PERCONA_TELEMETRY_DISABLE=1` - Sets an environment variable within the container. In this case, it disables telemetry for Percona Distribution for PostgreSQL.
    * `percona/percona-distribution-postgresql:<TAG>-multi` - Specifies the image to use for the container. For example, `{{dockertag}}-multi`. The `multi` part of the tag serves to identify the architecture (x86_64 or ARM64) and use the respective image.


## Disable telemetry for the installed software

Percona software you installed includes the telemetry feature that collects information about how you use this software. It is enabled by default. To turn  off telemetry, you need to disable both the Telemetry Agent and the Telemetry Subsystem.

### Disable Telemetry Agent

In the first 24 hours, no information is collected or sent.

You can either disable the Telemetry Agent temporarily or permanently.

=== "Disable temporarily"

    Turn off Telemetry Agent temporarily until the next server restart with this command:

    ```{.bash data-prompt=$}
    $ systemctl stop percona-telemetry-agent
    ```

=== "Disable permanently"

    Turn off Telemetry Agent permanently with this command:

    ```{.bash data-prompt=$}
    $ systemctl disable percona-telemetry-agent
    ```

Even after stopping the Telemetry Agent service, a different part of the software (`percona_pg_telemetry`) continues to create the Metrics File related to telemetry every day and saves that file for seven days.

### Telemetry Agent dependencies and removal considerations

If you decide to remove the Telemetry Agent, this also removes the database. That's because the Telemetry Agent is a mandatory dependency for Percona Distribution for PostgreSQL. 

On YUM-based systems, the system removes the Telemetry Agent package when you remove the last dependency package.

On APT-based systems, you must use the '--autoremove' option to remove all dependencies, as the system doesn't automatically remove the Telemetry Agent when you remove the database package.

The '--autoremove' option only removes unnecessary dependencies. It doesn't remove dependencies required by other packages or guarantee the removal of all package-associated dependencies.

### Disable the `percona_pg_telemetry` extension

To disable the Metrics File creation, stop and drop the `percona_pg_telemetry` extension. Here's how to do it:

1. Stop the extension and reapply the configuration for the changes to take effect:

    ```sql
    ALTER SYSTEM SET percona_pg_telemetry.enabled = 0;
    SELECT pg_reload_conf();
    ```

2. Remove the `percona_pg_telemetry` extension from the database:
   
    ```sql
    DROP EXTENSION percona_pg_telemetry;
    ```

3. Remove `percona_pg_telemetry` from the `shared_preload_libraries` configuration parameter:

    ```sql
    ALTER SYSTEM SET shared_preload_libraries = '';
    ```

    !!! important  

        If the `shared_preload_libraries parameter` includes other modules, specify them all for the `ALTER SYSTEM SET` command to keep using them.

4. Restart the PostgreSQL server

    === ":material-debian: On Debian and Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo systemctl restart postgresql.service
         ```


    === ":material-redhat: On Red Hat Enterprise Linux and derivatives"

         ```{.bash data-prompt="$"}
         $ sudo systemctl restart postgresql-14
         ```


!!! tip

    If you wish to re-enable the Telemetry Subsystem, complete the above steps in the reverse order:
    
    1. Add the `percona_pg_telemetry` to the `shared_preload_libraries`, 
    2. Set `percona_pg_telemetry.enabled` to `1`, and 
    3. Restart the PostgreSQL server.
