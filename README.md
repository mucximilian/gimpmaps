# GIMPmaps

Collection of Python scripts and packages to create a single map or map tiles from an *OpenStreetMap* (OSM) *PostGIS* database using GIMP brushes and different dynamics.

## Database setup

For the scripts in this repository, a spatial *PostGIS* database with OSM data imported via *osm2pgsql* has to be set up containing the provided SQL/PLPGSQL functions. *osm2pgsql* along with *Osmosis* can be used to keep the data up to date.

Furthermore the style rules are stored in a separate PostgreSQL database. A current dump of the latest version of this database can be found in */sql/style/*. 

## GIMP setup

The files have to be stored in a GIMP plugin directory on your local computer. The directory */gimprenderer/python-fu* needs to be set as a plugin folder in the GIMP preferences. This can be done inside GIMP in the submenu *Folders* > *Plug-Ins* in the *Preferences* which can be accessed via the *Edit* menu.

Files for the **Brush** and **Dynamics** settings (*scripts/gimp_files/*) also need to be moved to the appropriate directories inside *~/.gimp-2.8*.

**Note:** The brush size settings only work with GIMP version 2.8.14.

* * *

Project environment: Xubuntu 14.04

License: GNU GENERAL PUBLIC LICENSE