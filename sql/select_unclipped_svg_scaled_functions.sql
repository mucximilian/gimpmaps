SELECT 
	ROW_NUMBER() OVER (ORDER BY osm_id) AS id,
	svg
FROM (
	SELECT
		get_scaled_svg(
			way,
			1271912.15067,
			6124746.20243,
			1281696.09029,
			6114962.26281,
			256
		) AS svg,
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
	highway = 'motorway'
