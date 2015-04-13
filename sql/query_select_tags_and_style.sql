SELECT
	f.id,
	f.tags,
	f.z_order,
	s.brush,
	s.brush_size,
	s.color,
	s.opacity,
	s.dynamics
FROM 
	feature f
JOIN	style s 
ON (
	f.style = s.id
)
WHERE f.geometry = 2
AND f.zoom_max <= 12
AND f.zoom_min >= 12
