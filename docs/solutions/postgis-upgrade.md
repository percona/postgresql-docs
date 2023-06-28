# Spatial database upgrade

When using PostgreSQL and PostGIS for some time, you may eventually come to the decision to upgrade your spatial database. There can be different reasons for that: to receive improvements and/or bug fixes that come with a minor version of the database/extension, reaching the end of life of the currently used software and others.

The spatial database upgrade consists of two steps:

* upgrade of PostgreSQL, and 
* upgrade of the PostGIS extension. 

!!! important

    Before the upgrade, backup your data.

## Upgrade PostGIS

Each version of PostGIS is compatible with several versions of PostgreSQL and vise versa. The best practice is to first upgrade the PostGIS extension on the source cluster to match the compatible version on the target cluster and then upgrade PostgreSQL. Please see the [PostGIS Support matrix](https://trac.osgeo.org/postgis/wiki/UsersWikiPostgreSQLPostGIS#PostGISSupportMatrix) for version compatibility. 

PostGIS is enabled on the database level. This means that the upgrade is also done on the database level. 

=== "PostGIS 3 and above"

     Connect to the database where it is enabled and run the [`PostGIS_Extensions_Upgrade()`](https://postgis.net/docs/PostGIS_Extensions_Upgrade.html) function:

     ```sql
     SELECT postgis_extensions_upgrade();
     ```
     
     Repeat these steps to upgrade PostGIS on every database where it is enabled.

=== "PostGIS 2.5"

     Connect to the database with the enabled extension and run the following commands:

     ```sql
     ALTER EXTENSION postgis UPDATE;
     SELECT postgis_extensions_upgrade();
     ```

     Starting with version 3, vector and raster functionalities have been separated in two individual extensions. Thus, to upgrade those, you need to run the `postgis_extensions_upgrade();` twice.

     ```sql
     SELECT postgis_extensions_upgrade();
     ```

     TIP: If you don’t need the raster functionality, you can drop the `postgis_raster` extension after the upgrade.

     Repeat these steps to upgrade PostGIS on every database where it is enabled.

## Upgrade PostgreSQL

Upgrade PostgreSQL either to the [latest minor](../minor-upgrade.md) or to the [major version](../major-upgrade.md).

If you are using long deprecated views and functions and / or need the expertise in upgrading your spatial database, [contact Percona Managed Services](https://www.percona.com/services/managed-services) for an individual upgrade scenario development.
