/* DROP FUNCTION get_tags_and_style(
	zoom_level integer
); */

CREATE OR REPLACE FUNCTION get_tags_and_style(
	zoom_level integer
)
RETURNS TABLE(
	id integer,
	geometry_type integer,
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
	f.geometry,
	f.tags,
	f.z_order,
	b.brush,
	s.brush_size,
	c.color,
	s.opacity,
	d.dynamics,
	i.image,
	i.opacity AS opacity_image 
FROM 
	(
	SELECT * 
	FROM feature 
	WHERE 
		zoom_max <= zoom_level
	AND 
		zoom_min >= zoom_level
	) f
LEFT JOIN	
	style s 
ON (
	f.style = s.id
)
LEFT JOIN	
	brush b 
ON (
	s.brush = b.id
)
LEFT JOIN	
	color c
ON (
	s.color = c.id
)
LEFT JOIN	
	dynamics d 
ON (
	s.dynamics = d.id
)
LEFT JOIN
	image i
ON (
	f.style = i.style
)
ORDER BY f.geometry, f.z_order DESC
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_tags_and_style(
	zoom_level integer
)
OWNER TO gis;