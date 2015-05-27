--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.7
-- Dumped by pg_dump version 9.3.7
-- Started on 2015-05-27 16:51:52 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 202 (class 3079 OID 11789)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2181 (class 0 OID 0)
-- Dependencies: 202
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 221 (class 1255 OID 74862)
-- Name: get_background_image(integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_background_image(map_style integer) RETURNS TABLE(id integer, image character varying, zoom_min integer, zoom_max integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mbi.id,
	si.image,
	mbi.zoom_min,
	mbi.zoom_max
FROM
	map_background_image mbi
JOIN
	style_image si
ON (
	mbi.style_image = si.id
)
WHERE mbi.map_style = $1
$_$;


ALTER FUNCTION public.get_background_image(map_style integer) OWNER TO gis;

--
-- TOC entry 209 (class 1255 OID 74520)
-- Name: get_background_image(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_background_image(map_style integer, zoom_level integer) RETURNS TABLE(id integer, image character varying)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mbi.id,
	si.image
FROM
	map_background_image mbi
JOIN
	style_image si
ON (
	mbi.style_image = si.id
)
WHERE mbi.map_style = $1
-- TO DO: Zoom Levels?
$_$;


ALTER FUNCTION public.get_background_image(map_style integer, zoom_level integer) OWNER TO gis;

--
-- TOC entry 220 (class 1255 OID 74855)
-- Name: get_line_tags_and_style(integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_line_tags_and_style(map_style integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, z_order integer, zoom_min integer, zoom_max integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mfl.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	sc.color,
	sd.dynamics,	
	of.z_order,
	mfl.zoom_min,
	mfl.zoom_max
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
ORDER BY of.z_order DESC
$_$;


ALTER FUNCTION public.get_line_tags_and_style(map_style integer) OWNER TO gis;

--
-- TOC entry 216 (class 1255 OID 74403)
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
ORDER BY of.z_order DESC
$_$;


ALTER FUNCTION public.get_line_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

--
-- TOC entry 222 (class 1255 OID 74860)
-- Name: get_polygon_tags_and_style(integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_polygon_tags_and_style(map_style integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, brush_hachure character varying, brush_hachure_size integer, color_hachure integer[], dynamics_hachure character varying, hachure_spacing integer, hachure_angle integer, image character varying, color_fill integer[], z_order integer, zoom_min integer, zoom_max integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mfp.id,
	of.tags,
	sbl.brush,
	sl.brush_size,
	scl.color,
	sdl.dynamics,
	sbh.brush,
	slh.brush_size,
	sch.color,
	sdh.dynamics,
	sh.spacing,
	sh.angle,
	si.image,
	scp.color,
	of.z_order,
	mfp.zoom_min,
	mfp.zoom_max
FROM
	map_feature_polygon mfp
LEFT JOIN
	style_line sl
ON (
	mfp.style_line = sl.id
)
LEFT JOIN 
	style_brush sbl
ON (
	sl.brush = sbl.id
)
LEFT JOIN style_color scl
ON (
	sl.color = scl.id
)
LEFT JOIN style_dynamics sdl
ON (
	sl.dynamics = sdl.id
)
LEFT JOIN
	style_hachure sh
ON (
	mfp.style_hachure = sh.id
)
LEFT JOIN
	style_line slh
ON (
	sh.style_line = slh.id
)
LEFT JOIN 
	style_brush sbh
ON (
	slh.brush = sbh.id
)
LEFT JOIN style_color sch
ON (
	slh.color = sch.id
)
LEFT JOIN style_dynamics sdh
ON (
	slh.dynamics = sdh.id
)
LEFT JOIN style_image si
ON (
	mfp.style_image = si.id
)
LEFT JOIN osm_feature of
ON (
	mfp.osm_feature = of.id
)
LEFT JOIN style_color scp
ON (
	mfp.color = scp.id
)
WHERE mfp.map_style = $1
ORDER BY of.z_order DESC
$_$;


ALTER FUNCTION public.get_polygon_tags_and_style(map_style integer) OWNER TO gis;

--
-- TOC entry 219 (class 1255 OID 74853)
-- Name: get_polygon_tags_and_style(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_polygon_tags_and_style(map_style integer, zoom_level integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, brush_hachure character varying, brush_hachure_size integer, color_hachure integer[], dynamics_hachure character varying, hachure_spacing integer, hachure_angle integer, image character varying, color_fill integer[], z_order integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mfp.id,
	of.tags,
	sbl.brush,
	sl.brush_size,
	scl.color,
	sdl.dynamics,
	sbh.brush,
	slh.brush_size,
	sch.color,
	sdh.dynamics,
	sh.spacing,
	sh.angle,
	si.image,
	scp.color,
	of.z_order
FROM
	map_feature_polygon mfp
LEFT JOIN
	style_line sl
ON (
	mfp.style_line = sl.id
)
LEFT JOIN 
	style_brush sbl
ON (
	sl.brush = sbl.id
)
LEFT JOIN style_color scl
ON (
	sl.color = scl.id
)
LEFT JOIN style_dynamics sdl
ON (
	sl.dynamics = sdl.id
)
LEFT JOIN
	style_hachure sh
ON (
	mfp.style_hachure = sh.id
)
LEFT JOIN
	style_line slh
ON (
	sh.style_line = slh.id
)
LEFT JOIN 
	style_brush sbh
ON (
	slh.brush = sbh.id
)
LEFT JOIN style_color sch
ON (
	slh.color = sch.id
)
LEFT JOIN style_dynamics sdh
ON (
	slh.dynamics = sdh.id
)
LEFT JOIN style_image si
ON (
	mfp.style_image = si.id
)
LEFT JOIN osm_feature of
ON (
	mfp.osm_feature = of.id
)
LEFT JOIN style_color scp
ON (
	mfp.color = scp.id
)
WHERE mfp.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order DESC
$_$;


ALTER FUNCTION public.get_polygon_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

--
-- TOC entry 218 (class 1255 OID 74861)
-- Name: get_text_polygon_tags_and_style(integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_text_polygon_tags_and_style(map_style integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, font character varying, font_size integer, color_font integer[], z_order integer, zoom_min integer, zoom_max integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mtp.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	slc.color,
	sd.dynamics,
	sf.name,
	st.font_size,
	stc.color,
	of.z_order,
	mtp.zoom_min,
	mtp.zoom_max
FROM
	map_text_polygon mtp
LEFT JOIN
	style_line sl
ON (
	mtp.style_line = sl.id
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
LEFT JOIN style_text st
ON (
	mtp.style_text = st.id
)
LEFT JOIN style_font sf
ON (
	st.font = sf.id
)
LEFT JOIN style_color stc
ON (
	st.color = stc.id
)
LEFT JOIN osm_feature of
ON (
	mtp.osm_feature = of.id
)
WHERE mtp.map_style = $1
ORDER BY of.z_order DESC
$_$;


ALTER FUNCTION public.get_text_polygon_tags_and_style(map_style integer) OWNER TO gis;

--
-- TOC entry 217 (class 1255 OID 74519)
-- Name: get_text_polygon_tags_and_style(integer, integer); Type: FUNCTION; Schema: public; Owner: gis
--

CREATE FUNCTION get_text_polygon_tags_and_style(map_style integer, zoom_level integer) RETURNS TABLE(id integer, tags text[], brush character varying, brush_size integer, color integer[], dynamics character varying, font character varying, font_size integer, color_font integer[], z_order integer)
    LANGUAGE sql STABLE
    AS $_$
SELECT
	mtp.id,
	of.tags,
	sb.brush,
	sl.brush_size,
	slc.color,
	sd.dynamics,
	sf.name,
	st.font_size,
	stc.color,
	of.z_order
FROM
	map_text_polygon mtp
LEFT JOIN
	style_line sl
ON (
	mtp.style_line = sl.id
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
LEFT JOIN style_text st
ON (
	mtp.style_text = st.id
)
LEFT JOIN style_font sf
ON (
	st.font = sf.id
)
LEFT JOIN style_color stc
ON (
	st.color = stc.id
)
LEFT JOIN osm_feature of
ON (
	mtp.osm_feature = of.id
)
WHERE mtp.map_style = $1
AND of.zoom_max <= $2
AND of.zoom_min >= $2
ORDER BY of.z_order DESC
$_$;


ALTER FUNCTION public.get_text_polygon_tags_and_style(map_style integer, zoom_level integer) OWNER TO gis;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 199 (class 1259 OID 74443)
-- Name: map_background_image; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_background_image (
    id integer NOT NULL,
    style_image integer,
    map_style integer,
    zoom_min integer,
    zoom_max integer
);


ALTER TABLE public.map_background_image OWNER TO gis;

--
-- TOC entry 198 (class 1259 OID 74441)
-- Name: map_background_image_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE map_background_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.map_background_image_id_seq OWNER TO gis;

--
-- TOC entry 2182 (class 0 OID 0)
-- Dependencies: 198
-- Name: map_background_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_background_image_id_seq OWNED BY map_background_image.id;


--
-- TOC entry 195 (class 1259 OID 74359)
-- Name: map_feature_line; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_feature_line (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    map_style integer,
    zoom_min integer,
    zoom_max integer
);


ALTER TABLE public.map_feature_line OWNER TO gis;

--
-- TOC entry 194 (class 1259 OID 74357)
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
-- TOC entry 2183 (class 0 OID 0)
-- Dependencies: 194
-- Name: map_feature_line_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_line_id_seq OWNED BY map_feature_line.id;


--
-- TOC entry 193 (class 1259 OID 74336)
-- Name: map_feature_polygon; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_feature_polygon (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    style_hachure integer,
    style_image integer,
    map_style integer,
    color integer,
    zoom_min integer,
    zoom_max integer
);


ALTER TABLE public.map_feature_polygon OWNER TO gis;

--
-- TOC entry 192 (class 1259 OID 74334)
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
-- TOC entry 2184 (class 0 OID 0)
-- Dependencies: 192
-- Name: map_feature_polygon_hachure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_polygon_hachure_id_seq OWNED BY map_feature_polygon.id;


--
-- TOC entry 191 (class 1259 OID 74290)
-- Name: map_text_point; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_text_point (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    style_text integer,
    map_style integer,
    zoom_min integer,
    zoom_max integer
);


ALTER TABLE public.map_text_point OWNER TO gis;

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
-- TOC entry 2185 (class 0 OID 0)
-- Dependencies: 190
-- Name: map_feature_text_point_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_text_point_id_seq OWNED BY map_text_point.id;


--
-- TOC entry 189 (class 1259 OID 74267)
-- Name: map_text_polygon; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE map_text_polygon (
    id integer NOT NULL,
    osm_feature integer,
    style_line integer,
    style_text integer,
    map_style integer,
    zoom_min integer,
    zoom_max integer
);


ALTER TABLE public.map_text_polygon OWNER TO gis;

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
-- TOC entry 2186 (class 0 OID 0)
-- Dependencies: 188
-- Name: map_feature_text_polygon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE map_feature_text_polygon_id_seq OWNED BY map_text_polygon.id;


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
-- TOC entry 2187 (class 0 OID 0)
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
-- TOC entry 2188 (class 0 OID 0)
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
-- TOC entry 2189 (class 0 OID 0)
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
-- TOC entry 2190 (class 0 OID 0)
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
-- TOC entry 2191 (class 0 OID 0)
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
-- TOC entry 2192 (class 0 OID 0)
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
-- TOC entry 2193 (class 0 OID 0)
-- Dependencies: 176
-- Name: style_font_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_font_id_seq OWNED BY style_font.id;


--
-- TOC entry 201 (class 1259 OID 74576)
-- Name: style_hachure; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_hachure (
    id integer NOT NULL,
    name character varying(50),
    style_line integer,
    spacing integer,
    angle integer
);


ALTER TABLE public.style_hachure OWNER TO gis;

--
-- TOC entry 200 (class 1259 OID 74574)
-- Name: style_hachure_id_seq; Type: SEQUENCE; Schema: public; Owner: gis
--

CREATE SEQUENCE style_hachure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.style_hachure_id_seq OWNER TO gis;

--
-- TOC entry 2194 (class 0 OID 0)
-- Dependencies: 200
-- Name: style_hachure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_hachure_id_seq OWNED BY style_hachure.id;


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
-- TOC entry 2195 (class 0 OID 0)
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
-- TOC entry 2196 (class 0 OID 0)
-- Dependencies: 180
-- Name: style_line_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_line_id_seq OWNED BY style_line.id;


--
-- TOC entry 197 (class 1259 OID 74423)
-- Name: style_text; Type: TABLE; Schema: public; Owner: gis; Tablespace: 
--

CREATE TABLE style_text (
    id integer NOT NULL,
    name character varying(20),
    font integer,
    font_size integer,
    color integer
);


ALTER TABLE public.style_text OWNER TO gis;

--
-- TOC entry 196 (class 1259 OID 74421)
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
-- TOC entry 2197 (class 0 OID 0)
-- Dependencies: 196
-- Name: style_text_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gis
--

ALTER SEQUENCE style_text_id_seq OWNED BY style_text.id;


--
-- TOC entry 1975 (class 2604 OID 74446)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_background_image ALTER COLUMN id SET DEFAULT nextval('map_background_image_id_seq'::regclass);


--
-- TOC entry 1973 (class 2604 OID 74362)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line ALTER COLUMN id SET DEFAULT nextval('map_feature_line_id_seq'::regclass);


--
-- TOC entry 1972 (class 2604 OID 74339)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon ALTER COLUMN id SET DEFAULT nextval('map_feature_polygon_hachure_id_seq'::regclass);


--
-- TOC entry 1968 (class 2604 OID 74120)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_style ALTER COLUMN id SET DEFAULT nextval('map_style_id_seq'::regclass);


--
-- TOC entry 1971 (class 2604 OID 74293)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_point ALTER COLUMN id SET DEFAULT nextval('map_feature_text_point_id_seq'::regclass);


--
-- TOC entry 1970 (class 2604 OID 74270)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_polygon ALTER COLUMN id SET DEFAULT nextval('map_feature_text_polygon_id_seq'::regclass);


--
-- TOC entry 1967 (class 2604 OID 74109)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY osm_feature ALTER COLUMN id SET DEFAULT nextval('osm_feature_id_seq'::regclass);


--
-- TOC entry 1969 (class 2604 OID 74257)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY osm_feature_type ALTER COLUMN id SET DEFAULT nextval('osm_feature_type_id_seq'::regclass);


--
-- TOC entry 1961 (class 2604 OID 74043)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_brush ALTER COLUMN id SET DEFAULT nextval('style_brush_id_seq'::regclass);


--
-- TOC entry 1962 (class 2604 OID 74051)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_color ALTER COLUMN id SET DEFAULT nextval('style_color_id_seq'::regclass);


--
-- TOC entry 1963 (class 2604 OID 74062)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_dynamics ALTER COLUMN id SET DEFAULT nextval('style_dynamics_id_seq'::regclass);


--
-- TOC entry 1964 (class 2604 OID 74070)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_font ALTER COLUMN id SET DEFAULT nextval('style_font_id_seq'::regclass);


--
-- TOC entry 1976 (class 2604 OID 74579)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_hachure ALTER COLUMN id SET DEFAULT nextval('style_hachure_id_seq'::regclass);


--
-- TOC entry 1965 (class 2604 OID 74078)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_image ALTER COLUMN id SET DEFAULT nextval('style_image_id_seq'::regclass);


--
-- TOC entry 1966 (class 2604 OID 74086)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line ALTER COLUMN id SET DEFAULT nextval('style_line_id_seq'::regclass);


--
-- TOC entry 1974 (class 2604 OID 74426)
-- Name: id; Type: DEFAULT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_text ALTER COLUMN id SET DEFAULT nextval('style_text_id_seq'::regclass);


--
-- TOC entry 2171 (class 0 OID 74443)
-- Dependencies: 199
-- Data for Name: map_background_image; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_background_image (id, style_image, map_style, zoom_min, zoom_max) FROM stdin;
1	4	1	0	20
\.


--
-- TOC entry 2198 (class 0 OID 0)
-- Dependencies: 198
-- Name: map_background_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_background_image_id_seq', 1, true);


--
-- TOC entry 2167 (class 0 OID 74359)
-- Dependencies: 195
-- Data for Name: map_feature_line; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_feature_line (id, osm_feature, style_line, map_style, zoom_min, zoom_max) FROM stdin;
1	1	1	1	5	20
2	2	2	1	5	20
3	3	2	1	9	20
4	4	3	1	12	20
5	5	4	1	14	20
6	6	8	1	10	20
\.


--
-- TOC entry 2199 (class 0 OID 0)
-- Dependencies: 194
-- Name: map_feature_line_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_line_id_seq', 6, true);


--
-- TOC entry 2165 (class 0 OID 74336)
-- Dependencies: 193
-- Data for Name: map_feature_polygon; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_feature_polygon (id, osm_feature, style_line, style_hachure, style_image, map_style, color, zoom_min, zoom_max) FROM stdin;
5	\N	\N	\N	\N	\N	\N	\N	\N
1	7	6	1	2	1	\N	14	20
2	8	7	2	3	1	\N	10	20
3	9	5	3	1	1	\N	14	20
4	10	8	4	5	1	\N	17	20
\.


--
-- TOC entry 2200 (class 0 OID 0)
-- Dependencies: 192
-- Name: map_feature_polygon_hachure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_polygon_hachure_id_seq', 5, true);


--
-- TOC entry 2201 (class 0 OID 0)
-- Dependencies: 190
-- Name: map_feature_text_point_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_text_point_id_seq', 1, false);


--
-- TOC entry 2202 (class 0 OID 0)
-- Dependencies: 188
-- Name: map_feature_text_polygon_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_feature_text_polygon_id_seq', 4, true);


--
-- TOC entry 2157 (class 0 OID 74117)
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
-- TOC entry 2203 (class 0 OID 0)
-- Dependencies: 184
-- Name: map_style_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('map_style_id_seq', 5, true);


--
-- TOC entry 2163 (class 0 OID 74290)
-- Dependencies: 191
-- Data for Name: map_text_point; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_text_point (id, osm_feature, style_line, style_text, map_style, zoom_min, zoom_max) FROM stdin;
\.


--
-- TOC entry 2161 (class 0 OID 74267)
-- Dependencies: 189
-- Data for Name: map_text_polygon; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY map_text_polygon (id, osm_feature, style_line, style_text, map_style, zoom_min, zoom_max) FROM stdin;
1	11	11	1	1	14	20
2	12	11	1	1	15	20
3	13	11	1	1	15	20
4	14	11	1	1	10	20
\.


--
-- TOC entry 2155 (class 0 OID 74106)
-- Dependencies: 183
-- Data for Name: osm_feature; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY osm_feature (id, tags, feature_type, z_order) FROM stdin;
1	{"highway='motorway' OR highway='motorway_link'"}	2	1
2	{"highway='trunk' OR highway='trunk_link'"}	2	2
3	{"highway='primary' OR highway='primary_link'"}	2	3
4	{"highway='secondary' OR highway='secondary_link'"}	2	4
5	{"highway='tertiary' OR highway='tertiary_link'"}	2	5
6	{waterway='river'}	2	6
9	{building='yes'}	3	1
8	{"landuse='forest' OR leisure='park'"}	3	3
10	{waterway='riverbank'}	3	4
7	{landuse='village_green'}	3	2
14	{admin_level='6'}	3	1
11	{"admin_level='9' OR admin_level='10'"}	3	2
12	{tourism='attraction'}	3	3
13	{building='cathedral'}	3	4
\.


--
-- TOC entry 2204 (class 0 OID 0)
-- Dependencies: 182
-- Name: osm_feature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('osm_feature_id_seq', 14, true);


--
-- TOC entry 2159 (class 0 OID 74254)
-- Dependencies: 187
-- Data for Name: osm_feature_type; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY osm_feature_type (id, name) FROM stdin;
1	point
2	line
3	polygon
\.


--
-- TOC entry 2205 (class 0 OID 0)
-- Dependencies: 186
-- Name: osm_feature_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('osm_feature_type_id_seq', 3, true);


--
-- TOC entry 2143 (class 0 OID 74040)
-- Dependencies: 171
-- Data for Name: style_brush; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_brush (id, brush) FROM stdin;
1	GIMP Brush #7
2	Chalk 03
3	Oils 02
\.


--
-- TOC entry 2206 (class 0 OID 0)
-- Dependencies: 170
-- Name: style_brush_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_brush_id_seq', 3, true);


--
-- TOC entry 2145 (class 0 OID 74048)
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
10	White	{255,255,255}
\.


--
-- TOC entry 2207 (class 0 OID 0)
-- Dependencies: 172
-- Name: style_color_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_color_id_seq', 10, true);


--
-- TOC entry 2147 (class 0 OID 74059)
-- Dependencies: 175
-- Data for Name: style_dynamics; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_dynamics (id, dynamics) FROM stdin;
1	Det3
\.


--
-- TOC entry 2208 (class 0 OID 0)
-- Dependencies: 174
-- Name: style_dynamics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_dynamics_id_seq', 1, true);


--
-- TOC entry 2149 (class 0 OID 74067)
-- Dependencies: 177
-- Data for Name: style_font; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_font (id, name) FROM stdin;
1	Arial
\.


--
-- TOC entry 2209 (class 0 OID 0)
-- Dependencies: 176
-- Name: style_font_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_font_id_seq', 1, true);


--
-- TOC entry 2173 (class 0 OID 74576)
-- Dependencies: 201
-- Data for Name: style_hachure; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_hachure (id, name, style_line, spacing, angle) FROM stdin;
1	Hachure green	6	10	35
2	Hachure Forest/Park	7	10	35
3	Hachure Building	5	10	35
4	Hachure Riverbank	8	10	35
\.


--
-- TOC entry 2210 (class 0 OID 0)
-- Dependencies: 200
-- Name: style_hachure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_hachure_id_seq', 4, true);


--
-- TOC entry 2151 (class 0 OID 74075)
-- Dependencies: 179
-- Data for Name: style_image; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_image (id, name, image, opacity) FROM stdin;
1	Buildings	hachure_grey_05.png	100
2	Green areas	hachure_green_060705.png	100
3	Forest and parks	hachure_green_040504.png	100
4	Blackboard	texture_blackboard.png	100
5	Water	hachure_blue_050708.png	100
\.


--
-- TOC entry 2211 (class 0 OID 0)
-- Dependencies: 178
-- Name: style_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_image_id_seq', 5, true);


--
-- TOC entry 2153 (class 0 OID 74083)
-- Dependencies: 181
-- Data for Name: style_line; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_line (id, name, brush, brush_size, dynamics, color, opacity) FROM stdin;
11	Text	3	2	1	6	100
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
-- TOC entry 2212 (class 0 OID 0)
-- Dependencies: 180
-- Name: style_line_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_line_id_seq', 11, true);


--
-- TOC entry 2169 (class 0 OID 74423)
-- Dependencies: 197
-- Data for Name: style_text; Type: TABLE DATA; Schema: public; Owner: gis
--

COPY style_text (id, name, font, font_size, color) FROM stdin;
1	Test	1	10	10
\.


--
-- TOC entry 2213 (class 0 OID 0)
-- Dependencies: 196
-- Name: style_text_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gis
--

SELECT pg_catalog.setval('style_text_id_seq', 1, true);


--
-- TOC entry 2006 (class 2606 OID 74448)
-- Name: map_background_image_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_background_image
    ADD CONSTRAINT map_background_image_pk_id PRIMARY KEY (id);


--
-- TOC entry 2002 (class 2606 OID 74364)
-- Name: map_feature_line_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_pk_id PRIMARY KEY (id);


--
-- TOC entry 2000 (class 2606 OID 74522)
-- Name: map_feature_polygon_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_feature_polygon
    ADD CONSTRAINT map_feature_polygon_pk_id PRIMARY KEY (id);


--
-- TOC entry 1992 (class 2606 OID 74122)
-- Name: map_style_pk_image_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_style
    ADD CONSTRAINT map_style_pk_image_id PRIMARY KEY (id);


--
-- TOC entry 1998 (class 2606 OID 74460)
-- Name: map_text_point_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_text_point
    ADD CONSTRAINT map_text_point_pk_id PRIMARY KEY (id);


--
-- TOC entry 1996 (class 2606 OID 74482)
-- Name: map_text_polygon_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY map_text_polygon
    ADD CONSTRAINT map_text_polygon_pk_id PRIMARY KEY (id);


--
-- TOC entry 1990 (class 2606 OID 74114)
-- Name: osm_feature_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY osm_feature
    ADD CONSTRAINT osm_feature_pk_id PRIMARY KEY (id);


--
-- TOC entry 1994 (class 2606 OID 74259)
-- Name: osm_feature_type_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY osm_feature_type
    ADD CONSTRAINT osm_feature_type_pk_id PRIMARY KEY (id);


--
-- TOC entry 1978 (class 2606 OID 74045)
-- Name: style_brush_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_brush
    ADD CONSTRAINT style_brush_pk_id PRIMARY KEY (id);


--
-- TOC entry 1980 (class 2606 OID 74056)
-- Name: style_color_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_color
    ADD CONSTRAINT style_color_pk_id PRIMARY KEY (id);


--
-- TOC entry 1982 (class 2606 OID 74064)
-- Name: style_dynamics_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_dynamics
    ADD CONSTRAINT style_dynamics_pk_id PRIMARY KEY (id);


--
-- TOC entry 1984 (class 2606 OID 74072)
-- Name: style_font_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_font
    ADD CONSTRAINT style_font_pk_id PRIMARY KEY (id);


--
-- TOC entry 2008 (class 2606 OID 74581)
-- Name: style_hachure_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_hachure
    ADD CONSTRAINT style_hachure_pk_id PRIMARY KEY (id);


--
-- TOC entry 1986 (class 2606 OID 74080)
-- Name: style_image_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_image
    ADD CONSTRAINT style_image_pk_id PRIMARY KEY (id);


--
-- TOC entry 1988 (class 2606 OID 74088)
-- Name: style_line_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_pk_id PRIMARY KEY (id);


--
-- TOC entry 2004 (class 2606 OID 74428)
-- Name: style_text_pk_id; Type: CONSTRAINT; Schema: public; Owner: gis; Tablespace: 
--

ALTER TABLE ONLY style_text
    ADD CONSTRAINT style_text_pk_id PRIMARY KEY (id);


--
-- TOC entry 2032 (class 2606 OID 74449)
-- Name: map_background_image_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_background_image
    ADD CONSTRAINT map_background_image_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2033 (class 2606 OID 74454)
-- Name: map_background_image_fk_style_image; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_background_image
    ADD CONSTRAINT map_background_image_fk_style_image FOREIGN KEY (style_image) REFERENCES style_image(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2029 (class 2606 OID 74376)
-- Name: map_feature_line_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2027 (class 2606 OID 74365)
-- Name: map_feature_line_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2028 (class 2606 OID 74370)
-- Name: map_feature_line_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_line
    ADD CONSTRAINT map_feature_line_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2026 (class 2606 OID 74846)
-- Name: map_feature_polygon_fk_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon
    ADD CONSTRAINT map_feature_polygon_fk_color FOREIGN KEY (color) REFERENCES style_color(id);


--
-- TOC entry 2024 (class 2606 OID 74543)
-- Name: map_feature_polygon_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon
    ADD CONSTRAINT map_feature_polygon_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2021 (class 2606 OID 74523)
-- Name: map_feature_polygon_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon
    ADD CONSTRAINT map_feature_polygon_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id);


--
-- TOC entry 2025 (class 2606 OID 74841)
-- Name: map_feature_polygon_fk_style_hachure; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon
    ADD CONSTRAINT map_feature_polygon_fk_style_hachure FOREIGN KEY (style_hachure) REFERENCES style_hachure(id);


--
-- TOC entry 2023 (class 2606 OID 74538)
-- Name: map_feature_polygon_fk_style_image; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon
    ADD CONSTRAINT map_feature_polygon_fk_style_image FOREIGN KEY (style_image) REFERENCES style_image(id);


--
-- TOC entry 2022 (class 2606 OID 74528)
-- Name: map_feature_polygon_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_feature_polygon
    ADD CONSTRAINT map_feature_polygon_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id);


--
-- TOC entry 2018 (class 2606 OID 74476)
-- Name: map_text_point_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_point
    ADD CONSTRAINT map_text_point_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2017 (class 2606 OID 74461)
-- Name: map_text_point_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_point
    ADD CONSTRAINT map_text_point_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id);


--
-- TOC entry 2020 (class 2606 OID 74513)
-- Name: map_text_point_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_point
    ADD CONSTRAINT map_text_point_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id);


--
-- TOC entry 2019 (class 2606 OID 74508)
-- Name: map_text_point_fk_style_text; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_point
    ADD CONSTRAINT map_text_point_fk_style_text FOREIGN KEY (style_text) REFERENCES style_text(id);


--
-- TOC entry 2016 (class 2606 OID 74498)
-- Name: map_text_polygon_fk_map_style; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_polygon
    ADD CONSTRAINT map_text_polygon_fk_map_style FOREIGN KEY (map_style) REFERENCES map_style(id);


--
-- TOC entry 2013 (class 2606 OID 74483)
-- Name: map_text_polygon_fk_osm_feature; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_polygon
    ADD CONSTRAINT map_text_polygon_fk_osm_feature FOREIGN KEY (osm_feature) REFERENCES osm_feature(id);


--
-- TOC entry 2014 (class 2606 OID 74488)
-- Name: map_text_polygon_fk_style_line; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_polygon
    ADD CONSTRAINT map_text_polygon_fk_style_line FOREIGN KEY (style_line) REFERENCES style_line(id);


--
-- TOC entry 2015 (class 2606 OID 74493)
-- Name: map_text_polygon_fk_style_text; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY map_text_polygon
    ADD CONSTRAINT map_text_polygon_fk_style_text FOREIGN KEY (style_text) REFERENCES style_text(id);


--
-- TOC entry 2012 (class 2606 OID 74260)
-- Name: osm_feature_type_fk_feature_type; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY osm_feature
    ADD CONSTRAINT osm_feature_type_fk_feature_type FOREIGN KEY (feature_type) REFERENCES osm_feature_type(id);


--
-- TOC entry 2034 (class 2606 OID 74582)
-- Name: style_hachure_fk_style_hachure; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_hachure
    ADD CONSTRAINT style_hachure_fk_style_hachure FOREIGN KEY (style_line) REFERENCES style_line(id);


--
-- TOC entry 2009 (class 2606 OID 74089)
-- Name: style_line_fk_brush; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_fk_brush FOREIGN KEY (brush) REFERENCES style_brush(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2010 (class 2606 OID 74094)
-- Name: style_line_fk_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_fk_color FOREIGN KEY (color) REFERENCES style_color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2011 (class 2606 OID 74099)
-- Name: style_line_fk_dynamics; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_line
    ADD CONSTRAINT style_line_fk_dynamics FOREIGN KEY (dynamics) REFERENCES style_dynamics(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2031 (class 2606 OID 74434)
-- Name: style_text_fk_color; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_text
    ADD CONSTRAINT style_text_fk_color FOREIGN KEY (color) REFERENCES style_color(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2030 (class 2606 OID 74429)
-- Name: style_text_fk_font; Type: FK CONSTRAINT; Schema: public; Owner: gis
--

ALTER TABLE ONLY style_text
    ADD CONSTRAINT style_text_fk_font FOREIGN KEY (font) REFERENCES style_font(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2180 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-05-27 16:51:52 CEST

--
-- PostgreSQL database dump complete
--

