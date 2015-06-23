SELECT * FROM (
	SELECT svg FROM (
		SELECT
			gimpmaps_scale_svg_polygon(
				ST_GeometryN(
					ST_Union(way),generate_series(
						1,ST_NumGeometries(ST_Union(way))
					)
				),
				1528800, 6630800, 1530200, 6630100, 
				1067, 533, 3
			) AS svg
		FROM 
			planet_osm_polygon
		WHERE 
			way 
			&&
			gimpmaps_get_bbox(
				1528800, 6630800, 1530200, 6630100,
	1295, 914, 3
			)
		AND 
			ST_Area(way) > (3 * 3) ^ 2
		AND 
		building IS NOT NULL
	)t    
) x 