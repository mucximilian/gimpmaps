SELECT * FROM (
	(SELECT  
	row_number() over (ORDER BY osm_id) AS id,  
	highway,
	route,
	ST_AsSVG(  
		ST_Scale(
			ST_Translate(
				ST_Simplify(
					way,
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
))) t
WHERE
	highway = 'motorway' OR
	highway = 'motorway_link' OR
	highway = 'primary' OR 
	route = 'road' OR 
	highway = 'secondary'
