SELECT 
	row_number() over() AS id,
	name,
	gimpmaps_scale_text_polygon_point(
		way,
		1271912.15067,
		6124746.20243,
		1281696.09029,
		6114962.26281,
		256, 256
	) AS point
FROM (
	SELECT		
		*
	FROM planet_osm_polygon 
	WHERE ST_Intersects ( 
		way, 
		gimpmaps_get_bbox(
			1271912.15067,
			6124746.20243,
			1281696.09029,
			6114962.26281,
			256, 256,
			12
		) 
	)
) t
WHERE
	admin_level='6' OR
	admin_level='8' OR
	admin_level='9'OR
	admin_level='10'
