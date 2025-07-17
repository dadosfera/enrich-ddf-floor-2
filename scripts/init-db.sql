-- Database initialization script for Enrich DDF Floor 2

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create basic tables will be handled by Alembic migrations
-- This file is for any additional database setup

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE enrich_ddf_floor2 TO postgres;

-- Create any initial data if needed
-- (Add initial data setup here in future iterations) 