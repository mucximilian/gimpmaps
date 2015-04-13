/*DROP FUNCTION get_scaled_svg(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size integer
);*/

CREATE OR REPLACE FUNCTION get_scaled_svg(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size integer
)
RETURNS text
AS
$BODY$
DECLARE
	svg text;
BEGIN  
	svg = ST_AsSVG(  
		ST_Scale(
			ST_Translate(
				ST_Simplify(
					geom,
					1
				),
				-ul_x,
				-ul_y
			),
			1/((lr_x-ul_x)/tile_size),
			1/((ul_y-lr_y)/tile_size)
		),
		1, 
		0 
	);
	RETURN svg;
END;
$BODY$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION get_scaled_svg(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size integer
	)
OWNER TO gis;