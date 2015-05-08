SELECT 
	row_to_json(z)
FROM (
	SELECT
		'12' AS zoom,
		(
		SELECT 
			array_to_json(array_agg(row_to_json(t))) AS line_styles
		FROM (
			SELECT 
				tags,
				z_order,
				(
				SELECT row_to_json(s)
				FROM (
					SELECT 
						brush,
						brush_size,
						color,
						opacity,
						dynamics
					FROM style
					WHERE id=feature.style
					) s
				) AS style
			FROM feature
			WHERE geometry = 2
		) t
	)
) z