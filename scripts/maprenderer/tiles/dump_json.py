import json
import psycopg2

conn = psycopg2.connect('dbname=gimp_osm_styles '
                	'user=gis '
                	'password=gis '
                	'host=localhost '
                	'port=5432')
    
curs = conn.cursor()

sql = """
SELECT 
	row_to_json(z)
FROM (
	SELECT
		'12' AS zoom,
		(
		SELECT 
			array_to_json(array_agg(row_to_json(t))) AS lines
		FROM (
			SELECT 
				(
				SELECT geometry 
				FROM geometry 
				WHERE id = feature.geometry
				),
				tags,
				z_level,
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
		) t
	)
) z
    """   
                        
curs.execute(sql)

for row in curs.fetchall():
    json_string = row[0]    
    print json_string
    data = json.loads(json_string)

with open('style.json', 'w') as outfile:
    json.dump(data, outfile)