SELECT * FROM (
	SELECT svg FROM (
		SELECT 
			gimpmaps_scale_svg_polygon(
				ST_Union(way),
				1528600, 6631200, 1530300, 6630000, 
				1295, 914, 3
			) AS svg
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
			building is not null
	)t	
)x
