-- Function: gimpmaps_generalize_polygon(geometry, numeric)

-- DROP FUNCTION gimpmaps_generalize_polygon(geometry, numeric);

CREATE OR REPLACE FUNCTION gimpmaps_generalize_polygon(geom geometry, buffer_in numeric)
  RETURNS geometry AS
$BODY$
DECLARE
	geom_new geometry;
	buffer numeric;
BEGIN
	-- using buffer two times to eliminate small holes
	buffer = buffer_in * 2;

	geom_new = 
		ST_Buffer(
			ST_Buffer(
				ST_Buffer(
					ST_Buffer(
						geom,
						-(buffer), 
						'join=mitre miter_limit=' || buffer
					),
					(buffer),
					'join=mitre miter_limit=' || buffer
				),
				(buffer),
				'join=mitre miter_limit=' || buffer
			),
			-(buffer),
			'join=mitre miter_limit=' || buffer
		);
	RETURN geom_new;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_generalize_polygon(geometry, numeric)
  OWNER TO gis;


-- Function: gimpmaps_get_bbox(numeric, numeric, numeric, numeric, integer, integer, integer)

-- DROP FUNCTION gimpmaps_get_bbox(numeric, numeric, numeric, numeric, integer, integer, integer);

CREATE OR REPLACE FUNCTION gimpmaps_get_bbox(ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer, brushsize integer)
  RETURNS geometry AS
$BODY$
DECLARE
	pixel_in_m_x numeric;
	pixel_in_m_y numeric;
	bbox geometry;
BEGIN 

	-- Calculating the size of one pixel in meter
	pixel_in_m_x = ((lr_x-ul_x)/size_x);
	pixel_in_m_y = ((ul_y-lr_y)/size_y);

	bbox = ST_MakeEnvelope( 
		ul_x - pixel_in_m_x * (brushsize/2),  
		ul_y + pixel_in_m_y * (brushsize/2),  
		lr_x + pixel_in_m_x * (brushsize/2),  
		lr_y - pixel_in_m_y * (brushsize/2),
		900913
	);
	RETURN bbox;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_get_bbox(numeric, numeric, numeric, numeric, integer, integer, integer)
  OWNER TO gis;


-- Function: gimpmaps_transform(geometry, numeric, numeric, numeric, numeric, integer, integer)

-- DROP FUNCTION gimpmaps_transform(geometry, numeric, numeric, numeric, numeric, integer, integer);

CREATE OR REPLACE FUNCTION gimpmaps_transform(geom geometry, ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer)
  RETURNS text AS
$BODY$
DECLARE
	geom_scaled geometry;
	pixel_in_m_x numeric;
	pixel_in_m_y numeric;
	pixel_in_m numeric;

BEGIN 
	-- Calculating the size of one image pixel in meter
	pixel_in_m_x = ((lr_x-ul_x)/size_x);
	pixel_in_m_y = ((ul_y-lr_y)/size_y);
	pixel_in_m = GREATEST(pixel_in_m_x, pixel_in_m_y);
	
	geom_scaled = ST_Scale(
		ST_Translate(
			ST_SimplifyPreserveTopology(
				geom,
				pixel_in_m
			),
			-ul_x,
			-ul_y
		),
		1/pixel_in_m_x,
		1/pixel_in_m_y
	);
	RETURN geom_scaled;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_transform(geometry, numeric, numeric, numeric, numeric, integer, integer)
  OWNER TO postgres;

  -- Function: gimpmaps_line_svg(geometry, numeric, numeric, numeric, numeric, integer, integer)

-- DROP FUNCTION gimpmaps_line_svg(geometry, numeric, numeric, numeric, numeric, integer, integer);

CREATE OR REPLACE FUNCTION gimpmaps_line_svg(geom geometry, ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer)
  RETURNS text AS
$BODY$
DECLARE
	svg text;
BEGIN  
	svg = ST_AsSVG(  
		gimpmaps_transform(geom, ul_x, ul_y, lr_x, lr_y, size_x, size_y),
		0, -- absolute moves (relative = 1)
		2 -- decimal digits
	);
	RETURN svg;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_line_svg(geometry, numeric, numeric, numeric, numeric, integer, integer)
  OWNER TO gis;


-- Function: gimpmaps_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer, integer, boolean)

-- DROP FUNCTION gimpmaps_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer, integer, boolean);

CREATE OR REPLACE FUNCTION gimpmaps_polygon(geom geometry, ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer, brushsize integer, outline boolean)
  RETURNS geometry AS
$BODY$
DECLARE
	polygon geometry;
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
	
	polygon =
		-- Negative buffer half of brushsize to make outline brush fit the polygon bounds
		ST_Buffer(
			gimpmaps_generalize_polygon(
				geom,
				pixel_in_m
			),
			outline_buffer,
			'join=mitre miter_limit=' || brushsize_in_m
		);
	RETURN polygon;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_polygon(geometry, numeric, numeric, numeric, numeric, integer, integer, integer, boolean)
  OWNER TO postgres;


-- Function: gimpmaps_polygon_svg(geometry, numeric, numeric, numeric, numeric, integer, integer, integer, boolean)

-- DROP FUNCTION gimpmaps_polygon_svg(geometry, numeric, numeric, numeric, numeric, integer, integer, integer, boolean);

CREATE OR REPLACE FUNCTION gimpmaps_polygon_svg(geom geometry, ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer, brushsize integer, outline boolean)
  RETURNS text AS
$BODY$
DECLARE
	svg text;
BEGIN  
	svg = ST_AsSVG(  
		gimpmaps_transform(
			gimpmaps_polygon(geom, ul_x, ul_y, lr_x, lr_y, size_x, size_y, brushsize, outline),
			ul_x, ul_y, lr_x, lr_y, size_x, size_y
		),
		0, -- absolute moves (relative = 1)
		2 -- decimal digits
	);
	RETURN svg;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_polygon_svg(geometry, numeric, numeric, numeric, numeric, integer, integer, integer, boolean)
  OWNER TO gis;


-- Function: gimpmaps_scale_text_polygon_point(geometry, numeric, numeric, numeric, numeric, integer, integer)

-- DROP FUNCTION gimpmaps_scale_text_polygon_point(geometry, numeric, numeric, numeric, numeric, integer, integer);

CREATE OR REPLACE FUNCTION gimpmaps_scale_text_polygon_point(geom geometry, ul_x numeric, ul_y numeric, lr_x numeric, lr_y numeric, size_x integer, size_y integer)
  RETURNS numeric[] AS
$BODY$
DECLARE
	point geometry;
	points numeric[];
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
			
	points = ARRAY[
		ROUND(
			(St_X(point)::numeric),
			1
		),
		ROUND(
			(St_Y(point)::numeric),
			1
		)
	];

	RETURN points;
END;
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100;
ALTER FUNCTION gimpmaps_scale_text_polygon_point(geometry, numeric, numeric, numeric, numeric, integer, integer)
  OWNER TO gis;
