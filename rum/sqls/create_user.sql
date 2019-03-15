-- Create new user
CREATE USER {} WITH PASSWORD '{}';
-- Limit concurrent connections from user to 20
ALTER USER {} WITH CONNECTION LIMIT 20;
-- Set user default timeout to 5 minutes
ALTER USER {} WITH SET statement_timeout to 300000;
