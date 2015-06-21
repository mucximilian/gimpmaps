/*
This is a test of using a view as the query result to have a 
simple function which takes all parameters only once. The query
is too slow compared to the used query...
*/

-- Defining the view

DROP VIEW gimpmaps_polygon_osm CASCADE;

CREATE OR REPLACE VIEW gimpmaps_polygon_osm AS 
SELECT 
	*,
	''::text AS svg
FROM planet_osm_polygon;

-- Defining the function

DROP FUNCTION IF EXISTS gimpmaps_select_polygon(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
);

CREATE OR REPLACE FUNCTION gimpmaps_select_polygon(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
)
RETURNS SETOF planet_osm_polygon AS
$$
	SELECT
		*
	FROM 
		planet_osm_polygon
	WHERE 
		way 
		&&
		gimpmaps_get_bbox($1, $2, $3, $4, $5, $6, $7)
	AND 
		ST_Area(way) > ($7 * $7) ^2
$$
LANGUAGE SQL;

-- The actual query (for the Dresden city center)

SELECT 
	svg
FROM gimpmaps_select_polygon(
	1528600, 6631200, 1530300, 6630000, 
	1295, 914, 3
)
WHERE building IS NOT NULL