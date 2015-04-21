/* DROP FUNCTION get_tags_and_style(
	zoom_level integer
); */

CREATE OR REPLACE FUNCTION get_line_tags_and_style(
	zoom_level integer
)
RETURNS TABLE(
	id integer,
	tags text[],
	z_order integer,
	brush character varying(20),
	brush_size numeric,
	color integer[],
	opacity integer,
	dnyamics character varying(20)
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
	s.opacity,
	s.dynamics
FROM 
	feature f
JOIN	style s 
ON (
	f.style = s.id
)
WHERE f.geometry = 2
AND f.zoom_max <= zoom_level
AND f.zoom_min >= zoom_level
ORDER BY f.z_order ASC
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_line_tags_and_style(
	zoom_level integer
)
OWNER TO gis;