--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+2)
-- Dumped by pg_dump version 16.6 (Ubuntu 16.6-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO dbuser;

--
-- Name: balances; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.balances (
    id integer NOT NULL,
    user_id integer,
    value bigint,
    date character varying,
    created timestamp without time zone
);


ALTER TABLE public.balances OWNER TO dbuser;

--
-- Name: balances_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.balances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.balances_id_seq OWNER TO dbuser;

--
-- Name: balances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.balances_id_seq OWNED BY public.balances.id;


--
-- Name: billings; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.billings (
    id integer NOT NULL,
    user_id integer,
    type character varying(32),
    state character varying(32),
    value bigint,
    created timestamp without time zone,
    payment_type character varying(32),
    payment_data character varying(512),
    currency character varying(32),
    value_usd bigint,
    image_id integer
);


ALTER TABLE public.billings OWNER TO dbuser;

--
-- Name: billings_buy_requests; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.billings_buy_requests (
    id integer NOT NULL,
    billing_id integer,
    buy_request_id integer,
    created timestamp without time zone
);


ALTER TABLE public.billings_buy_requests OWNER TO dbuser;

--
-- Name: billings_buy_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.billings_buy_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.billings_buy_requests_id_seq OWNER TO dbuser;

--
-- Name: billings_buy_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.billings_buy_requests_id_seq OWNED BY public.billings_buy_requests.id;


--
-- Name: billings_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.billings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.billings_id_seq OWNER TO dbuser;

--
-- Name: billings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.billings_id_seq OWNED BY public.billings.id;


--
-- Name: billings_payments; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.billings_payments (
    id integer NOT NULL,
    billing_id integer,
    payment_id integer,
    created timestamp without time zone
);


ALTER TABLE public.billings_payments OWNER TO dbuser;

--
-- Name: billings_payments_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.billings_payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.billings_payments_id_seq OWNER TO dbuser;

--
-- Name: billings_payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.billings_payments_id_seq OWNED BY public.billings_payments.id;


--
-- Name: buy_request_miner_items; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.buy_request_miner_items (
    id integer NOT NULL,
    buy_request_id integer,
    miner_item_id integer,
    count integer,
    created timestamp without time zone
);


ALTER TABLE public.buy_request_miner_items OWNER TO dbuser;

--
-- Name: buy_request_miner_items_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.buy_request_miner_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.buy_request_miner_items_id_seq OWNER TO dbuser;

--
-- Name: buy_request_miner_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.buy_request_miner_items_id_seq OWNED BY public.buy_request_miner_items.id;


--
-- Name: buy_requests; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.buy_requests (
    id integer NOT NULL,
    name character varying,
    user_id integer,
    state character varying(32),
    created timestamp without time zone
);


ALTER TABLE public.buy_requests OWNER TO dbuser;

--
-- Name: buy_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.buy_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.buy_requests_id_seq OWNER TO dbuser;

--
-- Name: buy_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.buy_requests_id_seq OWNED BY public.buy_requests.id;


--
-- Name: countries; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.countries (
    id integer NOT NULL,
    name character varying,
    short_code character varying
);


ALTER TABLE public.countries OWNER TO dbuser;

--
-- Name: countries_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.countries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.countries_id_seq OWNER TO dbuser;

--
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.countries_id_seq OWNED BY public.countries.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    username character varying,
    email character varying,
    password character varying,
    created timestamp without time zone
);


ALTER TABLE public.employees OWNER TO dbuser;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO dbuser;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: feedbacks; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.feedbacks (
    id integer NOT NULL,
    name character varying,
    phone character varying(32),
    state character varying(16),
    created timestamp without time zone
);


ALTER TABLE public.feedbacks OWNER TO dbuser;

--
-- Name: feedbacks_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.feedbacks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feedbacks_id_seq OWNER TO dbuser;

--
-- Name: feedbacks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.feedbacks_id_seq OWNED BY public.feedbacks.id;


--
-- Name: images; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.images (
    id integer NOT NULL,
    path character varying(256),
    filename character varying(128),
    extension character varying(8),
    created timestamp without time zone
);


ALTER TABLE public.images OWNER TO dbuser;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.images_id_seq OWNER TO dbuser;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: markets_carts; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.markets_carts (
    id integer NOT NULL,
    user_id integer,
    miner_item_id integer,
    created timestamp without time zone,
    count integer
);


