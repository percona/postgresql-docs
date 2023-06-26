# Query spatial data

After you [installed and set up PostGIS](postgis-deploy.md), let’s find answers to the following questions by querying the database:

## *What is the population of the New York City?*

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

## *What is the area of Central Park?*

To get the answer we will use the `ST_Area` function that returns the areas of polygons.

```sql
SELECT ST_Area(geom) / 1000000
  FROM nyc_neighborhoods
  WHERE name = 'Central Park';
```

Output:

```{.sql .no-copy}
      st_area
--------------------
 3.5198365965413294
(1 row)
```

By default, the output is given in square meters. To get the value in square kilometers, divide it by 1 000 000.

## *How long is Columbus Circle?*

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