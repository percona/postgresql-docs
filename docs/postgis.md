# PostGIS

!!! admonition "Version added: 15.3"


PostGIS is the open-source extension that allows storing and manipulating spacial data in PostgreSQL. 

Spatial data includes the following data types:

* Geographical data like points, lines, polygons, GPS coordinates that can be mapped on a sphere.
* Geometrical data. This is also points, lines and polygons but they apply to a 2D surface.

To operate with spacial data inside SQL queries, PostGIS supports [spacial functions](https://postgis.net/docs/reference.html#SRS_Functions) like distance, area, union, intersection. It uses the spacial indexes like [R-Tree](https://en.wikipedia.org/wiki/R-tree) and [Quadtree](https://en.wikipedia.org/wiki/Quadtree) for efficient processing of database operations. Read more about supported spacial functions and indexes in [PostGIS documentation](https://postgis.net/workshops/postgis-intro/introduction.html). 

## When to use PostGIS

You can use PostGIS in the following cases:

* To store and manage spatial data, create and store spatial shapes, calculate areas and distances
* To build the software that visualizes spacial data on a map, 
* To work with raster data, such as satellite imagery or digital elevation models.
* To integrate spatial and non-spatial data such as demographic or economic data in a database

## When not to use PostGIS

Despite its power and flexibility, PostGIS may not suit your needs if:

* You need to store only a couple of map locations. Consider using the [built-in geometric functions and operations of PostgreSQL](https://www.postgresql.org/docs/current/functions-geometry.html)
* You need real-time data analysis. While PostGIS can handle real-time spatial data, it may not be the best option for real-time data analysis on large volumes of data.
* You need complex 3D analysis or visualization.
* You need to acquire spatial data. Use other tools for this purpose and import spatial data into PostGIS to manipulate it.

## Get started 

The following section provides guidelines how to install PostGIS and how to run the basic queries. 

### Preconditions

1. We assume that you have the basic knowledge of spatial data, GIS (Geographical Information System) and of shapefiles.
2. You need to acquire spacial data. For the following examples, we will use the same [data set](https://s3.amazonaws.com/s3.cleverelephant.ca/postgis-workshop-2020.zip) as is used in [PostGIS tutorial](http://postgis.net/workshops/postgis-intro/) 

### Install PostGIS

1. Enable Percona repository.

   As other components of Percona Distribution for PostgreSQL, PostGIS is available from Percona repositories. Use the [`percona-release`](https://docs.percona.com/percona-software-repositories/installing.html) repository management tool to enable the repository. 

   ```{.bash data-prompt="$"}
   $ sudo percona-release setup ppg15
   ```

2. Install postGIS packages

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

### Upload spatial data to PostgreSQL

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

Repeat the command to upload other shapefiles in the data set: `nyc_census_blocks`, `nyc_neighborhoods`, `nyc_subway_stations`

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

### Querying the database

Now let’s find answers to the following questions by querying the database:

*What is the population of the New York City?*

```sql
SELECT Sum(popn_total) AS population
  FROM nyc_census_blocks;
```

Output:

```{.sql .no-copy}
population
------------
    8175032
(1 row)
```

*What is the area of Central Park?*

To get the answer we will use the `ST_Area` function that returns the areas of polygons.

```sql
SELECT ST_Area(geom) / 1000
  FROM nyc_neighborhoods
  WHERE name = 'Central Park';
```

Output:

```{.sql .no-copy}
      st_area
--------------------
 3519.8365965413293
(1 row)
```

By default, the output is given in square meters. To get the value in square kilometers, divide it by 1000.

*How long is Columbus Circle?*

```sql
SELECT ST_Length(geom)
  FROM nyc_streets
  WHERE name = 'Columbus Cir';
```

Output:

```{.sql .no-copy}
     st_length
-------------------
 308.3419936909855
(1 row)
```
