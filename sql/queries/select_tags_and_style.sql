SELECT
	f.id,
	f.geometry,
	f.tags,
	f.z_order,
	b.brush,
	s.brush_size,
	c.color,
	s.opacity,
	d.dynamics,
	i.image,
	i.opacity AS opacity_image 
FROM 
	(
	SELECT * 
	FROM feature 
	WHERE 
		zoom_max <= 12
	AND 
		zoom_min >= 12
	) f
LEFT JOIN	
	style s 
ON (
	f.style = s.id
)
LEFT JOIN	
	brush b 
ON (
	s.brush = b.id
)
LEFT JOIN	
	color c
ON (
	s.color = c.id
)
LEFT JOIN	
	dynamics d 
ON (
	s.dynamics = d.id
)
LEFT JOIN
	image i
ON (
	f.style = i.style
)
ORDER BY f.geometry, f.z_order ASC