/*DROP FUNCTION get_scaled_svg_polygon(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size_px integer
);*/

CREATE OR REPLACE FUNCTION get_scaled_svg_polygon(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size_px integer
)
RETURNS text
AS
$BODY$
DECLARE
	svg text;
	tile_pixel_m_x numeric;
	tile_pixel_m_y numeric;

BEGIN  
	tile_pixel_m_x = ((lr_x-ul_x)/tile_size_px);
	tile_pixel_m_y = ((ul_y-lr_y)/tile_size_px);
	
	svg = ST_AsSVG(  
		ST_Scale(
			ST_Translate(
				ST_SimplifyPreserveTopology(
					ST_Buffer(
						ST_Buffer(
							ST_Buffer(
								ST_Buffer(
									geom,
									-(tile_pixel_m_x*2),
									'join=mitre miter_limit=1'
								),
								(tile_pixel_m_x*2),
								'join=mitre miter_limit=1'
							),
							(tile_pixel_m_x*2),
							'join=mitre miter_limit=1'
						),
						-(tile_pixel_m_x*2),
						'join=mitre miter_limit=1'
					),
					tile_pixel_m_x
				),
				-ul_x,
				-ul_y
			),
			1/tile_pixel_m_x,
			1/tile_pixel_m_y
		),
		0, -- absolute moves (relative = 1)
		0 -- decimal digits
	);
	RETURN svg;
END;
$BODY$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION get_scaled_svg_polygon(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	tile_size_px integer
	)
OWNER TO gis;