SELECT
	row_number() over (ORDER BY osm_id) AS id,
	highway,
	way AS geometry
FROM planet_osm_line 
WHERE ST_Intersects (
	way,
	ST_MakeEnvelope(
		1278200, 
		6120200, 
		1280000, 
		6121600, 
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

