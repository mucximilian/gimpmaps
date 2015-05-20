CREATE OR REPLACE FUNCTION get_background_image(IN map_style integer, IN zoom_level integer)
RETURNS TABLE (
  id integer,
  image character varying
) AS
$BODY$
SELECT
	mbi.id,
	si.image
FROM
	map_background_image mbi
JOIN
	style_image si
ON (
	mbi.style_image = si.id
)
WHERE mbi.map_style = $1
-- TO DO: Zoom Levels?
$BODY$
  LANGUAGE sql STABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION get_background_image(integer, integer)
  OWNER TO gis;
