SELECT 
	ROW_NUMBER() OVER (ORDER BY id) AS id,
	line_type,
	svg
FROM (
	SELECT  
		SUM(osm_id) AS id,  
		highway,
		route,
		concat(highway, route) AS line_type,
		ST_AsSVG(  
			ST_Scale(
				ST_Translate(
					ST_Simplify(
						ST_Union(way),
						1
					),
					-1271912.15067,
					-6124746.20243
				),
				1/((1281696.09029-1271912.15067)/256),
				1/((6124746.20243-6114962.26281)/256)
			),
			1, 
			0 
		) AS svg  
	FROM planet_osm_line  
	WHERE ST_Intersects ( 
		way, 
		ST_MakeEnvelope( 
			1271912.15067 + (1/((1281696.09029-1271912.15067)/256))*(12/2),  
			6124746.20243 + (1/((6124746.20243-6114962.26281)/256))*(12/2),  
			1281696.09029 + (1/((1281696.09029-1271912.15067)/256))*(12/2),  
			6114962.26281 + (1/((6124746.20243-6114962.26281)/256))*(12/2),  
			900913 
		) 
	)
	GROUP BY line_type, highway, route
) t
WHERE
	highway = 'motorway' OR
	highway = 'motorway_link' OR
	highway = 'primary' OR 
	route = 'road' OR 
	highway = 'secondary'
