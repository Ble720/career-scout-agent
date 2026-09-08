-- init.sql
-- Enables pgvector extension for storing and querying 768-dim Gemini embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable uuid-ossp extension in case UUID primary keys are needed in the future
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";