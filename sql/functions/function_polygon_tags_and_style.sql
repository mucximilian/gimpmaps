DROP FUNCTION get_polygon_tags_and_style(integer, integer);

CREATE OR REPLACE FUNCTION get_polygon_tags_and_style(IN map_style integer, IN zoom_level integer)
  RETURNS TABLE(
  id integer, 
  tags text[], 
  brush character varying, 
  brush_size integer, 
  color integer[], 
  dynamics character varying, 
  brush_hachure character varying, 
  brush_hachure_size integer, 
  color_hachure integer[], 
  dynamics_hachure character varying,
  hachure_spacing integer,
  hachure_angle integer,
  image character varying, 
  z_order integer
  ) AS
$BODY$
SELECT
	mfp.id,
	of.tags,
	slb.brush,
	sl.brush_size,
	slc.color,
	sld.dynamics,
	shb.brush,
	sh.brush_size,
	shc.color,
	shd.dynamics,
	mfp.hachure_spacing,
	mfp.hachure_angle,
	si.image,
	of.z_order
FROM
	map_feature_polygon mfp
LEFT JOIN
	style_line sl
ON (
	mfp.style_line = sl.id
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
	mfp.style_hachure = sh.id
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
LEFT JOIN style_image si
ON (
	mfp.style_image = si.id
)
LEFT JOIN osm_feature of
ON (
	mfp.osm_feature = of.id
)
WHERE mfp.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$BODY$
  LANGUAGE sql STABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION get_polygon_tags_and_style(integer, integer)
  OWNER TO gis;
