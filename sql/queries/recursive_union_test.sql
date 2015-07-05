-- Way too slow...
WITH RECURSIVE t(n) AS (
    SELECT
		ST_Union(way)
	FROM 
		planet_osm_polygon
	WHERE
		way
		&&
		ST_MakeBox2D('POINT(1528600 6630000)', 'POINT(1530300 6631200)')
	AND building IS NOT NULL

	UNION ALL

	SELECT ST_Union(
		p.way,
		a.n
	)
	FROM planet_osm_polygon p, t a
	WHERE 
		NOT ST_Contains(a.n, p.way)
	AND
		ST_Intersects(
			a.n,
			p.way
		)
	AND building IS NOT NULL
)
SELECT
	1 AS id, ST_Union(n)
FROM t