ALTER TABLE public.markets_carts OWNER TO dbuser;

--
-- Name: markets_carts_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.markets_carts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.markets_carts_id_seq OWNER TO dbuser;

--
-- Name: markets_carts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.markets_carts_id_seq OWNED BY public.markets_carts.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    content character varying,
    ticket_id integer,
    created_at timestamp without time zone,
    sender character varying(32),
    image_id integer
);


ALTER TABLE public.messages OWNER TO dbuser;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.messages_id_seq OWNER TO dbuser;

--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: miner_items; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.miner_items (
    id integer NOT NULL,
    name character varying,
    description character varying,
    hash_rate bigint,
    energy_consumption integer,
    price integer,
    is_hidden boolean,
    created timestamp without time zone,
    image_id integer,
    priority integer,
    category_id integer,
    discount_count integer,
    discount_value integer
);


ALTER TABLE public.miner_items OWNER TO dbuser;

--
-- Name: miner_items_categories; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.miner_items_categories (
    id integer NOT NULL,
    name character varying,
    description character varying,
    is_hidden boolean,
    priority integer,
    created timestamp without time zone
);


ALTER TABLE public.miner_items_categories OWNER TO dbuser;

--
-- Name: miner_items_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.miner_items_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.miner_items_categories_id_seq OWNER TO dbuser;

--
-- Name: miner_items_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.miner_items_categories_id_seq OWNED BY public.miner_items_categories.id;


--
-- Name: miner_items_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.miner_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.miner_items_id_seq OWNER TO dbuser;

--
-- Name: miner_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.miner_items_id_seq OWNED BY public.miner_items.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    type character varying(32),
    currency character varying(8),
    user_id integer,
    value bigint,
    date character varying,
    created timestamp without time zone,
    date_time timestamp without time zone
);


ALTER TABLE public.payments OWNER TO dbuser;

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO dbuser;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: payments_sites; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.payments_sites (
    id integer NOT NULL,
    payment_id integer,
    site_id character varying(128),
    created timestamp without time zone,
    hash_rate bigint
);


ALTER TABLE public.payments_sites OWNER TO dbuser;

--
-- Name: payments_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.payments_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_sites_id_seq OWNER TO dbuser;

--
-- Name: payments_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.payments_sites_id_seq OWNED BY public.payments_sites.id;


--
-- Name: purchases_records; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.purchases_records (
    id integer NOT NULL,
    user_id integer,
    name character varying,
    date timestamp without time zone,
    amount integer
);


ALTER TABLE public.purchases_records OWNER TO dbuser;

--
-- Name: purchases_records_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.purchases_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.purchases_records_id_seq OWNER TO dbuser;

--
-- Name: purchases_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.purchases_records_id_seq OWNED BY public.purchases_records.id;


--
-- Name: resets_passwords_requests; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.resets_passwords_requests (
    id character varying NOT NULL,
    user_id integer,
    created_at timestamp without time zone,
    expired boolean
);


ALTER TABLE public.resets_passwords_requests OWNER TO dbuser;

--
-- Name: settings; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.settings (
    id integer NOT NULL,
    key character varying,
    value character varying
);


ALTER TABLE public.settings OWNER TO dbuser;

--
-- Name: settings_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.settings_id_seq OWNER TO dbuser;

--
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.settings_id_seq OWNED BY public.settings.id;


--
-- Name: tickets; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.tickets (
    id integer NOT NULL,
    title character varying,
    created_at timestamp without time zone,
    user_id integer,
    is_open boolean
);


ALTER TABLE public.tickets OWNER TO dbuser;

--
-- Name: tickets_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.tickets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tickets_id_seq OWNER TO dbuser;

--
-- Name: tickets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.tickets_id_seq OWNED BY public.tickets.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.users (
    id integer NOT NULL,
    firstname character varying,
    lastname character varying,
    phone character varying,
    email character varying,
    password character varying,
    telegram character varying,
    country character varying,
    address character varying,
    inn character varying,
    profile_type character varying,
    last_totp character varying,
    totp_sent timestamp without time zone,
    wallet character varying,
    mfa_key character varying,
    mfa_enabled boolean,
    miner_name character varying,
    miner_id character varying,
    wallet_id character varying,
    access_allowed boolean,
    created timestamp without time zone,
    image_id integer,
    lang character varying(4)
);


ALTER TABLE public.users OWNER TO dbuser;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO dbuser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: workers; Type: TABLE; Schema: public; Owner: dbuser
--

