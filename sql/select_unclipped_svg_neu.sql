SELECT  
    row_number() over (ORDER BY osm_id) AS id,  
    highway,  
    ST_AsSVG(  
        ST_Scale(
		ST_Translate(
			ST_Simplify(
				way,
				0.1
			),
			-1271912.15067,
			-6134530.14206
		),
		1/((1281696.09029-1271912.15067)/256),
		1/((6134530.14206-6124746.20243)/256)
	),
        1, 
        0 
    ) AS svg 
FROM planet_osm_line  
WHERE ST_Intersects ( 
    way, 
    ST_MakeEnvelope( 
	1271912.15067,
	6134530.14206,
	1281696.09029,
	6124746.20243,
        900913 
    ) 
) 
AND 
(
highway = 'secondary' OR 
highway = 'motorway' OR 
highway = 'tertiary' OR 
highway = 'motorway_link' OR 
highway = 'residential' OR 
highway = 'service'
)