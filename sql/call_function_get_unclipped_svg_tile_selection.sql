SELECT 
	ROW_NUMBER() OVER (ORDER BY id) AS id,
	line_type,
	svg
FROM 
	get_unclipped_svg_tile_union(
		1271912.15067,
		6124746.20243,
		1281696.09029,
		6114962.26281,
		12,
		256,
		'highway',
		'motorway'
	)