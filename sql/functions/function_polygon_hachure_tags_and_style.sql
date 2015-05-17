CREATE OR REPLACE FUNCTION get_polygon_hachure_tags_and_style(IN map_style integer, IN zoom_level integer)
  RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, brush_hachure character varying, brush_hachure_size integer, color_hachure integer[], dynamics_hachure character varying, z_order integer) AS
$BODY$
SELECT
	mfph.id,
	of.tags,
	slb.brush,
	sl.brush_size,
	slc.color,
	sld.dynamics,
	shb.brush,
	sh.brush_size,
	shc.color,
	shd.dynamics,
	of.z_order
FROM
	map_feature_polygon_hachure mfph
LEFT JOIN
	style_line sl
ON (
	mfph.style_line = sl.id
)
LEFT JOIN 
	style_brush slb
ON (
	sl.brush = slb.id
)
LEFT JOIN style_color slc
ON (
	sl.color = slc.id
)
LEFT JOIN style_dynamics sld
ON (
	sl.dynamics = sld.id
)
LEFT JOIN
	style_line sh
ON (
	mfph.style_hachure = sh.id
)
LEFT JOIN 
	style_brush shb
ON (
	sl.brush = shb.id
)
LEFT JOIN style_color shc
ON (
	sh.color = shc.id
)
LEFT JOIN style_dynamics shd
ON (
	sl.dynamics = shd.id
)
LEFT JOIN osm_feature of
ON (
	mfph.osm_feature = of.id
)
WHERE mfph.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$BODY$
  LANGUAGE sql STABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION get_polygon_hachure_tags_and_style(integer, integer)
  OWNER TO gis;