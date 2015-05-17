SELECT
	s.id,
	f.feature_type,
	f.tags,
	f.z_order,
	b.brush,
	sl.brush_size,
	c.color,
	sl.opacity,
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
	style_line sl
ON (
	s.feature_style = sl.id
)
LEFT JOIN	
	brush b 
ON (
	sl.brush = b.id
)
LEFT JOIN	
	color c
ON (
	sl.color = c.id
)
LEFT JOIN	
	dynamics d 
ON (
	sl.dynamics = d.id
)
LEFT JOIN
	image i
ON (
	s.feature_style = i.style
)
WHERE s.map_style = 1
AND f.zoom_max <= 12
AND f.zoom_min >= 12
