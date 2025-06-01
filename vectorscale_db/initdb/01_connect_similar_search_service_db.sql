-- Connect to the created database and enable necessary extensions

\connect similarity_search_service_db

CREATE EXTENSION IF NOT EXISTS vector CASCADE;
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;
