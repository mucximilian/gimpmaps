/*DROP FUNCTION get_tile_bbox(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size integer,
	brush_size integer
);*/

CREATE OR REPLACE FUNCTION get_tile_bbox(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size integer,
	brush_size integer
)
RETURNS geometry
AS
$BODY$
DECLARE
	bbox geometry;
BEGIN  
	bbox = ST_MakeEnvelope( 
		ul_x - ((lr_x-ul_x)/tile_size)*(brush_size/2),  
		ul_y + ((ul_y-lr_y)/tile_size)*(brush_size/2),  
		lr_x + ((lr_x-ul_x)/tile_size)*(brush_size/2),  
		lr_y - ((ul_y-lr_y)/tile_size)*(brush_size/2),
		900913
	);
	RETURN bbox;
END;
$BODY$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION get_tile_bbox(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size integer,
	brush_size integer
	)
OWNER TO gis;