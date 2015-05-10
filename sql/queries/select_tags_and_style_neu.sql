SELECT
	s.id,
	f.geometry,
	f.tags,
	f.z_order,
	b.brush,
	fs.brush_size,
	c.color,
	fs.opacity,
	d.dynamics,
	i.image,
	i.opacity AS opacity_image 
FROM 
	styling s
LEFT JOIN
	feature f
ON (
	s.feature = f.id
)
LEFT JOIN
	feature_style fs
ON (
	s.feature_style = fs.id
)
LEFT JOIN	
	brush b 
ON (
	fs.brush = b.id
)
LEFT JOIN	
	color c
ON (
	fs.color = c.id
)
LEFT JOIN	
	dynamics d 
ON (
	fs.dynamics = d.id
)
LEFT JOIN
	image i
ON (
	s.feature_style = i.style
)
WHERE map_style = 1
AND f.zoom_max <= 12
AND f.zoom_min >= 12
ORDER BY f.geometry, f.z_order ASC