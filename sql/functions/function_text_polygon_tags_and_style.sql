DROP FUNCTION get_text_polygon_tags_and_style(integer);

CREATE OR REPLACE FUNCTION get_text_polygon_tags_and_style(IN map_style integer)
  RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer,
  color integer[], dynamics character varying, font character varying, 
  font_size integer, color_font integer[], z_order integer, zoom_min integer, 
  zoom_max integer,
  effect character varying,
  buffer_size integer,
  buffer_color integer[]) AS
$BODY$
SELECT
	mtp.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	slc.color,
	sd.dynamics,
	sf.name,
	st.font_size,
	stc.color,
	of.z_order,
	mtp.zoom_min,
	mtp.zoom_max,
	te.name AS effect,
	te.buffer_size,
	tec.color
FROM
	map_text_polygon mtp
LEFT JOIN
	style_line sl
ON (
	mtp.style_line = sl.id
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
LEFT JOIN style_text st
ON (
	mtp.style_text = st.id
)
LEFT JOIN style_font sf
ON (
	st.font = sf.id
)
LEFT JOIN style_color stc
ON (
	st.color = stc.id
)
LEFT JOIN text_effect te
ON (
	mtp.effect = te.id
)
LEFT JOIN style_color tec
ON (
	te.buffer_color = tec.id
)
LEFT JOIN osm_feature of
ON (
	mtp.osm_feature = of.id
)
WHERE mtp.map_style = $1
ORDER BY of.z_order DESC
$BODY$
  LANGUAGE sql STABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION get_text_polygon_tags_and_style(integer)
  OWNER TO gis;