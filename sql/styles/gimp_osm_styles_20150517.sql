--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.6
-- Dumped by pg_dump version 9.3.6
-- Started on 2015-05-18 01:49:12 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 198 (class 3079 OID 11789)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2152 (class 0 OID 0)
-- Dependencies: 198
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 211 (class 1255 OID 74403)
-- Name: get_line_tags_and_style(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_line_tags_and_style(map_style integer, zoom_level integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, z_order integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mfl.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	sc.color,
	sd.dynamics,	
	of.z_order
FROM
	map_feature_line mfl
LEFT JOIN
	style_line sl
ON (
	mfl.style_line = sl.id
)
LEFT JOIN 
	style_brush sb
ON (
	sl.brush = sb.id
)
LEFT JOIN style_dynamics sd
ON (
	sl.dynamics = sd.id
)
LEFT JOIN style_color sc
ON (
	sl.color = sc.id
)
LEFT JOIN osm_feature of
ON (
	mfl.osm_feature = of.id
)
WHERE mfl.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$_$;


ALTER FUNCTION public.get_line_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

--
-- TOC entry 212 (class 1255 OID 74404)
-- Name: get_polygon_hachure_tags_and_style(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_polygon_hachure_tags_and_style(map_style integer, zoom_level integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, brush_hachure character varying, brush_hachure_size integer, color_hachure integer[], dynamics_hachure character varying, z_order integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mfph.id,
	of.tags,
	slb.brush,
	sl.brush_size,
	slc.color,
	sld.dynamics,
	shb.brush,
	sh.brush_size,
	shc.color,
	shd.dynamics,
	of.z_order
FROM
	map_feature_polygon_hachure mfph
LEFT JOIN
	style_line sl
ON (
	mfph.style_line = sl.id
)
LEFT JOIN 
	style_brush slb
ON (
	sl.brush = slb.id
)
LEFT JOIN style_color slc
ON (
	sl.color = slc.id
)
LEFT JOIN style_dynamics sld
ON (
	sl.dynamics = sld.id
)
LEFT JOIN
	style_line sh
ON (
	mfph.style_hachure = sh.id
)
LEFT JOIN 
	style_brush shb
ON (
	sl.brush = shb.id
)
LEFT JOIN style_color shc
ON (
	sh.color = shc.id
)
LEFT JOIN style_dynamics shd
ON (
	sl.dynamics = shd.id
)
LEFT JOIN osm_feature of
ON (
	mfph.osm_feature = of.id
)
WHERE mfph.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$_$;


ALTER FUNCTION public.get_polygon_hachure_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

--
-- TOC entry 213 (class 1255 OID 74410)
-- Name: get_polygon_image_tags_and_style(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_polygon_image_tags_and_style(map_style integer, zoom_level integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, image character varying, z_order integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mfpi.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	sc.color,
	sd.dynamics,
	si.image,
	of.z_order
FROM
	map_feature_polygon_image mfpi
LEFT JOIN
	style_line sl
ON (
	mfpi.style_line = sl.id
)
LEFT JOIN 
	style_brush sb
ON (
	sl.brush = sb.id
)
LEFT JOIN style_color sc
ON (
	sl.color = sc.id
)
LEFT JOIN style_dynamics sd
ON (
	sl.dynamics = sd.id
)
LEFT JOIN style_image si
ON (
	mfpi.style_image = si.id
)
LEFT JOIN osm_feature of
ON (
	mfpi.osm_feature = of.id
)
WHERE mfpi.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$_$;


ALTER FUNCTION public.get_polygon_image_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

--
-- TOC entry 214 (class 1255 OID 74414)
-- Name: get_text_polygon_tags_and_style(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_text_polygon_tags_and_style(map_style integer, zoom_level integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, style_color integer, z_order integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mftp.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	slc.color,
	sd.dynamics,
	mftp.style_color,
	of.z_order
FROM
	map_feature_text_polygon mftp
LEFT JOIN
	style_line sl
ON (
	mftp.style_line = sl.id
)
LEFT JOIN 
	style_brush sb
ON (
	sl.brush = sb.id
)
LEFT JOIN style_color slc
ON (
	sl.color = slc.id
)
LEFT JOIN style_dynamics sd
ON (
	sl.dynamics = sd.id
)
LEFT JOIN style_color sc
ON (
	mftp.style_color = sc.id
)
LEFT JOIN osm_feature of
ON (
	mftp.osm_feature = of.id
)
WHERE mftp.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order ASC
$_$;


ALTER FUNCTION public.get_text_polygon_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 197 (class 1259 OID 74359)
-- Name: map_feature_line; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_feature_line (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    map_style integer
);


ALTER TABLE public.map_feature_line OWNER TO gis;

--
-- TOC entry 196 (class 1259 OID 74357)
-- Name: map_feature_line_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE map_feature_line_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_feature_line_id_seq OWNER TO gis;

--
-- TOC entry 2153 (class 0 OID 0)
-- Dependencies: 196
-- Name: map_feature_line_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_line_id_seq OWNED BY map_feature_line.id;


--
-- TOC entry 195 (class 1259 OID 74336)
-- Name: map_feature_polygon_hachure; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_feature_polygon_hachure (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    style_hachure integer,
    map_style integer
);


ALTER TABLE public.map_feature_polygon_hachure OWNER TO gis;

--
-- TOC entry 194 (class 1259 OID 74334)
-- Name: map_feature_polygon_hachure_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE map_feature_polygon_hachure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_feature_polygon_hachure_id_seq OWNER TO gis;

--
-- TOC entry 2154 (class 0 OID 0)
-- Dependencies: 194
-- Name: map_feature_polygon_hachure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_polygon_hachure_id_seq OWNED BY map_feature_polygon_hachure.id;


--
-- TOC entry 193 (class 1259 OID 74313)
-- Name: map_feature_polygon_image; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_feature_polygon_image (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    style_image integer,
    map_style integer
);


ALTER TABLE public.map_feature_polygon_image OWNER TO gis;

--
-- TOC entry 192 (class 1259 OID 74311)
-- Name: map_feature_polygon_image_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE map_feature_polygon_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_feature_polygon_image_id_seq OWNER TO gis;

--
-- TOC entry 2155 (class 0 OID 0)
-- Dependencies: 192
-- Name: map_feature_polygon_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_polygon_image_id_seq OWNED BY map_feature_polygon_image.id;


--
-- TOC entry 191 (class 1259 OID 74290)
-- Name: map_feature_text_point; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_feature_text_point (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    style_color integer,
    map_style integer
);


ALTER TABLE public.map_feature_text_point OWNER TO gis;

--
-- TOC entry 190 (class 1259 OID 74288)
-- Name: map_feature_text_point_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE map_feature_text_point_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_feature_text_point_id_seq OWNER TO gis;

--
-- TOC entry 2156 (class 0 OID 0)
-- Dependencies: 190
-- Name: map_feature_text_point_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_text_point_id_seq OWNED BY map_feature_text_point.id;


--
-- TOC entry 189 (class 1259 OID 74267)
-- Name: map_feature_text_polygon; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_feature_text_polygon (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    style_color integer,
    map_style integer
);


ALTER TABLE public.map_feature_text_polygon OWNER TO gis;

--
-- TOC entry 188 (class 1259 OID 74265)
-- Name: map_feature_text_polygon_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE map_feature_text_polygon_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_feature_text_polygon_id_seq OWNER TO gis;

--
-- TOC entry 2157 (class 0 OID 0)
-- Dependencies: 188
-- Name: map_feature_text_polygon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_text_polygon_id_seq OWNED BY map_feature_text_polygon.id;


--
-- TOC entry 185 (class 1259 OID 74117)
-- Name: map_style; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_style (
    id integer NOT NULL,
    name character varying(20)
);


ALTER TABLE public.map_style OWNER TO gis;

--
-- TOC entry 184 (class 1259 OID 74115)
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
-- TOC entry 2158 (class 0 OID 0)
-- Dependencies: 184
-- Name: map_style_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_style_id_seq OWNED BY map_style.id;


--
-- TOC entry 183 (class 1259 OID 74106)
-- Name: osm_feature; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE osm_feature (
    id integer NOT NULL,
    tags text[],
    feature_type integer,
    zoom_max integer,
    zoom_min integer,
    z_order integer
);


ALTER TABLE public.osm_feature OWNER TO gis;

--
-- TOC entry 182 (class 1259 OID 74104)
-- Name: osm_feature_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE osm_feature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.osm_feature_id_seq OWNER TO gis;

--
-- TOC entry 2159 (class 0 OID 0)
-- Dependencies: 182
-- Name: osm_feature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE osm_feature_id_seq OWNED BY osm_feature.id;


--
-- TOC entry 187 (class 1259 OID 74254)
-- Name: osm_feature_type; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE osm_feature_type (
    id integer NOT NULL,
    name character varying(10)
);


ALTER TABLE public.osm_feature_type OWNER TO gis;

--
-- TOC entry 186 (class 1259 OID 74252)
-- Name: osm_feature_type_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE osm_feature_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.osm_feature_type_id_seq OWNER TO gis;

--
-- TOC entry 2160 (class 0 OID 0)
-- Dependencies: 186
-- Name: osm_feature_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE osm_feature_type_id_seq OWNED BY osm_feature_type.id;


--
-- TOC entry 171 (class 1259 OID 74040)
-- Name: style_brush; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_brush (
    id integer NOT NULL,
    brush character varying(20)
);


ALTER TABLE public.style_brush OWNER TO gis;

--
-- TOC entry 170 (class 1259 OID 74038)
-- Name: style_brush_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_brush_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_brush_id_seq OWNER TO gis;

--
-- TOC entry 2161 (class 0 OID 0)
-- Dependencies: 170
-- Name: style_brush_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_brush_id_seq OWNED BY style_brush.id;


--
-- TOC entry 173 (class 1259 OID 74048)
-- Name: style_color; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_color (
    id integer NOT NULL,
    name character varying(20),
    color integer[]
);


ALTER TABLE public.style_color OWNER TO gis;

--
-- TOC entry 172 (class 1259 OID 74046)
-- Name: style_color_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_color_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_color_id_seq OWNER TO gis;

--
-- TOC entry 2162 (class 0 OID 0)
-- Dependencies: 172
-- Name: style_color_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_color_id_seq OWNED BY style_color.id;


--
-- TOC entry 175 (class 1259 OID 74059)
-- Name: style_dynamics; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_dynamics (
    id integer NOT NULL,
    dynamics character varying(20)
);


ALTER TABLE public.style_dynamics OWNER TO gis;

--
-- TOC entry 174 (class 1259 OID 74057)
-- Name: style_dynamics_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_dynamics_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_dynamics_id_seq OWNER TO gis;

--
-- TOC entry 2163 (class 0 OID 0)
-- Dependencies: 174
-- Name: style_dynamics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_dynamics_id_seq OWNED BY style_dynamics.id;


--
-- TOC entry 177 (class 1259 OID 74067)
-- Name: style_font; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_font (
    id integer NOT NULL,
    name character varying(20)
);


ALTER TABLE public.style_font OWNER TO gis;

--
-- TOC entry 176 (class 1259 OID 74065)
-- Name: style_font_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_font_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_font_id_seq OWNER TO gis;

--
-- TOC entry 2164 (class 0 OID 0)
-- Dependencies: 176
-- Name: style_font_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_font_id_seq OWNED BY style_font.id;


--
-- TOC entry 179 (class 1259 OID 74075)
-- Name: style_image; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_image (
    id integer NOT NULL,
    name character varying(20),
    image character varying(50),
    opacity integer
);


ALTER TABLE public.style_image OWNER TO gis;

--
-- TOC entry 178 (class 1259 OID 74073)
-- Name: style_image_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_image_id_seq OWNER TO gis;

--
-- TOC entry 2165 (class 0 OID 0)
-- Dependencies: 178
-- Name: style_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_image_id_seq OWNED BY style_image.id;


--
-- TOC entry 181 (class 1259 OID 74083)
-- Name: style_line; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_line (
    id integer NOT NULL,
    name character varying(50),
    brush integer,
    brush_size integer,
    dynamics integer,
    color integer,
    opacity integer
);


ALTER TABLE public.style_line OWNER TO gis;

--
-- TOC entry 180 (class 1259 OID 74081)
-- Name: style_line_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_line_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_line_id_seq OWNER TO gis;

--
-- TOC entry 2166 (class 0 OID 0)
-- Dependencies: 180
-- Name: style_line_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_line_id_seq OWNED BY style_line.id;


--
-- TOC entry 1958 (class 2604 OID 74362)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line ALTER COLUMN id SET DEFAULT nextval('map_feature_line_id_seq'::regclass);


--
-- TOC entry 1957 (class 2604 OID 74339)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_hachure ALTER COLUMN id SET DEFAULT nextval('map_feature_polygon_hachure_id_seq'::regclass);


--
-- TOC entry 1956 (class 2604 OID 74316)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_image ALTER COLUMN id SET DEFAULT nextval('map_feature_polygon_image_id_seq'::regclass);


--
-- TOC entry 1955 (class 2604 OID 74293)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_point ALTER COLUMN id SET DEFAULT nextval('map_feature_text_point_id_seq'::regclass);


--
-- TOC entry 1954 (class 2604 OID 74270)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_polygon ALTER COLUMN id SET DEFAULT nextval('map_feature_text_polygon_id_seq'::regclass);


--
-- TOC entry 1952 (class 2604 OID 74120)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_style ALTER COLUMN id SET DEFAULT nextval('map_style_id_seq'::regclass);


--
-- TOC entry 1951 (class 2604 OID 74109)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY osm_feature ALTER COLUMN id SET DEFAULT nextval('osm_feature_id_seq'::regclass);


--
-- TOC entry 1953 (class 2604 OID 74257)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY osm_feature_type ALTER COLUMN id SET DEFAULT nextval('osm_feature_type_id_seq'::regclass);


--
-- TOC entry 1945 (class 2604 OID 74043)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_brush ALTER COLUMN id SET DEFAULT nextval('style_brush_id_seq'::regclass);


--
-- TOC entry 1946 (class 2604 OID 74051)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_color ALTER COLUMN id SET DEFAULT nextval('style_color_id_seq'::regclass);


--
-- TOC entry 1947 (class 2604 OID 74062)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_dynamics ALTER COLUMN id SET DEFAULT nextval('style_dynamics_id_seq'::regclass);


--
-- TOC entry 1948 (class 2604 OID 74070)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_font ALTER COLUMN id SET DEFAULT nextval('style_font_id_seq'::regclass);


--
-- TOC entry 1949 (class 2604 OID 74078)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_image ALTER COLUMN id SET DEFAULT nextval('style_image_id_seq'::regclass);


--
-- TOC entry 1950 (class 2604 OID 74086)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line ALTER COLUMN id SET DEFAULT nextval('style_line_id_seq'::regclass);


--
-- TOC entry 2144 (class 0 OID 74359)
-- Dependencies: 197
-- Data for Name: map_feature_line; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_feature_line (id, osm_feature, style_line, map_style) FROM stdin;
1	1	1	1
2	2	2	1
6	6	8	1
3	3	2	1
4	4	3	1
5	5	4	1
\.


--
-- TOC entry 2167 (class 0 OID 0)
-- Dependencies: 196
-- Name: map_feature_line_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_line_id_seq', 6, true);


--
-- TOC entry 2142 (class 0 OID 74336)
-- Dependencies: 195
-- Data for Name: map_feature_polygon_hachure; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_feature_polygon_hachure (id, osm_feature, style_line, style_hachure, map_style) FROM stdin;
1	7	6	9	1
2	8	7	10	1
3	9	5	5	1
5	\N	\N	\N	1
4	10	8	8	1
\.


--
-- TOC entry 2168 (class 0 OID 0)
-- Dependencies: 194
-- Name: map_feature_polygon_hachure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_polygon_hachure_id_seq', 5, true);


--
-- TOC entry 2140 (class 0 OID 74313)
-- Dependencies: 193
-- Data for Name: map_feature_polygon_image; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_feature_polygon_image (id, osm_feature, style_line, style_image, map_style) FROM stdin;
\.


--
-- TOC entry 2169 (class 0 OID 0)
-- Dependencies: 192
-- Name: map_feature_polygon_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_polygon_image_id_seq', 1, false);


--
-- TOC entry 2138 (class 0 OID 74290)
-- Dependencies: 191
-- Data for Name: map_feature_text_point; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_feature_text_point (id, osm_feature, style_line, style_color, map_style) FROM stdin;
\.


--
-- TOC entry 2170 (class 0 OID 0)
-- Dependencies: 190
-- Name: map_feature_text_point_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_text_point_id_seq', 1, false);


--
-- TOC entry 2136 (class 0 OID 74267)
-- Dependencies: 189
-- Data for Name: map_feature_text_polygon; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_feature_text_polygon (id, osm_feature, style_line, style_color, map_style) FROM stdin;
\.


--
-- TOC entry 2171 (class 0 OID 0)
-- Dependencies: 188
-- Name: map_feature_text_polygon_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_text_polygon_id_seq', 1, false);


--
-- TOC entry 2132 (class 0 OID 74117)
-- Dependencies: 185
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
-- TOC entry 2172 (class 0 OID 0)
-- Dependencies: 184
-- Name: map_style_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_style_id_seq', 5, true);


--
-- TOC entry 2130 (class 0 OID 74106)
-- Dependencies: 183
-- Data for Name: osm_feature; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY osm_feature (id, tags, feature_type, zoom_max, zoom_min, z_order) FROM stdin;
1	{"highway='motorway' OR highway='motorway_link'"}	2	5	20	1
2	{"highway='trunk' OR highway='trunk_link'"}	2	5	20	2
3	{"highway='primary' OR highway='primary_link'"}	2	9	20	3
4	{"highway='secondary' OR highway='secondary_link'"}	2	12	20	4
5	{"highway='tertiary' OR highway='tertiary_link'"}	2	14	20	5
6	{waterway='river'}	2	10	20	6
9	{building='yes'}	3	14	20	1
11	{"admin_level='9' OR admin_level='10'"}	3	14	20	1
7	{landuse='village_green'}	3	10	16	2
8	{"landuse='forest' OR leisure='park'"}	3	10	20	3
10	{waterway='riverbank'}	3	17	20	4
12	{tourism='attraction'}	3	15	20	2
13	{building='cathedral'}	3	15	20	2
\.


--
-- TOC entry 2173 (class 0 OID 0)
-- Dependencies: 182
-- Name: osm_feature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('osm_feature_id_seq', 13, true);


--
-- TOC entry 2134 (class 0 OID 74254)
-- Dependencies: 187
-- Data for Name: osm_feature_type; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY osm_feature_type (id, name) FROM stdin;
1	point
2	line
3	polygon
\.


--
-- TOC entry 2174 (class 0 OID 0)
-- Dependencies: 186
-- Name: osm_feature_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('osm_feature_type_id_seq', 3, true);


--
-- TOC entry 2118 (class 0 OID 74040)
-- Dependencies: 171
-- Data for Name: style_brush; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_brush (id, brush) FROM stdin;
1	GIMP Brush #7
2	Chalk 03
3	Oils 02
\.


--
-- TOC entry 2175 (class 0 OID 0)
-- Dependencies: 170
-- Name: style_brush_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_brush_id_seq', 3, true);


--
-- TOC entry 2120 (class 0 OID 74048)
-- Dependencies: 173
-- Data for Name: style_color; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_color (id, name, color) FROM stdin;
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
-- TOC entry 2176 (class 0 OID 0)
-- Dependencies: 172
-- Name: style_color_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_color_id_seq', 9, true);


--
-- TOC entry 2122 (class 0 OID 74059)
-- Dependencies: 175
-- Data for Name: style_dynamics; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_dynamics (id, dynamics) FROM stdin;
1	Det3
\.


--
-- TOC entry 2177 (class 0 OID 0)
-- Dependencies: 174
-- Name: style_dynamics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_dynamics_id_seq', 1, true);


--
-- TOC entry 2124 (class 0 OID 74067)
-- Dependencies: 177
-- Data for Name: style_font; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_font (id, name) FROM stdin;
1	Arial
\.


--
-- TOC entry 2178 (class 0 OID 0)
-- Dependencies: 176
-- Name: style_font_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_font_id_seq', 1, true);


--
-- TOC entry 2126 (class 0 OID 74075)
-- Dependencies: 179
-- Data for Name: style_image; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_image (id, name, image, opacity) FROM stdin;
1	Buildings	hachure_grey_05.png	255
2	Green areas	hachure_green_060705.png	255
3	Forest and parks	hachure_green_040504.png	255
4	Blackboard	texture_blackboard.png	255
\.


--
-- TOC entry 2179 (class 0 OID 0)
-- Dependencies: 178
-- Name: style_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_image_id_seq', 4, true);


--
-- TOC entry 2128 (class 0 OID 74083)
-- Dependencies: 181
-- Data for Name: style_line; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_line (id, name, brush, brush_size, dynamics, color, opacity) FROM stdin;
1	Motorways	3	10	1	8	100
2	Main roads	3	8	1	6	100
3	Medium roads	3	6	1	6	100
4	Small roads	3	4	1	6	100
8	Rivers	3	6	1	7	100
10	Forest and parks hachure	3	4	1	9	100
6	Green areas	3	6	1	9	100
7	Forest and Parks	3	6	1	9	100
9	Green areas hachure	3	4	1	9	100
5	Buildings	3	6	1	1	100
\.


--
-- TOC entry 2180 (class 0 OID 0)
-- Dependencies: 180
-- Name: style_line_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_line_id_seq', 10, true);


--
-- TOC entry 1986 (class 2606 OID 74364)
-- Name: map_feature_line_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_pk_id PRIMARY KEY (id);


--
-- TOC entry 1984 (class 2606 OID 74341)
-- Name: map_feature_polygon_hachure_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_feature_polygon_hachure
    ADD CONSTRAINT map_feature_polygon_hachure_pk_id PRIMARY KEY (id);


--
-- TOC entry 1982 (class 2606 OID 74318)
-- Name: map_feature_polygon_image_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_feature_polygon_image
    ADD CONSTRAINT map_feature_polygon_image_pk_id PRIMARY KEY (id);


--
-- TOC entry 1980 (class 2606 OID 74295)
-- Name: map_feature_text_point_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_feature_text_point
    ADD CONSTRAINT map_feature_text_point_pk_id PRIMARY KEY (id);


--
-- TOC entry 1978 (class 2606 OID 74272)
-- Name: map_feature_text_polygon_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_feature_text_polygon
    ADD CONSTRAINT map_feature_text_polygon_pk_id PRIMARY KEY (id);


--
-- TOC entry 1974 (class 2606 OID 74122)
-- Name: map_style_pk_image_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_style
    ADD CONSTRAINT map_style_pk_image_id PRIMARY KEY (id);


--
-- TOC entry 1972 (class 2606 OID 74114)
-- Name: osm_feature_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY osm_feature
    ADD CONSTRAINT osm_feature_pk_id PRIMARY KEY (id);


--
-- TOC entry 1976 (class 2606 OID 74259)
-- Name: osm_feature_type_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY osm_feature_type
    ADD CONSTRAINT osm_feature_type_pk_id PRIMARY KEY (id);


--
-- TOC entry 1960 (class 2606 OID 74045)
-- Name: style_brush_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_brush
    ADD CONSTRAINT style_brush_pk_id PRIMARY KEY (id);


--
-- TOC entry 1962 (class 2606 OID 74056)
-- Name: style_color_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_color
    ADD CONSTRAINT style_color_pk_id PRIMARY KEY (id);


--
-- TOC entry 1964 (class 2606 OID 74064)
-- Name: style_dynamics_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_dynamics
    ADD CONSTRAINT style_dynamics_pk_id PRIMARY KEY (id);


--
-- TOC entry 1966 (class 2606 OID 74072)
-- Name: style_font_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_font
    ADD CONSTRAINT style_font_pk_id PRIMARY KEY (id);


--
-- TOC entry 1968 (class 2606 OID 74080)
-- Name: style_image_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_image
    ADD CONSTRAINT style_image_pk_id PRIMARY KEY (id);


--
-- TOC entry 1970 (class 2606 OID 74088)
-- Name: style_line_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_pk_id PRIMARY KEY (id);


--
-- TOC entry 2009 (class 2606 OID 74376)
-- Name: map_feature_line_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2007 (class 2606 OID 74365)
-- Name: map_feature_line_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2008 (class 2606 OID 74370)
-- Name: map_feature_line_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2002 (class 2606 OID 74386)
-- Name: map_feature_polygon_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_image
    ADD CONSTRAINT map_feature_polygon_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2006 (class 2606 OID 74381)
-- Name: map_feature_polygon_hachure_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_hachure
    ADD CONSTRAINT map_feature_polygon_hachure_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2003 (class 2606 OID 74342)
-- Name: map_feature_polygon_hachure_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_hachure
    ADD CONSTRAINT map_feature_polygon_hachure_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2004 (class 2606 OID 74347)
-- Name: map_feature_polygon_hachure_fk_style_hachure; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_hachure
    ADD CONSTRAINT map_feature_polygon_hachure_fk_style_hachure FOREIGN KEY (style_hachure) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2005 (class 2606 OID 74352)
-- Name: map_feature_polygon_hachure_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_hachure
    ADD CONSTRAINT map_feature_polygon_hachure_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1999 (class 2606 OID 74319)
-- Name: map_feature_polygon_image_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_image
    ADD CONSTRAINT map_feature_polygon_image_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2000 (class 2606 OID 74324)
-- Name: map_feature_polygon_image_fk_style_image; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_image
    ADD CONSTRAINT map_feature_polygon_image_fk_style_image FOREIGN KEY (style_image) REFERENCES style_image(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2001 (class 2606 OID 74329)
-- Name: map_feature_polygon_image_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon_image
    ADD CONSTRAINT map_feature_polygon_image_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1998 (class 2606 OID 74391)
-- Name: map_feature_text_point_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_point
    ADD CONSTRAINT map_feature_text_point_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 1995 (class 2606 OID 74296)
-- Name: map_feature_text_point_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_point
    ADD CONSTRAINT map_feature_text_point_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1996 (class 2606 OID 74301)
-- Name: map_feature_text_point_fk_style_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_point
    ADD CONSTRAINT map_feature_text_point_fk_style_color FOREIGN KEY (style_color) REFERENCES style_color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1997 (class 2606 OID 74306)
-- Name: map_feature_text_point_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_point
    ADD CONSTRAINT map_feature_text_point_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1994 (class 2606 OID 74396)
-- Name: map_feature_text_polygon_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_polygon
    ADD CONSTRAINT map_feature_text_polygon_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 1991 (class 2606 OID 74273)
-- Name: map_feature_text_polygon_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_polygon
    ADD CONSTRAINT map_feature_text_polygon_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1992 (class 2606 OID 74278)
-- Name: map_feature_text_polygon_fk_style_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_polygon
    ADD CONSTRAINT map_feature_text_polygon_fk_style_color FOREIGN KEY (style_color) REFERENCES style_color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1993 (class 2606 OID 74283)
-- Name: map_feature_text_polygon_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_text_polygon
    ADD CONSTRAINT map_feature_text_polygon_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1990 (class 2606 OID 74260)
-- Name: osm_feature_type_fk_feature_type; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY osm_feature
    ADD CONSTRAINT osm_feature_type_fk_feature_type FOREIGN KEY (feature_type) REFERENCES osm_feature_type(id);


--
-- TOC entry 1987 (class 2606 OID 74089)
-- Name: style_line_fk_brush; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_fk_brush FOREIGN KEY (brush) REFERENCES style_brush(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1988 (class 2606 OID 74094)
-- Name: style_line_fk_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_fk_color FOREIGN KEY (color) REFERENCES style_color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1989 (class 2606 OID 74099)
-- Name: style_line_fk_dynamics; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_fk_dynamics FOREIGN KEY (dynamics) REFERENCES style_dynamics(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2151 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-05-18 01:49:13 CEST

--
-- PostgreSQL database dump complete
--

