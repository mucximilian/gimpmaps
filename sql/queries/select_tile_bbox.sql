SELECT
	ST_AsText(tile),
	ST_X(
		ST_pointN(
			ST_Boundary(tile),1
		)
	) || ','||
	ST_Y(
		ST_pointN(
			ST_Boundary(tile),1
		)
	) || ','||
	ST_X(
		ST_pointN(
			ST_Boundary(tile),3
		)
	) || ','||
	ST_Y(
		ST_pointN(
			ST_Boundary(tile),3
		)
	) AS bbox
FROM tiles_muc
WHERE id = 44955