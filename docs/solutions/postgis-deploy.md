# Deploy spatial data with PostgreSQL

The following document provides guidelines how to install PostGIS and how to run the basic queries. 

## Preconditions

1. We assume that you have the basic knowledge of spatial data, GIS (Geographical Information System) and of shapefiles.
2. For uploading the spatial data and querying the database, we use the same [data set](https://s3.amazonaws.com/s3.cleverelephant.ca/postgis-workshop-2020.zip) as is used in [PostGIS tutorial](http://postgis.net/workshops/postgis-intro/). 

## Install PostGIS

1. Enable Percona repository

    As other components of Percona Distribution for PostgreSQL, PostGIS is available from Percona repositories. Use the [`percona-release`](https://docs.percona.com/percona-software-repositories/installing.html) repository management tool to enable the repository. 

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup ppg14
    ```

2. Install PostGIS packages

    === "On Debian and Ubuntu"

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgis
          ```

          This installs the set of PostGIS extensions. To check what extensions are available, run the following query from the `psql` terminal:

          ```sql
          SELECT name, default_version,installed_version
          FROM pg_available_extensions WHERE name LIKE 'postgis%' or name LIKE 'address%';
          ```

        !!! note
            To enable the `postgis_sfcgal-3` extension on Ubuntu 18.04, you need to manually install the required dependency:

            ```{.bash data-prompt="$"}
            $ sudo apt-get install libsfcgal1
            ```

    === "On RHEL and derivatives"

          1. Install `epel` repository

              ```{.bash data-prompt="$"}
              $ sudo yum install epel-release
              ```

          2. Enable the `llvm-toolset dnf` module

              ```{.bash data-prompt="$"}
              $ sudo dnf module enable llvm-toolset
              ```

          3. Enable the codeready builder repository to resolve dependencies conflict. For Red Hat Enterprise Linux 8, replace the operating system version in the following commands accordingly.

            === "RHEL 9"

                 ```{.bash data-prompt="$"}
                 $ sudo dnf config-manager --set-enabled codeready-builder-for-rhel-9-x86_64-rpms
                 ```

            === "CentOS 9"

                 ```{.bash data-prompt="$"}
                 $ sudo dnf config-manager --set-enabled crb
                 ```

            === "Oracle Linux 9"

                 ```{.bash data-prompt="$"}
                 $ sudo dnf config-manager --set-enabled ol9_codeready_builder
                 ```

            === "Rocky Linux 9"
                 ```{.bash data-prompt="$"}
                 $ sudo dnf install dnf-plugins-core
                 $ sudo dnf config-manager --set-enabled powertools
                 ```
                
          4. Install the extension
              ```{.bash data-prompt="$"}                    
              $ sudo yum install percona-postgis33 percona-postgis33-client
              ```

          This installs the set of PostGIS extensions. To check what extensions are available, run the following query from the `psql` terminal:

          ```sql
          SELECT name, default_version,installed_version
          FROM pg_available_extensions WHERE name LIKE 'postgis%' or name LIKE 'address%';
          ```

3. Create a database and a schema for this database to store your data. A schema is a container that logically segments objects (tables, functions, views, and so on) for better management. Run the following commands from the `psql` terminal:

    ```sql
    CREATE database nyc;
    \c nyc;
    CREATE SCHEMA gis;
    ```

4. To make PostGIS functions and operations work, you need to enable the `postgis` extension. Make sure you are connected to the database you created earlier and run the following command:

    ```sql
    CREATE EXTENSION postgis;
    ```

5. Check that the extension is enabled:

    ```sql
    SELECT postgis_full_version();
    ```
    
    The output should resemble the following:

    ```{.sql .no-copy}
    postgis_full_version
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------
     POSTGIS="3.3.3" [EXTENSION] PGSQL="140" GEOS="3.10.2-CAPI-1.16.0" PROJ="8.2.1" LIBXML="2.9.13" LIBJSON="0.15" LIBPROTOBUF="1.3.3" WAGYU="0.5.0 (Internal)"
    ```

## Upload spatial data to PostgreSQL

PostGIS provides the `shp2pgsql` command line utility that converts the binary data from shapefiles into the series of SQL commands and loads them into the database.

1. For testing purposes, download the sample data set:

    ```{.bash data-prompt="$"}
    $ curl -LO https://s3.amazonaws.com/s3.cleverelephant.ca/postgis-workshop-2020.zip
    ```
    
2. From the folder where the `.shp` files are located, execute the following command and replace the `dbname` value with the name of your database:

    ```{.bash data-prompt="$"}
    shp2pgsql \
      -D \
      -I \
      -s 26918 \
      nyc_streets.shp \
      nyc_streets \
      | psql -U postgres dbname=nyc
    ```    
    
    The command does the following:

    * `-D` flag instructs the command to generate the dump format
    * `-I` flag instructs to create the spatial index on the table upon the data load
    * `-s` indicates the [spatial reference identifier](https://en.wikipedia.org/wiki/Spatial_reference_system) of the data. The data we load is in the Projected coordinate system for North America and has the value 26918.
    * `nyc_streets.shp` is the source shapefile
    * `nyc_streets` is the table name to create in the database
    * `dbname=nyc` is the database name

3. Check the uploaded data

   ```sql
   \d nyc_streets;
                                            Table "public.nyc_streets"
    Column |              Type               | Collation | Nullable |                 Default
   --------+---------------------------------+-----------+----------+------------------------------------------
    gid    | integer                         |           | not null | nextval('nyc_streets_gid_seq'::regclass)
    id     | double precision                |           |          |
    name   | character varying(200)          |           |          |
    oneway | character varying(10)           |           |          |
    type   | character varying(50)           |           |          |
    geom   | geometry(MultiLineString,26918) |           |          |
   Indexes:
       "nyc_streets_pkey" PRIMARY KEY, btree (gid)
       "nyc_streets_geom_idx" gist (geom)
   ```

4. Repeat the command to upload other shapefiles in the data set: `nyc_census_blocks`, `nyc_neighborhoods`, `nyc_subway_stations`