SELECT 
	ROW_NUMBER() OVER () AS id,
	* 
FROM (
	SELECT
		--(ST_Union(way))
		ST_GeometryN(
			ST_Union(way),generate_series(
				1,ST_NumGeometries(ST_Union(way))
			)
		)
	FROM 
		planet_osm_polygon
	WHERE 
		way 
		&&
		gimpmaps_get_bbox(
			1528600, 6631200, 1530300, 6630000, 
			1295, 914, 3
		)
	AND
		ST_Area(way) > (3 * 3) ^ 2
	AND
		building IS NOT NULL
)t	

