-- DROP FUNCTION gimpmaps_scale_text_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer);

CREATE OR REPLACE FUNCTION gimpmaps_scale_text_polygon(geom geometry, ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer)
  RETURNS text AS
$BODY$
DECLARE
	point text;
BEGIN  
	point = ST_AsText(  
		ST_Scale(
			ST_Translate(
				ST_PointOnSurface(geom),
				-ul_x,
				-ul_y
			),
			1/((lr_x-ul_x)/size_x),
			1/((ul_y-lr_y)/size_y)
		)
	);
	RETURN point;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_scale_text_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer)
  OWNER TO gis;
