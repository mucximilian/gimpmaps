DROP FUNCTION gimpmaps_get_bbox(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
);

CREATE FUNCTION gimpmaps_get_bbox(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
)
RETURNS geometry
AS
$BODY$
DECLARE
	bbox geometry;
BEGIN  
	bbox = ST_MakeEnvelope( 
		ul_x - ((lr_x-ul_x)/size_x)*(brush_size/2),  
		ul_y + ((ul_y-lr_y)/size_y)*(brush_size/2),  
		lr_x + ((lr_x-ul_x)/size_x)*(brush_size/2),  
		lr_y - ((ul_y-lr_y)/size_y)*(brush_size/2),
		900913
	);
	RETURN bbox;
END;
$BODY$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION gimpmaps_get_bbox(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
	)
OWNER TO gis;