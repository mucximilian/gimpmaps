SELECT 
	row_number() over() AS id,
	get_scaled_svg(
		ST_Union(way),
		1271912.15067,
		6124746.20243,
		1281696.09029,
		6114962.26281,
		256
	) AS svg
FROM (
	SELECT		
		*
	FROM planet_osm_line  
	WHERE ST_Intersects ( 
		way, 
		get_tile_bbox(
			1271912.15067,
			6124746.20243,
			1281696.09029,
			6114962.26281,
			256,
			12
		) 
	)
) t
WHERE
	highway = 'trunk'
