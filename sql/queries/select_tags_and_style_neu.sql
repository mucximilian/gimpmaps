SELECT
	s.id,
	f.id,
	f.geometry,
	f.zoom_min,
	f.zoom_max
FROM 
	styling s
LEFT JOIN
	feature f
ON (
	s.feature = f.id
) 
WHERE map_style = 1
AND f.zoom_max <= 12
AND f.zoom_min >= 12