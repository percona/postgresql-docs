# Deploy spatial data with PostgreSQL

The following document provides guidelines how to install PostGIS and how to run the basic queries. 

## Preconditions

1. We assume that you have the basic knowledge of spatial data, GIS (Geographical Information System) and of shapefiles.
2. You need to acquire spacial data. For the following examples, we'll use the same [data set](https://s3.amazonaws.com/s3.cleverelephant.ca/postgis-workshop-2020.zip) as is used in [PostGIS tutorial](http://postgis.net/workshops/postgis-intro/) 

## Install PostGIS

1. Enable Percona repository.

    As other components of Percona Distribution for PostgreSQL, PostGIS is available from Percona repositories. Use the [`percona-release`](https://docs.percona.com/percona-software-repositories/installing.html) repository management tool to enable the repository. 

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup ppg14
    ```

2. Install PostGIS packages

    === "On Debian and Ubuntu"

          ```{.bash data-prompt="$"}
          $ sudo apt install percona-postgis
          ```

    === "On RHEL and derivatives"

          ```{.bash data-prompt="$"}
          $ sudo yum install percona-postgis33
          ```

3. Create a database and a schema to store your data. A schema is a container that logically segments objects (tables, functions, views, and so on) for better management. Run the following commands from the `psql` terminal

    ```sql
    CREATE database nyc;
    CREATE SCHEMA gis;
    ```

4. To make PostGIS functions and operations work, you need to enable the `postgis` extension. From the `psql` terminal, switch to the database you created and run the following command:

    ```sql
    \c nyc;
    CREATE EXTENSION postgis;
    ```

5. Check that the extension is enabled:

    ```sql
    SELECT postgis_full_version();
    ```
    
    The output should be similar to the following:

    ```{.sql .no-copy}
    postgis_full_version
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------
     POSTGIS="3.3.3dev 0" [EXTENSION] PGSQL="140" GEOS="3.10.2-CAPI-1.16.0" PROJ="8.2.1" LIBXML="2.9.13" LIBJSON="0.15" LIBPROTOBUF="1.3.3" WAGYU="0.5.0 (Internal)"
    ```

## Upload spatial data to PostgreSQL

PostGIS provides the `shp2pgsql` command line utility that converts the binary data from shapefiles into the series of SQL commands and loads them into the database.

1. From the folder where the `.shp` files are located, execute the following command and replace the `dbname` value with the name of your database:

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

2. Check the uploaded data

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

3. Repeat the command to upload other shapefiles in the data set: `nyc_census_blocks`, `nyc_neighborhoods`, `nyc_subway_stations`