CREATE TABLE public.workers (
    id integer NOT NULL,
    user_id integer,
    miner_item_id integer,
    id_str character varying(64),
    name character varying(128),
    behavior character varying(32),
    hidden boolean,
    created timestamp without time zone
);


ALTER TABLE public.workers OWNER TO dbuser;

--
-- Name: workers_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE public.workers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workers_id_seq OWNER TO dbuser;

--
-- Name: workers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE public.workers_id_seq OWNED BY public.workers.id;


--
-- Name: balances id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.balances ALTER COLUMN id SET DEFAULT nextval('public.balances_id_seq'::regclass);


--
-- Name: billings id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings ALTER COLUMN id SET DEFAULT nextval('public.billings_id_seq'::regclass);


--
-- Name: billings_buy_requests id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_buy_requests ALTER COLUMN id SET DEFAULT nextval('public.billings_buy_requests_id_seq'::regclass);


--
-- Name: billings_payments id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_payments ALTER COLUMN id SET DEFAULT nextval('public.billings_payments_id_seq'::regclass);


--
-- Name: buy_request_miner_items id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.buy_request_miner_items ALTER COLUMN id SET DEFAULT nextval('public.buy_request_miner_items_id_seq'::regclass);


--
-- Name: buy_requests id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.buy_requests ALTER COLUMN id SET DEFAULT nextval('public.buy_requests_id_seq'::regclass);


