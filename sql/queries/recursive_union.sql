SELECT 1 as id, ST_Union(way) FROM(
WITH RECURSIVE box AS (
	SELECT ST_Union(way) AS way FROM 
		planet_osm_polygon
	WHERE
		way
		&&
		ST_MakeBox2D('POINT(1287363 6129915)', 'POINT(1287400 6129876)')
	AND building IS NOT NULL

	UNION ALL
	
	SELECT DISTINCT p.way FROM
		planet_osm_polygon p, box b
	WHERE
		(
		ST_Touches(
			b.way,
			p.way
		)
	)
	AND 
		building IS NOT NULL
)
SELECT way FROM box LIMIT 100
)t