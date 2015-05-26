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
  color_fill integer[],
  z_order integer
  ) AS
$BODY$
SELECT
	mfp.id,
	of.tags,
	sbl.brush,
	sl.brush_size,
	scl.color,
	sdl.dynamics,
	sbh.brush,
	slh.brush_size,
	sch.color,
	sdh.dynamics,
	sh.spacing,
	sh.angle,
	si.image,
	scp.color,
	of.z_order
FROM
	map_feature_polygon mfp
LEFT JOIN
	style_line sl
ON (
	mfp.style_line = sl.id
)
LEFT JOIN 
	style_brush sbl
ON (
	sl.brush = sbl.id
)
LEFT JOIN style_color scl
ON (
	sl.color = scl.id
)
LEFT JOIN style_dynamics sdl
ON (
	sl.dynamics = sdl.id
)
LEFT JOIN
	style_hachure sh
ON (
	mfp.style_hachure = sh.id
)
LEFT JOIN
	style_line slh
ON (
	sh.style_line = slh.id
)
LEFT JOIN 
	style_brush sbh
ON (
	slh.brush = sbh.id
)
LEFT JOIN style_color sch
ON (
	slh.color = sch.id
)
LEFT JOIN style_dynamics sdh
ON (
	slh.dynamics = sdh.id
)
LEFT JOIN style_image si
ON (
	mfp.style_image = si.id
)
LEFT JOIN osm_feature of
ON (
	mfp.osm_feature = of.id
)
LEFT JOIN style_color scp
ON (
	mfp.color = scp.id
)
WHERE mfp.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order DESC
$BODY$
  LANGUAGE sql STABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION get_polygon_tags_and_style(integer, integer)
  OWNER TO gis;