WITH RECURSIVE box AS (
	SELECT ST_Union(way) AS way FROM 
		planet_osm_polygon
	WHERE
		way
		&&
		ST_MakeBox2D('POINT(1287333 6130030)', 'POINT(1287428 6129950)')
	AND building IS NOT NULL

	UNION ALL
	
	SELECT p.way FROM
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
SELECT way FROM box