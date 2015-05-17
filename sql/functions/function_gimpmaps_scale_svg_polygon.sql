DROP FUNCTION gimpmaps_scale_svg_polygon(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
);

CREATE FUNCTION gimpmaps_scale_svg_polygon(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
)
RETURNS text
AS
$BODY$
DECLARE
	svg text;
	pixel_in_m_x numeric;
	pixel_in_m_y numeric;
	pixel_in_m numeric;

BEGIN 
	-- Calculating the size of one pixel in meter
	pixel_in_m_x = ((lr_x-ul_x)/size_x);
	pixel_in_m_y = ((ul_y-lr_y)/size_y);
	pixel_in_m = GREATEST(pixel_in_m_x, pixel_in_m_y);
	
	svg = ST_AsSVG(  
		ST_Scale(
			ST_Translate(
				ST_SimplifyPreserveTopology(
					ST_Buffer(
						gimpmaps_generalize_polygon(
							geom,
							pixel_in_m
						),
						-(brush_size/2),
						'join=mitre miter_limit=1'
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
		0 -- decimal digits
	);
	RETURN svg;
END;
$BODY$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION gimpmaps_scale_svg_polygon(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer,
	brush_size integer
	)
OWNER TO gis;