SELECT 
	ROW_NUMBER() OVER (ORDER BY osm_id) AS id,
	svg
FROM (
	SELECT
		get_scaled_svg(
			way,
			1280473.09783327,
			6121077.22507691,
			1281696.09028583,
			6119854.23262435,
			256
		) AS svg,
		*
	FROM planet_osm_polygon
	WHERE ST_Intersects ( 
		way, 
		get_tile_bbox(
			1280473.09783327,
			6121077.22507691,
			1281696.09028583,
			6119854.23262435,
			256,
			12
		) 
	)
) t
WHERE
	landuse = 'village_green'