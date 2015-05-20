CREATE OR REPLACE FUNCTION gimpmaps_scale_text_polygon_point(
	geom geometry, 
	ul_x numeric, 
	ul_y numeric, 
	lr_x numeric, 
	lr_y numeric, 
	size_x integer, 
	size_y integer
)
RETURNS TABLE(x double precision, y double precision) AS
$BODY$
DECLARE
	point geometry;
BEGIN  
	point = ST_Scale(
				ST_Translate(
					ST_PointOnSurface(geom),
					-ul_x,
					-ul_y
				),
				1/((lr_x-ul_x)/size_x),
				1/((ul_y-lr_y)/size_y)
			);

	RETURN QUERY SELECT St_X(point) AS x, St_Y(point) AS y;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_scale_text_polygon_point(
	geometry,
	numeric, 
	numeric, 
	numeric, 
	numeric, 
	integer, 
	integer
)
  OWNER TO gis;
