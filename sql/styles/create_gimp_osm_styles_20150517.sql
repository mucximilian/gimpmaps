CREATE TABLE style_brush
(
  id serial NOT NULL,
  brush character varying(20),
  CONSTRAINT style_brush_pk_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE style_brush
  OWNER TO gis;

CREATE TABLE style_color
(
  id serial NOT NULL,
  name character varying(20),
  color integer[],
  CONSTRAINT style_color_pk_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE style_color
  OWNER TO gis;

CREATE TABLE style_dynamics
(
  id serial NOT NULL,
  dynamics character varying(20),
  CONSTRAINT style_dynamics_pk_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE style_dynamics
  OWNER TO gis;

CREATE TABLE style_font
(
  id serial NOT NULL,
  name character varying(20),
  CONSTRAINT style_font_pk_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE style_font
  OWNER TO gis;

CREATE TABLE style_image
(
  id serial NOT NULL,
  name character varying(20),
  image character varying(50),
  opacity integer,
  CONSTRAINT style_image_pk_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE style_image
  OWNER TO gis;


CREATE TABLE style_line
(
  id serial NOT NULL,
  name character varying(50),
  brush integer,
  brush_size integer,
  dynamics integer,
  color integer,
  opacity integer,
  CONSTRAINT style_line_pk_id PRIMARY KEY (id),
  CONSTRAINT style_line_fk_brush FOREIGN KEY (brush)
      REFERENCES style_brush (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT style_line_fk_color FOREIGN KEY (color)
      REFERENCES style_color (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT style_line_fk_dynamics FOREIGN KEY (dynamics)
      REFERENCES style_dynamics (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE style_line
  OWNER TO gis;

 CREATE TABLE osm_feature
(
  id serial NOT NULL,
  tags text[],
  CONSTRAINT osm_feature_pk_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE osm_feature
  OWNER TO gis;

CREATE TABLE map_style
(
  id serial NOT NULL,
  name character varying(20),
  CONSTRAINT map_style_pk_image_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE map_style
  OWNER TO gis;

CREATE TABLE map_feature
(
  id serial NOT NULL,
  osm_feature integer,
  zoom_max integer,
  zoom_min integer,
  map_style integer,
  CONSTRAINT map_feature_pk_id PRIMARY KEY (id),
  CONSTRAINT map_feature_fk_map_style FOREIGN KEY (map_style)
      REFERENCES map_style (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_fk_osm_feature FOREIGN KEY (osm_feature)
      REFERENCES osm_feature (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE map_feature
  OWNER TO gis;

CREATE TABLE map_feature_line
(
  id serial NOT NULL,
  map_feature integer,
  style_line integer,
  z_order integer,
  CONSTRAINT map_feature_line_pk_id PRIMARY KEY (id),
  CONSTRAINT map_feature_line_fk_map_feature FOREIGN KEY (map_feature)
      REFERENCES map_feature (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_line_fk_style_line FOREIGN KEY (style_line)
      REFERENCES style_line (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE map_feature_line
  OWNER TO gis;

CREATE TABLE map_feature_polygon_hachure
(
  id serial NOT NULL,
  map_feature integer,
  style_line integer,
  style_hachure integer,
  z_order integer,
  CONSTRAINT map_feature_polygon_hachure_pk_id PRIMARY KEY (id),
  CONSTRAINT map_feature_polygon_hachure_fk_map_feature FOREIGN KEY (map_feature)
      REFERENCES map_feature (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_polygon_hachure_fk_style_hachure FOREIGN KEY (style_hachure)
      REFERENCES style_line (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_polygon_hachure_fk_style_line FOREIGN KEY (style_line)
      REFERENCES style_line (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE map_feature_polygon_hachure
  OWNER TO gis;

CREATE TABLE map_feature_polygon_image
(
  id serial NOT NULL,
  map_feature integer,
  style_line integer,
  style_image integer,
  z_order integer,
  CONSTRAINT map_feature_polygon_image_pk_id PRIMARY KEY (id),
  CONSTRAINT map_feature_polygon_image_fk_map_feature FOREIGN KEY (map_feature)
      REFERENCES map_feature (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_polygon_image_fk_style_image FOREIGN KEY (style_image)
      REFERENCES style_image (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_polygon_image_fk_style_line FOREIGN KEY (style_line)
      REFERENCES style_line (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE map_feature_polygon_image
  OWNER TO gis;

CREATE TABLE map_feature_text_point
(
  id serial NOT NULL,
  map_feature integer,
  style_line integer,
  style_color integer,
  CONSTRAINT map_feature_text_point_pk_id PRIMARY KEY (id),
  CONSTRAINT map_feature_text_point_fk_map_feature FOREIGN KEY (map_feature)
      REFERENCES map_feature (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_text_point_fk_style_color FOREIGN KEY (style_color)
      REFERENCES style_color (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_text_point_fk_style_line FOREIGN KEY (style_line)
      REFERENCES style_line (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE map_feature_text_point
  OWNER TO gis;

CREATE TABLE map_feature_text_polygon
(
  id serial NOT NULL,
  map_feature integer,
  style_line integer,
  style_color integer,
  CONSTRAINT map_feature_text_polygon_pk_id PRIMARY KEY (id),
  CONSTRAINT map_feature_text_polygon_fk_map_feature FOREIGN KEY (map_feature)
      REFERENCES map_feature (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_text_polygon_fk_style_color FOREIGN KEY (style_color)
      REFERENCES style_color (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT map_feature_text_polygon_fk_style_line FOREIGN KEY (style_line)
      REFERENCES style_line (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE map_feature_text_polygon
  OWNER TO gis;