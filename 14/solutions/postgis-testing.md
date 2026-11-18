> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/14/llms.txt).

# Query spatial data

After you [installed and set up PostGIS](https://docs.percona.com/postgresql/14/solutions/postgis-deploy.html), let’s find answers to the following questions by querying the database:

## *What is the population of the New York City?*

```
SELECT Sum(popn_total) AS population
  FROM nyc_census_blocks;
```

Output:

```
population
------------
    8175032
(1 row)
```

## *What is the area of Central Park?*

To get the answer we will use the `ST_Area` function that returns the areas of polygons.

```
SELECT ST_Area(geom) / 1000000
  FROM nyc_neighborhoods
  WHERE name = 'Central Park';
```

Output:

```
      st_area
--------------------
 3.5198365965413293
(1 row)
```

By default, the output is given in square meters. To get the value in square kilometers, divide it by 1 000 000.

## *How long is Columbus Circle?*

```
SELECT ST_Length(geom)
  FROM nyc_streets
  WHERE name = 'Columbus Cir';
```

Output:

```
     st_length
-------------------
 308.3419936909855
(1 row)
```
