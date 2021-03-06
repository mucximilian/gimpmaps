﻿SELECT * FROM (
	SELECT 
		ROW_NUMBER() OVER () AS id,
		gimpmaps_scale_svg_polygon(
			ST_Union(way),
			1271912.15067,
			6134530.14206,
			1281696.09029,
			6124746.20243,
			256, 256,
			12
		) AS svg
	FROM (
		SELECT
			*
		FROM planet_osm_polygon
		WHERE ST_Intersects (
			way, 
			gimpmaps_get_bbox(
				1271912.15067,
				6134530.14206,
				1281696.09029,
				6124746.20243,
				256, 256,
				12
			) 
		)
		AND ST_Area(way) > ((((1281696.09029-1271912.15067)/(256/2))*2)^2)
	) t
	WHERE
		landuse='forest' OR leisure='park'
) x WHERE coalesce(svg, '') <> ''