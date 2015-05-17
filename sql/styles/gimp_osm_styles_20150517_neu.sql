--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.6
-- Dumped by pg_dump version 9.3.6
-- Started on 2015-05-17 00:53:38 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 197 (class 3079 OID 11789)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2139 (class 0 OID 0)
-- Dependencies: 197
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 210 (class 1255 OID 72282)
-- Name: get_tags_and_style(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_tags_and_style(map_style integer, zoom_level integer) RETURNS TABLE(id integer, geometry_type integer, tags text[], z_order integer, brush character varying, brush_size integer, color integer[], opacity_brush integer, dynamics character varying, image character varying, opacity_image integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	s.id,
	f.geometry,
	f.tags,
	f.z_order,
	b.brush,
	fs.brush_size,
	c.color,
	fs.opacity,
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
	feature_style fs
ON (
	s.feature_style = fs.id
)
LEFT JOIN	
	brush b 
ON (
	fs.brush = b.id
)
LEFT JOIN	
	color c
ON (
	fs.color = c.id
)
LEFT JOIN	
	dynamics d 
ON (
	fs.dynamics = d.id
)
LEFT JOIN
	image i
ON (
	s.feature_style = i.style
)
WHERE s.map_style = $1
AND f.zoom_max <= $2
AND f.zoom_min >= $2
ORDER BY f.geometry, f.z_order ASC
$_$;


ALTER FUNCTION public.get_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

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
-- TOC entry 2140 (class 0 OID 0)
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
-- TOC entry 2141 (class 0 OID 0)
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
-- TOC entry 2142 (class 0 OID 0)
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
    feature_type integer,
    tags text[],
    z_order integer,
    zoom_max integer,
    zoom_min integer
);


ALTER TABLE public.feature OWNER TO gis;

--
-- TOC entry 196 (class 1259 OID 72606)
-- Name: feature_id_n_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE feature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.feature_id_seq OWNER TO gis;

--
-- TOC entry 2143 (class 0 OID 0)
-- Dependencies: 196
-- Name: feature_id_n_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE feature_id_seq OWNED BY feature.id_n;


--
-- TOC entry 177 (class 1259 OID 67793)
-- Name: feature_type; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE feature_type (
    id integer NOT NULL,
    type character varying(12)
);


ALTER TABLE public.feature_type OWNER TO gis;

--
-- TOC entry 187 (class 1259 OID 72413)
-- Name: font; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE font (
    id integer NOT NULL,
    name character varying(20)
);


ALTER TABLE public.font OWNER TO gis;

--
-- TOC entry 186 (class 1259 OID 72411)
-- Name: font_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE font_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.font_id_seq OWNER TO gis;

--
-- TOC entry 2144 (class 0 OID 0)
-- Dependencies: 186
-- Name: font_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE font_id_seq OWNED BY font.id;


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
-- TOC entry 2145 (class 0 OID 0)
-- Dependencies: 179
-- Name: image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE image_id_seq OWNED BY image.id;


--
-- TOC entry 183 (class 1259 OID 72206)
-- Name: map_style; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_style (
    id integer NOT NULL,
    name character varying(20)
);


ALTER TABLE public.map_style OWNER TO gis;

--
-- TOC entry 182 (class 1259 OID 72204)
-- Name: map_style_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE map_style_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_style_id_seq OWNER TO gis;

--
-- TOC entry 2146 (class 0 OID 0)
-- Dependencies: 182
-- Name: map_style_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_style_id_seq OWNED BY map_style.id;


--
-- TOC entry 185 (class 1259 OID 72217)
-- Name: styling; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE styling (
    id integer NOT NULL,
    map_style integer,
    feature integer,
    feature_style integer
);


ALTER TABLE public.styling OWNER TO gis;

--
-- TOC entry 184 (class 1259 OID 72215)
-- Name: render_styling_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE render_styling_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.render_styling_id_seq OWNER TO gis;

--
-- TOC entry 2147 (class 0 OID 0)
-- Dependencies: 184
-- Name: render_styling_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE render_styling_id_seq OWNED BY styling.id;


--
-- TOC entry 195 (class 1259 OID 72588)
-- Name: style_background; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_background (
    id integer NOT NULL,
    name character varying(20),
    image integer
);


ALTER TABLE public.style_background OWNER TO gis;

--
-- TOC entry 194 (class 1259 OID 72586)
-- Name: style_background_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_background_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_background_id_seq OWNER TO gis;

--
-- TOC entry 2148 (class 0 OID 0)
-- Dependencies: 194
-- Name: style_background_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_background_id_seq OWNED BY style_background.id;


--
-- TOC entry 180 (class 1259 OID 67801)
-- Name: style_line; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_line (
    id integer NOT NULL,
    name character varying(20),
    brush integer,
    brush_size integer,
    dynamics integer,
    color integer,
    opacity integer
);


ALTER TABLE public.style_line OWNER TO gis;

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
-- TOC entry 2149 (class 0 OID 0)
-- Dependencies: 181
-- Name: style_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_id_seq OWNED BY style_line.id;


--
-- TOC entry 189 (class 1259 OID 72491)
-- Name: style_polygon_hachure; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_polygon_hachure (
    id integer NOT NULL,
    name character varying(20),
    outline integer,
    hachure integer
);


ALTER TABLE public.style_polygon_hachure OWNER TO gis;

--
-- TOC entry 188 (class 1259 OID 72489)
-- Name: style_polygon_hachure_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_polygon_hachure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_polygon_hachure_id_seq OWNER TO gis;

--
-- TOC entry 2150 (class 0 OID 0)
-- Dependencies: 188
-- Name: style_polygon_hachure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_polygon_hachure_id_seq OWNED BY style_polygon_hachure.id;


--
-- TOC entry 191 (class 1259 OID 72509)
-- Name: style_polygon_image; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_polygon_image (
    id integer NOT NULL,
    name character varying(20),
    outline integer,
    image integer
);


ALTER TABLE public.style_polygon_image OWNER TO gis;

--
-- TOC entry 190 (class 1259 OID 72507)
-- Name: style_polygon_image_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_polygon_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_polygon_image_id_seq OWNER TO gis;

--
-- TOC entry 2151 (class 0 OID 0)
-- Dependencies: 190
-- Name: style_polygon_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_polygon_image_id_seq OWNED BY style_polygon_image.id;


--
-- TOC entry 193 (class 1259 OID 72565)
-- Name: style_text; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_text (
    id integer NOT NULL,
    name character varying(20),
    outline integer,
    color integer,
    font integer,
    font_size integer
);


ALTER TABLE public.style_text OWNER TO gis;

--
-- TOC entry 192 (class 1259 OID 72563)
-- Name: style_text_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_text_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_text_id_seq OWNER TO gis;

--
-- TOC entry 2152 (class 0 OID 0)
-- Dependencies: 192
-- Name: style_text_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_text_id_seq OWNED BY style_text.id;


--
-- TOC entry 1941 (class 2604 OID 67809)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY brush ALTER COLUMN id SET DEFAULT nextval('brush_id_seq'::regclass);


--
-- TOC entry 1942 (class 2604 OID 67810)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY color ALTER COLUMN id SET DEFAULT nextval('color_id_seq'::regclass);


--
-- TOC entry 1943 (class 2604 OID 67811)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY dynamics ALTER COLUMN id SET DEFAULT nextval('dynamics_id_seq'::regclass);


--
-- TOC entry 1944 (class 2604 OID 72608)
-- Name: id_n; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY feature ALTER COLUMN id_n SET DEFAULT nextval('feature_id_seq'::regclass);


--
-- TOC entry 1949 (class 2604 OID 72416)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY font ALTER COLUMN id SET DEFAULT nextval('font_id_seq'::regclass);


--
-- TOC entry 1945 (class 2604 OID 67812)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY image ALTER COLUMN id SET DEFAULT nextval('image_id_seq'::regclass);


--
-- TOC entry 1947 (class 2604 OID 72209)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_style ALTER COLUMN id SET DEFAULT nextval('map_style_id_seq'::regclass);


--
-- TOC entry 1953 (class 2604 OID 72591)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_background ALTER COLUMN id SET DEFAULT nextval('style_background_id_seq'::regclass);


--
-- TOC entry 1946 (class 2604 OID 67813)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line ALTER COLUMN id SET DEFAULT nextval('style_id_seq'::regclass);


--
-- TOC entry 1950 (class 2604 OID 72494)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_polygon_hachure ALTER COLUMN id SET DEFAULT nextval('style_polygon_hachure_id_seq'::regclass);


--
-- TOC entry 1951 (class 2604 OID 72512)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_polygon_image ALTER COLUMN id SET DEFAULT nextval('style_polygon_image_id_seq'::regclass);


--
-- TOC entry 1952 (class 2604 OID 72568)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_text ALTER COLUMN id SET DEFAULT nextval('style_text_id_seq'::regclass);


--
-- TOC entry 1948 (class 2604 OID 72220)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY styling ALTER COLUMN id SET DEFAULT nextval('render_styling_id_seq'::regclass);


--
-- TOC entry 2105 (class 0 OID 67769)
-- Dependencies: 170
-- Data for Name: brush; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY brush (id, brush) FROM stdin;
1	GIMP Brush #7
2	Chalk 03
3	Oils 02
\.


--
-- TOC entry 2153 (class 0 OID 0)
-- Dependencies: 171
-- Name: brush_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('brush_id_seq', 3, true);


--
-- TOC entry 2107 (class 0 OID 67774)
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
8	Orange	{255,180,100}
9	Green	{100,140,60}
\.


--
-- TOC entry 2154 (class 0 OID 0)
-- Dependencies: 173
-- Name: color_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('color_id_seq', 9, true);


--
-- TOC entry 2109 (class 0 OID 67782)
-- Dependencies: 174
-- Data for Name: dynamics; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY dynamics (id, dynamics) FROM stdin;
1	Det3
\.


--
-- TOC entry 2155 (class 0 OID 0)
-- Dependencies: 175
-- Name: dynamics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('dynamics_id_seq', 1, true);


--
-- TOC entry 2111 (class 0 OID 67787)
-- Dependencies: 176
-- Data for Name: feature; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY feature (id, feature_type, tags, z_order, zoom_max, zoom_min) FROM stdin;
1	2	{highway='motorway'}	1	5	20
2	2	{highway='motorway_link'}	2	5	20
3	2	{highway='primary'}	4	9	20
4	2	{highway='secondary'}	5	12	20
12	2	{highway='tertiary_link'}	6	14	20
14	2	{waterway='river'}	7	10	16
15	3	{waterway='riverbank'}	1	17	20
5	2	{highway='trunk_link'}	3	5	20
6	3	{landuse='village_green'}	3	10	20
7	3	{"landuse='forest' OR leisure='park'"}	2	10	20
8	3	{building='yes'}	1	14	20
9	2	{highway='primary_link'}	4	9	20
10	2	{highway='trunk'}	5	12	20
11	2	{highway='tertiary'}	6	12	20
13	2	{highway='secondary_link'}	6	14	20
\.


--
-- TOC entry 2156 (class 0 OID 0)
-- Dependencies: 196
-- Name: feature_id_n_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('feature_id_seq', 15, true);


--
-- TOC entry 2112 (class 0 OID 67793)
-- Dependencies: 177
-- Data for Name: feature_type; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY feature_type (id, type) FROM stdin;
1	point
2	line
3	polygon
\.


--
-- TOC entry 2122 (class 0 OID 72413)
-- Dependencies: 187
-- Data for Name: font; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY font (id, name) FROM stdin;
1	Arial
\.


--
-- TOC entry 2157 (class 0 OID 0)
-- Dependencies: 186
-- Name: font_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('font_id_seq', 1, true);


--
-- TOC entry 2113 (class 0 OID 67796)
-- Dependencies: 178
-- Data for Name: image; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY image (id, style, name, image, opacity) FROM stdin;
1	5	Buildings	hachure_grey_05.png	255
2	6	Green areas	hachure_green_060705.png	255
3	7	Forest and parks	hachure_green_040504.png	255
\.


--
-- TOC entry 2158 (class 0 OID 0)
-- Dependencies: 179
-- Name: image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('image_id_seq', 3, true);


--
-- TOC entry 2118 (class 0 OID 72206)
-- Dependencies: 183
-- Data for Name: map_style; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_style (id, name) FROM stdin;
1	Test Tiles
2	Chalk Tiles
3	Chalk Map
4	Oil Tiles
5	Oil Map
\.


--
-- TOC entry 2159 (class 0 OID 0)
-- Dependencies: 182
-- Name: map_style_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_style_id_seq', 5, true);


--
-- TOC entry 2160 (class 0 OID 0)
-- Dependencies: 184
-- Name: render_styling_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('render_styling_id_seq', 20, true);


--
-- TOC entry 2130 (class 0 OID 72588)
-- Dependencies: 195
-- Data for Name: style_background; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_background (id, name, image) FROM stdin;
\.


--
-- TOC entry 2161 (class 0 OID 0)
-- Dependencies: 194
-- Name: style_background_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_background_id_seq', 1, false);


--
-- TOC entry 2162 (class 0 OID 0)
-- Dependencies: 181
-- Name: style_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_id_seq', 7, true);


--
-- TOC entry 2115 (class 0 OID 67801)
-- Dependencies: 180
-- Data for Name: style_line; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_line (id, name, brush, brush_size, dynamics, color, opacity) FROM stdin;
1	Motorways	3	10	1	8	100
2	Main roads	3	8	1	6	100
3	Medium roads	3	6	1	6	100
4	Small roads	3	4	1	6	100
5	Buildings	3	4	1	1	100
8	Rivers	3	6	1	7	100
6	Green areas	3	4	1	9	100
7	Forest and Parks	3	4	1	9	100
\.


--
-- TOC entry 2124 (class 0 OID 72491)
-- Dependencies: 189
-- Data for Name: style_polygon_hachure; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_polygon_hachure (id, name, outline, hachure) FROM stdin;
\.


--
-- TOC entry 2163 (class 0 OID 0)
-- Dependencies: 188
-- Name: style_polygon_hachure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_polygon_hachure_id_seq', 1, false);


--
-- TOC entry 2126 (class 0 OID 72509)
-- Dependencies: 191
-- Data for Name: style_polygon_image; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_polygon_image (id, name, outline, image) FROM stdin;
\.


--
-- TOC entry 2164 (class 0 OID 0)
-- Dependencies: 190
-- Name: style_polygon_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_polygon_image_id_seq', 1, false);


--
-- TOC entry 2128 (class 0 OID 72565)
-- Dependencies: 193
-- Data for Name: style_text; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_text (id, name, outline, color, font, font_size) FROM stdin;
\.


--
-- TOC entry 2165 (class 0 OID 0)
-- Dependencies: 192
-- Name: style_text_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_text_id_seq', 1, false);


--
-- TOC entry 2120 (class 0 OID 72217)
-- Dependencies: 185
-- Data for Name: styling; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY styling (id, map_style, feature, feature_style) FROM stdin;
1	1	1	1
2	1	2	1
3	1	3	2
5	1	4	3
6	1	13	3
4	1	9	2
7	1	11	4
8	1	12	4
9	1	10	4
10	1	5	4
11	1	6	6
12	1	7	7
13	1	8	5
14	1	14	8
17	1	15	8
18	2	1	8
19	2	2	8
20	2	3	8
\.


--
-- TOC entry 1955 (class 2606 OID 67815)
-- Name: brush_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY brush
    ADD CONSTRAINT brush_pk_id PRIMARY KEY (id);


--
-- TOC entry 1957 (class 2606 OID 67817)
-- Name: color_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY color
    ADD CONSTRAINT color_pk_id PRIMARY KEY (id);


--
-- TOC entry 1959 (class 2606 OID 67819)
-- Name: dynamics_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY dynamics
    ADD CONSTRAINT dynamics_pk_id PRIMARY KEY (id);


--
-- TOC entry 1961 (class 2606 OID 67821)
-- Name: feature_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY feature
    ADD CONSTRAINT feature_pk_id PRIMARY KEY (id);


--
-- TOC entry 1973 (class 2606 OID 72562)
-- Name: font_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY font
    ADD CONSTRAINT font_pk_id PRIMARY KEY (id);


--
-- TOC entry 1963 (class 2606 OID 67823)
-- Name: geometry_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY feature_type
    ADD CONSTRAINT geometry_pk_id PRIMARY KEY (id);


--
-- TOC entry 1965 (class 2606 OID 67825)
-- Name: image_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY image
    ADD CONSTRAINT image_pk_id PRIMARY KEY (id);


--
-- TOC entry 1969 (class 2606 OID 72211)
-- Name: pk_map_style_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_style
    ADD CONSTRAINT pk_map_style_id PRIMARY KEY (id);


--
-- TOC entry 1981 (class 2606 OID 72593)
-- Name: style_background_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_background
    ADD CONSTRAINT style_background_pk_id PRIMARY KEY (id);


--
-- TOC entry 1967 (class 2606 OID 67827)
-- Name: style_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_pk_id PRIMARY KEY (id);


--
-- TOC entry 1975 (class 2606 OID 72496)
-- Name: style_polygon_hachure_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_polygon_hachure
    ADD CONSTRAINT style_polygon_hachure_pk_id PRIMARY KEY (id);


--
-- TOC entry 1977 (class 2606 OID 72514)
-- Name: style_polygon_image_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_polygon_image
    ADD CONSTRAINT style_polygon_image_pk_id PRIMARY KEY (id);


--
-- TOC entry 1979 (class 2606 OID 72570)
-- Name: style_text_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_text
    ADD CONSTRAINT style_text_pk_id PRIMARY KEY (id);


--
-- TOC entry 1971 (class 2606 OID 72222)
-- Name: styling_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY styling
    ADD CONSTRAINT styling_pk_id PRIMARY KEY (id);


--
-- TOC entry 1982 (class 2606 OID 72599)
-- Name: feature_fk_feature_type; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY feature
    ADD CONSTRAINT feature_fk_feature_type FOREIGN KEY (feature_type) REFERENCES feature_type(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1983 (class 2606 OID 67828)
-- Name: image_fk_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY image
    ADD CONSTRAINT image_fk_style FOREIGN KEY (style) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1997 (class 2606 OID 72594)
-- Name: style_background_fk_image; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_background
    ADD CONSTRAINT style_background_fk_image FOREIGN KEY (image) REFERENCES image(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1984 (class 2606 OID 67833)
-- Name: style_fk_brush; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_fk_brush FOREIGN KEY (brush) REFERENCES brush(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1985 (class 2606 OID 67838)
-- Name: style_fk_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_fk_color FOREIGN KEY (color) REFERENCES color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1986 (class 2606 OID 67843)
-- Name: style_fk_dynamics; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_fk_dynamics FOREIGN KEY (dynamics) REFERENCES dynamics(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1991 (class 2606 OID 72502)
-- Name: style_polygon_hachure_fk_hachure; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_polygon_hachure
    ADD CONSTRAINT style_polygon_hachure_fk_hachure FOREIGN KEY (hachure) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1990 (class 2606 OID 72497)
-- Name: style_polygon_hachure_fk_outline; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_polygon_hachure
    ADD CONSTRAINT style_polygon_hachure_fk_outline FOREIGN KEY (outline) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1993 (class 2606 OID 72520)
-- Name: style_polygon_image_fk_image; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_polygon_image
    ADD CONSTRAINT style_polygon_image_fk_image FOREIGN KEY (image) REFERENCES image(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1992 (class 2606 OID 72515)
-- Name: style_polygon_image_fk_outline; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_polygon_image
    ADD CONSTRAINT style_polygon_image_fk_outline FOREIGN KEY (outline) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1995 (class 2606 OID 72576)
-- Name: style_text_fk_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_text
    ADD CONSTRAINT style_text_fk_color FOREIGN KEY (color) REFERENCES color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1996 (class 2606 OID 72581)
-- Name: style_text_fk_font; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_text
    ADD CONSTRAINT style_text_fk_font FOREIGN KEY (font) REFERENCES font(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1994 (class 2606 OID 72571)
-- Name: style_text_fk_outline; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_text
    ADD CONSTRAINT style_text_fk_outline FOREIGN KEY (outline) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1988 (class 2606 OID 72228)
-- Name: styling_fk_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY styling
    ADD CONSTRAINT styling_fk_feature FOREIGN KEY (feature) REFERENCES feature(id);


--
-- TOC entry 1989 (class 2606 OID 72238)
-- Name: styling_fk_feature_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY styling
    ADD CONSTRAINT styling_fk_feature_style FOREIGN KEY (feature_style) REFERENCES style_line(id);


--
-- TOC entry 1987 (class 2606 OID 72223)
-- Name: styling_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY styling
    ADD CONSTRAINT styling_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2138 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-05-17 00:53:38 CEST

--
-- PostgreSQL database dump complete
--

