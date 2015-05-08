/* DROP FUNCTION get_polygon_tags_and_style(
	zoom_level integer
); */

CREATE OR REPLACE FUNCTION get_polygon_tags_and_style(
	zoom_level integer
)
RETURNS TABLE(
	id integer,
	tags text[],
	z_order integer,
	brush character varying(20),
	brush_size numeric,
	color integer[],
	opacity_brush integer,
	dynamics character varying(20),
	image character varying(50),
	opacity_image integer
	)
AS
$$
SELECT
	f.id,
	f.tags,
	f.z_order,
	s.brush,
	s.brush_size,
	s.color,
	s.opacity AS opacity_brush,
	s.dynamics,
	i.image,
	i.opacity AS opacity_image
FROM 
	feature f
JOIN	
	style s 
ON (
	f.style = s.id
)
JOIN
	image i
ON (
	f.style = i.style
)
WHERE f.geometry = 3
AND f.zoom_max <= zoom_level
AND f.zoom_min >= zoom_level
ORDER BY f.z_order DESC
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_polygon_tags_and_style(
	zoom_level integer
)
OWNER TO gis;