DROP FUNCTION gimpmaps_generalize_polygon(
	geom geometry,
	buffer numeric
);

CREATE FUNCTION gimpmaps_generalize_polygon(
	geom geometry,
	buffer numeric
)
RETURNS geometry
AS
$BODY$
DECLARE
	geom_new geometry;
BEGIN
	geom_new = ST_SimplifyPreserveTopology(
		ST_Buffer(
			ST_Buffer(
				ST_Buffer(
					ST_Buffer(
						geom,
						-(buffer*2), -- use buffer two times to eliminate small holes
						'join=mitre miter_limit=1'
					),
					(buffer*2),
					'join=mitre miter_limit=1'
				),
				(buffer*2),
				'join=mitre miter_limit=1'
			),
			-(buffer*2),
			'join=mitre miter_limit=1'
			),
		buffer
		);
	RETURN geom_new;
END;
$BODY$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION gimpmaps_generalize_polygon(
	geom geometry,
	buffer numeric
)
OWNER TO gis;