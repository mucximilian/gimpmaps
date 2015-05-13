DROP FUNCTION gimpmaps_scale_svg_line(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer
);

CREATE OR REPLACE FUNCTION gimpmaps_scale_svg_line(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer
)
RETURNS text AS
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
			1/((lr_x-ul_x)/size_x),
			1/((ul_y-lr_y)/size_y)
		),
		0, -- absolute moves (relative = 1)
		1 -- decimal digits
	);
	RETURN svg;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_scale_svg_line(
	geom geometry,
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	size_x integer,
	size_y integer
)
OWNER TO gis;