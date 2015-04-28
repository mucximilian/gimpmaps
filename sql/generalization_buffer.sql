SELECT 
	ROW_NUMBER() OVER () AS id,
    ST_SimplifyPreserveTopology(
        ST_Buffer(
            ST_Buffer(
                ST_Buffer(
                    ST_Buffer(
                        ST_Union(way),
                        -((9763/256)*2)
                    ),
                    ((9763/256)*2)
                ),
                ((9763/256)*2)
            ),
            -((9763/256)*2)
        ),
        (9763/256)
    )
    
FROM (
	SELECT
		*
	FROM planet_osm_polygon
	WHERE ST_Intersects (
		way, 
		get_tile_bbox(
			1271912.15067,
			6134530.14206,
			1281696.09029,
			6124746.20243,
			256,
			12
		) 
	)
	AND ST_Area(way) > ((((1281696.09029-1271912.15067)/(256/2))*2)^2)
) t
WHERE
	landuse='forest' OR leisure='park'
