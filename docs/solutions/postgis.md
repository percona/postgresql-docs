# Spatial data manipulation

!!! admonition "Version added: 15.3"

Organizations dealing with spatial data need to store it somewhere and manipulate it. PostGIS is the open source extension for PostgreSQL that allows doing just that. It adds support for storing the spatial data types such as:

* Geographical data like points, lines, polygons, GPS coordinates that can be mapped on a sphere.
* Geometrical data. This is also points, lines and polygons but they apply to a 2D surface.

To operate with spatial data inside SQL queries, PostGIS supports [spatial functions](https://postgis.net/docs/reference.html#SRS_Functions) like distance, area, union, intersection. It uses the spatial indexes like [R-Tree](https://en.wikipedia.org/wiki/R-tree) and [Quadtree](https://en.wikipedia.org/wiki/Quadtree) for efficient processing of database operations. Read more about supported spatial functions and indexes in [PostGIS documentation](https://postgis.net/workshops/postgis-intro/introduction.html). 

By deploying PostGIS with Percona Distribution for PostgreSQL, you receive the open-source spatial database that you can use in various areas without vendor lock-in. 

## When to use PostGIS

You can use PostGIS in the following cases:

* To store and manage spatial data, create and store spatial shapes, calculate areas and distances
* To build the software that visualizes spatial data on a map, 
* To work with raster data, such as satellite imagery or digital elevation models.
* To integrate spatial and non-spatial data such as demographic or economic data in a database

## When not to use PostGIS

Despite its power and flexibility, PostGIS may not suit your needs if:

* You need to store only a couple of map locations. Consider using the [built-in geometric functions and operations of PostgreSQL](https://www.postgresql.org/docs/current/functions-geometry.html)
* You need real-time data analysis. While PostGIS can handle real-time spatial data, it may not be the best option for real-time data analysis on large volumes of data.
* You need complex 3D analysis or visualization.
* You need to acquire spatial data. Use other tools for this purpose and import spatial data into PostGIS to manipulate it.


## Next steps:

[Deployment](postgis-deploy.md)

