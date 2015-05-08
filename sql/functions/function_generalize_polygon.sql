/*DROP FUNCTION get_generalized_polygon(
	geom geometry,
	tile_size_px numeric
);*/

CREATE OR REPLACE FUNCTION get_generalized_polygon(
	geom geometry,
	factor numeric
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
						-(factor*2),
						'join=mitre miter_limit=1'
					),
					(factor*2),
					'join=mitre miter_limit=1'
				),
				(factor*2),
				'join=mitre miter_limit=1'
			),
			-(factor*2),
			'join=mitre miter_limit=1'
			),
		factor
		);
	RETURN geom_new;
END;
$BODY$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION get_generalized_polygon(
	geom geometry,
	factor numeric
)
OWNER TO gis;