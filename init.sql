-- Connect to the workforcehub database
\c workforcehub

-- Grant all privileges on the public schema to workforcehub_admin
GRANT ALL ON SCHEMA public TO workforcehub_admin;

-- Alter the owner of the database to workforcehub_admin
ALTER DATABASE workforcehub OWNER TO workforcehub_admin;
