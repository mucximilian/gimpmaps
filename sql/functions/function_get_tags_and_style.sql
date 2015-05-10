/* DROP FUNCTION get_tags_and_style(
	map_style integer,
	zoom_level integer
); */

CREATE OR REPLACE FUNCTION get_tags_and_style(
	map_style integer,
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
	s.id,
	f.geometry,
	f.tags,
	f.z_order,
	b.brush,
	fs.brush_size,
	c.color,
	fs.opacity,
	d.dynamics,
	i.image,
	i.opacity AS opacity_image 
FROM 
	styling s
LEFT JOIN
	feature f
ON (
	s.feature = f.id
)
LEFT JOIN
	feature_style fs
ON (
	s.feature_style = fs.id
)
LEFT JOIN	
	brush b 
ON (
	fs.brush = b.id
)
LEFT JOIN	
	color c
ON (
	fs.color = c.id
)
LEFT JOIN	
	dynamics d 
ON (
	fs.dynamics = d.id
)
LEFT JOIN
	image i
ON (
	s.feature_style = i.style
)
WHERE map_style = map_style
AND f.zoom_max <= zoom_level
AND f.zoom_min >= zoom_level
ORDER BY f.geometry, f.z_order ASC
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_tags_and_style(
	map_style integer,
	zoom_level integer
)
OWNER TO gis;