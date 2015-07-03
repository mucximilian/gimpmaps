-- Function: gimpmaps_scale_svg_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer, integer)

-- DROP FUNCTION gimpmaps_scale_svg_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer, integer);

CREATE OR REPLACE FUNCTION gimpmaps_scale_svg_polygon(geom geometry, ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer, brushsize integer, outline boolean)
  RETURNS text AS
$BODY$
DECLARE
	svg text;
	pixel_in_m_x numeric;
	pixel_in_m_y numeric;
	pixel_in_m numeric;
	brushsize_in_m numeric;
	outline_buffer numeric;

BEGIN 
	-- Calculating the size of one image pixel in meter
	pixel_in_m_x = ((lr_x-ul_x)/size_x);
	pixel_in_m_y = ((ul_y-lr_y)/size_y);
	pixel_in_m = GREATEST(pixel_in_m_x, pixel_in_m_y);
	
	-- Calculating the brushsize in meter for buffering	
	brushsize_in_m = brushsize * pixel_in_m;

	-- If an outline should be drawn do another negative buffering of half the brush size of the outline
	IF 
		outline
	THEN
		outline_buffer = -(brushsize_in_m/2);
	ELSE
		outline_buffer = 0;
	END IF;
	
	svg = ST_AsSVG(  
		ST_Scale(
			ST_Translate(
				ST_SimplifyPreserveTopology(
					-- Negative buffer half of brushsize to make outline brush fit the polygon bounds
					ST_Buffer(
						gimpmaps_generalize_polygon(
							geom,
							pixel_in_m
						),
						outline_buffer,
						'join=mitre miter_limit=' || brushsize_in_m
					),
					pixel_in_m
				),
				-ul_x,
				-ul_y
			),
			1/pixel_in_m_x,
			1/pixel_in_m_y
		),
		0, -- absolute moves (relative = 1)
		2 -- decimal digits
	);
	RETURN svg;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_scale_svg_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer, integer)
  OWNER TO gis;
