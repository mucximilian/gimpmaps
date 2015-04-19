# GimpTiles
Collection of Python scripts to create map tiles using Gimp brush styling from an OpenStreetMap PostGIS database.

## Database setup

For the scripts in this repository, a PostGIS database with OpenStreetMap data (e.g. imported via *osm2pgsql*) has to be set up with the provided SQL/PLPGSQL functions. Furthermore the styling is also stored in a separate PostgreSQL database which is not part of the repository yet but this will be fixed soon.

## GIMP setup

The files have to be stored in a GIMP plugin directory on your local computer. This could either be in *~/.gimp-2.8/Plugins* or any other directory that is set as a plugin folder in the GIMP preferences.

Files for the **Brush** and **Dynamics** settings (*scripts/gimp_files/*) also need to be moved to the appropriate directories inside *~/.gimp-2.8*.

**Note:** The brush size settings only work with GIMP version 2.8.14.