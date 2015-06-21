SELECT 
	ROW_NUMBER() OVER() AS id,
	svg
FROM (
	SELECT 
		gimpmaps_generalize_polygon(
			ST_Polygonize(ST_Collect(ST_DumpRings(ST_Union(way)))), 
			1.313
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

)t	
