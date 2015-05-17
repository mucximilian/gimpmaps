CREATE FUNCTION get_polygon_image_tags_and_style(
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
	image character varying(50),
	z_order integer
	)
AS
$$
SELECT
	mfpi.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	sc.color,
	sd.dynamics,
	si.image,
	of.z_order
FROM
	map_feature_polygon_image mfpi
LEFT JOIN
	style_line sl
ON (
	mfpi.style_line = sl.id
)
LEFT JOIN 
	style_brush sb
ON (
	sl.brush = sb.id
)
LEFT JOIN style_color sc
ON (
	sl.color = sc.id
)
LEFT JOIN style_dynamics sd
ON (
	sl.dynamics = sd.id
)
LEFT JOIN style_image si
ON (
	mfpi.style_image = si.id
)
LEFT JOIN osm_feature of
ON (
	mfpi.osm_feature = of.id
)
WHERE mfpi.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_polygon_image_tags_and_style(
	map_style integer,
	zoom_level integer
)
OWNER TO gis;