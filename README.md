# GimpTiles
Collection of Python scripts to create map tiles using Gimp brush styling from an OpenStreetMap PostGIS database.

## Database setup

For the scripts in this repository, a spatial *PostGIS* database with OpenStreetMap data imported via *osm2pgsql* has to be set up containing the provided SQL/PLPGSQL functions. Furthermore the style rules are stored in a separate PostgreSQL database which is not part of the repository yet but an example setup script will be added soon.

## GIMP setup

The files have to be stored in a GIMP plugin directory on your local computer. The directory */gimprenderer/python-fu* needs to be set as a plugin folder in the GIMP preferences. This can be done inside GIMP in the submenu *Folders* > *Plug-Ins* in the *Preferences* which can be accessed via the *Edit* menu.

Files for the **Brush** and **Dynamics** settings (*scripts/gimp_files/*) also need to be moved to the appropriate directories inside *~/.gimp-2.8*.

**Note:** The brush size settings only work with GIMP version 2.8.14.