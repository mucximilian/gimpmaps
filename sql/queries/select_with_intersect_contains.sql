WITH a AS (
	SELECT ST_Union(way) AS way FROM 
		planet_osm_polygon
	WHERE
		way
		&&
		ST_MakeBox2D('POINT(1287382 6130030)', 'POINT(1287428 6129950)')
	AND building IS NOT NULL
)
SELECT * FROM
	planet_osm_polygon p, a a
WHERE
	(
	ST_Intersects(
		a.way,
		p.way
	)
	OR
	ST_Contains(
		a.way,
		p.way
	)
)
AND 
	building IS NOT NULL