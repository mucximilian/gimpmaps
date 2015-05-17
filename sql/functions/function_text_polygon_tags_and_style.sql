CREATE FUNCTION get_text_polygon_tags_and_style(
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
	style_color integer,
	z_order integer
	)
AS
$$
SELECT
	mftp.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	slc.color,
	sd.dynamics,
	mftp.style_color,
	of.z_order
FROM
	map_feature_text_polygon mftp
LEFT JOIN
	style_line sl
ON (
	mftp.style_line = sl.id
)
LEFT JOIN 
	style_brush sb
ON (
	sl.brush = sb.id
)
LEFT JOIN style_color slc
ON (
	sl.color = slc.id
)
LEFT JOIN style_dynamics sd
ON (
	sl.dynamics = sd.id
)
LEFT JOIN style_color sc
ON (
	mftp.style_color = sc.id
)
LEFT JOIN osm_feature of
ON (
	mftp.osm_feature = of.id
)
WHERE mftp.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_text_polygon_tags_and_style(
	map_style integer,
	zoom_level integer
)
OWNER TO gis;