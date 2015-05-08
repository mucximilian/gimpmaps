SELECT * FROM (
	SELECT 
		ROW_NUMBER() OVER () AS id,
		get_scaled_svg_polygon(
			way,
			1281696.09029,
			6134530.14206,
			1291480.02991,
			6124746.20243,
			256,
			4
		) AS svg,
		way
	FROM (
		SELECT
			*
		FROM planet_osm_polygon
		WHERE ST_Intersects (
			way, 
			get_tile_bbox(
				1281696.09029,
				6134530.14206,
				1291480.02991,
				6124746.20243,
				256,
				12
			) 
		)
		AND ST_Area(way) > ((((1281696.09029-1271912.15067)/(256/2))*2)^2)
	) t
WHERE
	landuse='forest' OR leisure='park'
	) x WHERE coalesce(svg, '') <> ''