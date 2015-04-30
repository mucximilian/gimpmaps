--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.6
-- Dumped by pg_dump version 9.3.6
-- Started on 2015-04-30 18:24:24 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 182 (class 3079 OID 11789)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2048 (class 0 OID 0)
-- Dependencies: 182
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 195 (class 1255 OID 67767)
-- Name: get_line_tags_and_style(integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_line_tags_and_style(zoom_level integer) RETURNS TABLE(id integer, tags text[], z_order integer, brush character varying, brush_size numeric, color integer[], opacity integer, dnyamics character varying)
    LANGUAGE sql STABLE
    AS $$
SELECT
	f.id,
	f.tags,
	f.z_order,
	b.brush,
	s.brush_size,
	c.color,
	s.opacity,
	d.dynamics
FROM
	feature f
JOIN style s ON (f.style = s.id)
JOIN brush b ON (s.brush = b.id)
JOIN color c ON (s.color = c.id)
JOIN dynamics d ON (s.dynamics = d.id)
WHERE f.geometry = 2
AND f.zoom_max <= zoom_level
AND f.zoom_min >= zoom_level
ORDER BY f.z_order ASC
$$;


ALTER FUNCTION public.get_line_tags_and_style(zoom_level integer) OWNER TO gis;

--
-- TOC entry 196 (class 1255 OID 67768)
-- Name: get_polygon_tags_and_style(integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_polygon_tags_and_style(zoom_level integer) RETURNS TABLE(id integer, tags text[], z_order integer, brush character varying, brush_size numeric, color integer[], opacity_brush integer, dynamics character varying, image character varying, opacity_image integer)
    LANGUAGE sql STABLE
    AS $$
SELECT
	f.id,
	f.tags,
	f.z_order,
	b.brush,
	s.brush_size,
	c.color,
	s.opacity,
	d.dynamics,
	i.image,
	i.opacity AS opacity_image 
FROM 
	feature f
JOIN	
	style s 
ON (
	f.style = s.id
)
JOIN	
	brush b 
ON (
	s.brush = b.id
)
JOIN	
	color c
ON (
	s.color = c.id
)
JOIN	
	dynamics d 
ON (
	s.dynamics = d.id
)
JOIN
	image i
ON (
	f.style = i.style
)
WHERE f.geometry = 3
AND f.zoom_max <= zoom_level
AND f.zoom_min >= zoom_level
ORDER BY f.z_order DESC
$$;


ALTER FUNCTION public.get_polygon_tags_and_style(zoom_level integer) OWNER TO gis;

--
-- TOC entry 197 (class 1255 OID 67852)
-- Name: get_tags_and_style(integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_tags_and_style(zoom_level integer) RETURNS TABLE(id integer, geometry_type integer, tags text[], z_order integer, brush character varying, brush_size numeric, color integer[], opacity_brush integer, dynamics character varying, image character varying, opacity_image integer)
    LANGUAGE sql STABLE
    AS $$
SELECT
	f.id,
	f.geometry,
	f.tags,
	f.z_order,
	b.brush,
	s.brush_size,
	c.color,
	s.opacity,
	d.dynamics,
	i.image,
	i.opacity AS opacity_image 
FROM 
	(
	SELECT * 
	FROM feature 
	WHERE 
		zoom_max <= zoom_level
	AND 
		zoom_min >= zoom_level
	) f
LEFT JOIN	
	style s 
ON (
	f.style = s.id
)
LEFT JOIN	
	brush b 
ON (
	s.brush = b.id
)
LEFT JOIN	
	color c
ON (
	s.color = c.id
)
LEFT JOIN	
	dynamics d 
ON (
	s.dynamics = d.id
)
LEFT JOIN
	image i
ON (
	f.style = i.style
)
ORDER BY f.geometry, f.z_order ASC
$$;


ALTER FUNCTION public.get_tags_and_style(zoom_level integer) OWNER TO gis;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 67769)
-- Name: brush; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE brush (
    id integer NOT NULL,
    brush character varying(50)
);


ALTER TABLE public.brush OWNER TO gis;

--
-- TOC entry 171 (class 1259 OID 67772)
-- Name: brush_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE brush_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.brush_id_seq OWNER TO gis;

--
-- TOC entry 2049 (class 0 OID 0)
-- Dependencies: 171
-- Name: brush_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE brush_id_seq OWNED BY brush.id;


--
-- TOC entry 172 (class 1259 OID 67774)
-- Name: color; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE color (
    id integer NOT NULL,
    name character varying(20),
    color integer[]
);


ALTER TABLE public.color OWNER TO gis;

--
-- TOC entry 173 (class 1259 OID 67780)
-- Name: color_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE color_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.color_id_seq OWNER TO gis;

--
-- TOC entry 2050 (class 0 OID 0)
-- Dependencies: 173
-- Name: color_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE color_id_seq OWNED BY color.id;


--
-- TOC entry 174 (class 1259 OID 67782)
-- Name: dynamics; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE dynamics (
    id integer NOT NULL,
    dynamics character varying(20)
);


ALTER TABLE public.dynamics OWNER TO gis;

--
-- TOC entry 175 (class 1259 OID 67785)
-- Name: dynamics_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE dynamics_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dynamics_id_seq OWNER TO gis;

--
-- TOC entry 2051 (class 0 OID 0)
-- Dependencies: 175
-- Name: dynamics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE dynamics_id_seq OWNED BY dynamics.id;


--
-- TOC entry 176 (class 1259 OID 67787)
-- Name: feature; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE feature (
    id integer NOT NULL,
    geometry integer,
    tags text[],
    z_order integer,
    zoom_max integer,
    zoom_min integer,
    style integer
);


ALTER TABLE public.feature OWNER TO gis;

--
-- TOC entry 177 (class 1259 OID 67793)
-- Name: geometry; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE geometry (
    id integer NOT NULL,
    geometry character varying(12)
);


ALTER TABLE public.geometry OWNER TO gis;

--
-- TOC entry 178 (class 1259 OID 67796)
-- Name: image; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE image (
    id integer NOT NULL,
    style integer,
    name character varying(20),
    image character varying(50),
    opacity integer
);


ALTER TABLE public.image OWNER TO gis;

--
-- TOC entry 179 (class 1259 OID 67799)
-- Name: image_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_id_seq OWNER TO gis;

--
-- TOC entry 2052 (class 0 OID 0)
-- Dependencies: 179
-- Name: image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE image_id_seq OWNED BY image.id;


--
-- TOC entry 180 (class 1259 OID 67801)
-- Name: style; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style (
    id integer NOT NULL,
    name character varying(20),
    brush integer,
    brush_size numeric,
    dynamics integer,
    color integer,
    opacity integer
);


ALTER TABLE public.style OWNER TO gis;

--
-- TOC entry 181 (class 1259 OID 67807)
-- Name: style_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_id_seq OWNER TO gis;

--
-- TOC entry 2053 (class 0 OID 0)
-- Dependencies: 181
-- Name: style_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_id_seq OWNED BY style.id;


--
-- TOC entry 1899 (class 2604 OID 67809)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY brush ALTER COLUMN id SET DEFAULT nextval('brush_id_seq'::regclass);


--
-- TOC entry 1900 (class 2604 OID 67810)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY color ALTER COLUMN id SET DEFAULT nextval('color_id_seq'::regclass);


--
-- TOC entry 1901 (class 2604 OID 67811)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY dynamics ALTER COLUMN id SET DEFAULT nextval('dynamics_id_seq'::regclass);


--
-- TOC entry 1902 (class 2604 OID 67812)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY image ALTER COLUMN id SET DEFAULT nextval('image_id_seq'::regclass);


--
-- TOC entry 1903 (class 2604 OID 67813)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style ALTER COLUMN id SET DEFAULT nextval('style_id_seq'::regclass);


--
-- TOC entry 2029 (class 0 OID 67769)
-- Dependencies: 170
-- Data for Name: brush; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY brush (id, brush) FROM stdin;
1	GIMP Brush #7
2	Chalk 03
\.


--
-- TOC entry 2054 (class 0 OID 0)
-- Dependencies: 171
-- Name: brush_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('brush_id_seq', 2, true);


--
-- TOC entry 2031 (class 0 OID 67774)
-- Dependencies: 172
-- Data for Name: color; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY color (id, name, color) FROM stdin;
1	Grey 100	{100,100,100}
2	Grey 130	{130,130,130}
3	Grey 160	{160,160,160}
4	Green areas	{140,160,140}
5	Green forest	{120,140,120}
6	Grey 240	{240,240,240}
7	Blue	{100,160,255}
\.


--
-- TOC entry 2055 (class 0 OID 0)
-- Dependencies: 173
-- Name: color_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('color_id_seq', 7, true);


--
-- TOC entry 2033 (class 0 OID 67782)
-- Dependencies: 174
-- Data for Name: dynamics; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY dynamics (id, dynamics) FROM stdin;
1	Det3
\.


--
-- TOC entry 2056 (class 0 OID 0)
-- Dependencies: 175
-- Name: dynamics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('dynamics_id_seq', 1, true);


--
-- TOC entry 2035 (class 0 OID 67787)
-- Dependencies: 176
-- Data for Name: feature; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY feature (id, geometry, tags, z_order, zoom_max, zoom_min, style) FROM stdin;
1	2	{highway='motorway'}	1	5	20	1
2	2	{highway='motorway_link'}	2	5	20	1
3	2	{highway='primary'}	4	9	20	3
4	2	{highway='secondary'}	5	12	20	4
6	3	{landuse='village_green'}	3	10	20	6
8	3	{building='yes'}	1	14	20	5
9	2	{highway='primary_link'}	4	9	20	3
11	2	{highway='tertiary'}	6	12	20	4
10	2	{highway='trunk'}	5	12	20	4
5	2	{highway='trunk_link'}	3	5	20	3
13	2	{highway='secondary_link'}	6	14	20	4
12	2	{highway='tertiary_link'}	6	14	20	4
7	3	{"landuse='forest' OR leisure='park'"}	2	10	20	7
14	2	{"waterway='river' OR waterway='canal'",z_order>=0}	7	10	16	8
\.


--
-- TOC entry 2036 (class 0 OID 67793)
-- Dependencies: 177
-- Data for Name: geometry; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY geometry (id, geometry) FROM stdin;
1	point
2	line
3	polygon
\.


--
-- TOC entry 2037 (class 0 OID 67796)
-- Dependencies: 178
-- Data for Name: image; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY image (id, style, name, image, opacity) FROM stdin;
1	5	Buildings	hachure_grey_05.png	255
2	6	Green areas	hachure_green_060705.png	255
3	7	Forest and parks	hachure_green_040504.png	255
\.


--
-- TOC entry 2057 (class 0 OID 0)
-- Dependencies: 179
-- Name: image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('image_id_seq', 3, true);


--
-- TOC entry 2039 (class 0 OID 67801)
-- Dependencies: 180
-- Data for Name: style; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style (id, name, brush, brush_size, dynamics, color, opacity) FROM stdin;
2	Main roads	2	8	1	6	100
3	Medium roads	2	6	1	6	100
4	Small roads	2	4	1	6	100
5	Buildings	2	4	1	1	100
6	Green areas	2	4	1	4	100
7	Forest and Parks	2	4	1	5	100
1	Motorways	2	10	1	6	100
8	Rivers	2	6	1	7	100
\.


--
-- TOC entry 2058 (class 0 OID 0)
-- Dependencies: 181
-- Name: style_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_id_seq', 7, true);


--
-- TOC entry 1905 (class 2606 OID 67815)
-- Name: brush_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY brush
    ADD CONSTRAINT brush_pk_id PRIMARY KEY (id);


--
-- TOC entry 1907 (class 2606 OID 67817)
-- Name: color_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY color
    ADD CONSTRAINT color_pk_id PRIMARY KEY (id);


--
-- TOC entry 1909 (class 2606 OID 67819)
-- Name: dynamics_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY dynamics
    ADD CONSTRAINT dynamics_pk_id PRIMARY KEY (id);


--
-- TOC entry 1911 (class 2606 OID 67821)
-- Name: feature_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY feature
    ADD CONSTRAINT feature_pk_id PRIMARY KEY (id);


--
-- TOC entry 1913 (class 2606 OID 67823)
-- Name: geometry_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY geometry
    ADD CONSTRAINT geometry_pk_id PRIMARY KEY (id);


--
-- TOC entry 1915 (class 2606 OID 67825)
-- Name: image_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY image
    ADD CONSTRAINT image_pk_id PRIMARY KEY (id);


--
-- TOC entry 1917 (class 2606 OID 67827)
-- Name: style_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style
    ADD CONSTRAINT style_pk_id PRIMARY KEY (id);


--
-- TOC entry 1918 (class 2606 OID 67828)
-- Name: image_fk_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY image
    ADD CONSTRAINT image_fk_style FOREIGN KEY (style) REFERENCES style(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1919 (class 2606 OID 67833)
-- Name: style_fk_brush; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style
    ADD CONSTRAINT style_fk_brush FOREIGN KEY (brush) REFERENCES brush(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1920 (class 2606 OID 67838)
-- Name: style_fk_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style
    ADD CONSTRAINT style_fk_color FOREIGN KEY (color) REFERENCES color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1921 (class 2606 OID 67843)
-- Name: style_fk_dynamics; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style
    ADD CONSTRAINT style_fk_dynamics FOREIGN KEY (dynamics) REFERENCES dynamics(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2047 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-04-30 18:24:24 CEST

--
-- PostgreSQL database dump complete
--

