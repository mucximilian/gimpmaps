﻿/* DROP FUNCTION get_unclipped_svg_tile_selection_2(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	brush_size integer,
	tile_size integer,
	selection_1 text,
	selection_2 text
); */

CREATE OR REPLACE FUNCTION get_unclipped_svg_tile_selection_2(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	brush_size integer,
	tile_size integer,
	selection text
)
RETURNS TABLE(
	id bigint,
	svg text
	)
AS
$func$
BEGIN
SELECT  
	row_number() over (ORDER BY osm_id) AS id,  
	ST_AsSVG(  
		ST_Scale(
			ST_Translate(
				ST_Simplify(
					way,
					1
				),
				-ul_x,
				-ul_y
			),
			1/((lr_x-ul_x)/tile_size),
			1/((ul_y-lr_y)/tile_size)
		),
		1, 
		0 
	) AS svg  
FROM planet_osm_line  
WHERE ST_Intersects ( 
	way, 
	ST_MakeEnvelope( 
		ul_x - ((lr_x-ul_x)/tile_size)*(brush_size/2),  
		ul_y + ((ul_y-lr_y)/tile_size)*(brush_size/2),  
		lr_x + ((lr_x-ul_x)/tile_size)*(brush_size/2),  
		lr_y - ((ul_y-lr_y)/tile_size)*(brush_size/2),
		900913 
	) 
)
AND || selection;
END;
$func$
LANGUAGE plpgsql STABLE;
ALTER FUNCTION get_unclipped_svg_tile_selection_2(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	brush_size integer,
	tile_size integer,
	selection text
	)
OWNER TO gis;