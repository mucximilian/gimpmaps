-- Function: get_unclipped_tile(numeric, numeric, numeric, numeric, integer, integer)

-- DROP FUNCTION get_unclipped_tile(numeric, numeric, numeric, numeric, integer, integer);

CREATE OR REPLACE FUNCTION get_unclipped_tile(IN ul_x numeric, IN ul_y numeric, IN lr_x numeric, IN lr_y numeric, IN brush_size integer, IN tile_size integer)
  RETURNS TABLE(id bigint, highway text, route text, way geometry) AS
$BODY$
SELECT  
	row_number() over (ORDER BY osm_id) AS id,  
	highway,
	route,
	ST_Simplify(
		way,
		1
	)AS way  
FROM planet_osm_line  
WHERE ST_Intersects ( 
	way, 
	ST_MakeEnvelope( 
		ul_x - ((lr_x-ul_x)/tile_size)*(brush_size/2),  
		ul_y + ((ul_y-lr_y)/tile_size)*(brush_size/2),  
		lr_x + ((lr_x-ul_x)/tile_size)*(brush_size/2),  
		lr_y - ((ul_y-lr_y)/tile_size)*(brush_size/2),  
		900913 
	) 
);
$BODY$
  LANGUAGE sql STABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION get_unclipped_tile(numeric, numeric, numeric, numeric, integer, integer)
  OWNER TO gis;
