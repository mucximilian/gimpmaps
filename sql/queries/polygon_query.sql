SELECT 
    ROW_NUMBER() OVER() AS id,
    gimpmaps_polygon(
        way, 
        1528600, 6631200, 1530300, 6630000, -- input bbox
        1295, 914, -- calculated image size
        4, -- brush size
        FALSE -- draw outline
    ) AS geom
FROM (
	SELECT
		-- union-dissolve of polygons
		ST_GeometryN(
			ST_Union(way),
			generate_series(
				1,
				ST_NumGeometries(ST_Union(way))
			)
		) AS way
	FROM
		planet_osm_polygon
	WHERE 
		way 
		&&
		gimpmaps_get_bbox(
			1528800, 6630800, 1530200, 6630100,
			1295, 914,
			4
		)
    AND
		building IS NOT NULL		
    )t
WHERE
	ST_Area(way) > (2 * 4) ^ 2