--
-- Name: countries id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.countries ALTER COLUMN id SET DEFAULT nextval('public.countries_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: feedbacks id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.feedbacks ALTER COLUMN id SET DEFAULT nextval('public.feedbacks_id_seq'::regclass);


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Name: markets_carts id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.markets_carts ALTER COLUMN id SET DEFAULT nextval('public.markets_carts_id_seq'::regclass);


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: miner_items id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.miner_items ALTER COLUMN id SET DEFAULT nextval('public.miner_items_id_seq'::regclass);


--
-- Name: miner_items_categories id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.miner_items_categories ALTER COLUMN id SET DEFAULT nextval('public.miner_items_categories_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: payments_sites id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.payments_sites ALTER COLUMN id SET DEFAULT nextval('public.payments_sites_id_seq'::regclass);


--
-- Name: purchases_records id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.purchases_records ALTER COLUMN id SET DEFAULT nextval('public.purchases_records_id_seq'::regclass);


--
-- Name: settings id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.settings ALTER COLUMN id SET DEFAULT nextval('public.settings_id_seq'::regclass);


--
-- Name: tickets id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.tickets ALTER COLUMN id SET DEFAULT nextval('public.tickets_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: workers id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.workers ALTER COLUMN id SET DEFAULT nextval('public.workers_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: balances balances_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.balances
    ADD CONSTRAINT balances_pkey PRIMARY KEY (id);


--
-- Name: billings_buy_requests billings_buy_requests_billing_id_key; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_buy_requests
    ADD CONSTRAINT billings_buy_requests_billing_id_key UNIQUE (billing_id);


--
-- Name: billings_buy_requests billings_buy_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_buy_requests
    ADD CONSTRAINT billings_buy_requests_pkey PRIMARY KEY (id);


--
-- Name: billings_payments billings_payments_billing_id_key; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_payments
    ADD CONSTRAINT billings_payments_billing_id_key UNIQUE (billing_id);


--
-- Name: billings_payments billings_payments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_payments
    ADD CONSTRAINT billings_payments_pkey PRIMARY KEY (id);


--
-- Name: billings billings_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings
    ADD CONSTRAINT billings_pkey PRIMARY KEY (id);


--
-- Name: buy_request_miner_items buy_request_miner_items_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.buy_request_miner_items
    ADD CONSTRAINT buy_request_miner_items_pkey PRIMARY KEY (id);


--
-- Name: buy_requests buy_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.buy_requests
    ADD CONSTRAINT buy_requests_pkey PRIMARY KEY (id);


--
-- Name: countries countries_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_name_key UNIQUE (name);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: employees employees_email_key; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_email_key UNIQUE (email);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: feedbacks feedbacks_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.feedbacks
    ADD CONSTRAINT feedbacks_name_key UNIQUE (name);


--
-- Name: feedbacks feedbacks_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.feedbacks
    ADD CONSTRAINT feedbacks_pkey PRIMARY KEY (id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: markets_carts markets_carts_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.markets_carts
    ADD CONSTRAINT markets_carts_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: miner_items_categories miner_items_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.miner_items_categories
    ADD CONSTRAINT miner_items_categories_pkey PRIMARY KEY (id);


--
-- Name: miner_items miner_items_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.miner_items
    ADD CONSTRAINT miner_items_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: payments_sites payments_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.payments_sites
    ADD CONSTRAINT payments_sites_pkey PRIMARY KEY (id);


--
-- Name: purchases_records purchases_records_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.purchases_records
    ADD CONSTRAINT purchases_records_pkey PRIMARY KEY (id);


--
-- Name: resets_passwords_requests resets_passwords_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.resets_passwords_requests
    ADD CONSTRAINT resets_passwords_requests_pkey PRIMARY KEY (id);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- Name: tickets tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_phone_key; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: workers workers_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.workers
    ADD CONSTRAINT workers_pkey PRIMARY KEY (id);


--
-- Name: balances balances_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.balances
    ADD CONSTRAINT balances_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: billings_buy_requests billings_buy_requests_billing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_buy_requests
    ADD CONSTRAINT billings_buy_requests_billing_id_fkey FOREIGN KEY (billing_id) REFERENCES public.billings(id) ON DELETE SET NULL;


--
-- Name: billings_buy_requests billings_buy_requests_buy_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_buy_requests
    ADD CONSTRAINT billings_buy_requests_buy_request_id_fkey FOREIGN KEY (buy_request_id) REFERENCES public.buy_requests(id) ON DELETE SET NULL;


--
-- Name: billings billings_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings
    ADD CONSTRAINT billings_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(id) ON DELETE SET NULL;


--
-- Name: billings_payments billings_payments_billing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_payments
    ADD CONSTRAINT billings_payments_billing_id_fkey FOREIGN KEY (billing_id) REFERENCES public.billings(id) ON DELETE SET NULL;


--
-- Name: billings_payments billings_payments_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings_payments
    ADD CONSTRAINT billings_payments_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id) ON DELETE SET NULL;


--
-- Name: billings billings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.billings
    ADD CONSTRAINT billings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: buy_request_miner_items buy_request_miner_items_buy_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.buy_request_miner_items
    ADD CONSTRAINT buy_request_miner_items_buy_request_id_fkey FOREIGN KEY (buy_request_id) REFERENCES public.buy_requests(id) ON DELETE SET NULL;


--
-- Name: buy_request_miner_items buy_request_miner_items_miner_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.buy_request_miner_items
    ADD CONSTRAINT buy_request_miner_items_miner_item_id_fkey FOREIGN KEY (miner_item_id) REFERENCES public.miner_items(id) ON DELETE SET NULL;


--
-- Name: buy_requests buy_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.buy_requests
    ADD CONSTRAINT buy_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: markets_carts markets_carts_miner_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.markets_carts
    ADD CONSTRAINT markets_carts_miner_item_id_fkey FOREIGN KEY (miner_item_id) REFERENCES public.miner_items(id) ON DELETE SET NULL;


--
-- Name: markets_carts markets_carts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.markets_carts
    ADD CONSTRAINT markets_carts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: messages messages_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(id) ON DELETE SET NULL;


--
-- Name: messages messages_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id) ON DELETE SET NULL;


--
-- Name: miner_items miner_items_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.miner_items
    ADD CONSTRAINT miner_items_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.miner_items_categories(id) ON DELETE SET NULL;


--
-- Name: miner_items miner_items_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.miner_items
    ADD CONSTRAINT miner_items_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(id) ON DELETE SET NULL;


--
-- Name: payments_sites payments_sites_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.payments_sites
    ADD CONSTRAINT payments_sites_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id) ON DELETE SET NULL;


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: purchases_records purchases_records_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.purchases_records
    ADD CONSTRAINT purchases_records_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: resets_passwords_requests resets_passwords_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.resets_passwords_requests
    ADD CONSTRAINT resets_passwords_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: tickets tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: users users_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(id) ON DELETE SET NULL;


--
-- Name: workers workers_miner_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.workers
    ADD CONSTRAINT workers_miner_item_id_fkey FOREIGN KEY (miner_item_id) REFERENCES public.miner_items(id) ON DELETE SET NULL;


--
-- Name: workers workers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY public.workers
    ADD CONSTRAINT workers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

