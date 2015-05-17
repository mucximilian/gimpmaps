CREATE FUNCTION get_line_tags_and_style(
	map_style integer,
	zoom_level integer
)
RETURNS TABLE(
	id integer,
	tags text[],
	brush character varying(20),
	brush_size integer,
	color integer[],
	dynamics character varying(20),
	z_order integer
	)
AS
$$
SELECT
	mfl.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	sc.color,
	sd.dynamics,	
	of.z_order
FROM
	map_feature_line mfl
LEFT JOIN
	style_line sl
ON (
	mfl.style_line = sl.id
)
LEFT JOIN 
	style_brush sb
ON (
	sl.brush = sb.id
)
LEFT JOIN style_dynamics sd
ON (
	sl.dynamics = sd.id
)
LEFT JOIN style_color sc
ON (
	sl.color = sc.id
)
LEFT JOIN osm_feature of
ON (
	mfl.osm_feature = of.id
)
WHERE mfl.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_line_tags_and_style(
	map_style integer,
	zoom_level integer
)
OWNER TO gis;