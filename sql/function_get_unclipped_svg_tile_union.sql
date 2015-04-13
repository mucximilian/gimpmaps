/*DROP FUNCTION get_unclipped_svg_tile_union(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	brush_size integer,
	tile_size integer
);*/

CREATE OR REPLACE FUNCTION get_unclipped_svg_tile_union(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	brush_size integer,
	tile_size integer
)
RETURNS TABLE(
	id numeric,
	line_type text,
	svg text)
AS
$$
SELECT  
	SUM(osm_id) AS id,  
	concat(highway, route) AS line_type,
	ST_AsSVG(  
		ST_Scale(
			ST_Translate(
				ST_Simplify(
					ST_Union(way),
					1
				),
				-ul_x,
				-ul_y
			),
			1/((lr_x-ul_x)/tile_size),
			1/((ul_y-lr_y)/tile_size)
		),
		1, -- absolute or relative
		1 -- number of decimals
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
GROUP BY line_type, highway, route;
$$
LANGUAGE sql STABLE;
ALTER FUNCTION get_unclipped_svg_tile_union(
	ul_x numeric,
	ul_y numeric,
	lr_x numeric,
	lr_y numeric,
	brush_size integer,
	tile_size integer
	)
OWNER TO gis;