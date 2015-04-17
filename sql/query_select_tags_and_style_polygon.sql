SELECT
	f.id,
	f.tags,
	f.z_order,
	s.brush,
	s.brush_size,
	s.color,
	s.opacity,
	s.dynamics,
	i.image,
	i.opacity
FROM 
	feature f
JOIN	
	style s 
ON (
	f.style = s.id
)
JOIN
	image i
ON (
	f.style = i.style
)
WHERE f.geometry = 3
AND f.zoom_max <= 12
AND f.zoom_min >= 12
ORDER BY f.z_order DESC