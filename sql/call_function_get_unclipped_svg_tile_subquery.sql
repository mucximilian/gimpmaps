SELECT * FROM (
	SELECT * 
	FROM get_unclipped_svg_tile(
		1271912.15067,
		6124746.20243,
		1281696.09029,
		6114962.26281,
		12,
		256
	) AS tile (
		id bigint,
		highway text,
		route text,
		svg text
	)
) t
WHERE
	highway = 'motorway' OR
	highway = 'motorway_link' OR
	highway = 'primary' OR 
	route = 'road' OR 
	highway = 'secondary'