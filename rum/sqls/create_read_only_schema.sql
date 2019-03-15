-- Create a schema and grant ownership to a specific user
CREATE SCHEMA {0} AUTHORIZATION {1};
-- Grant read only permissions to group users
GRANT USAGE ON SCHEMA {0} TO GROUP read_only;
ALTER DEFAULT PRIVILEGES for user {1} IN SCHEMA {0} GRANT SELECT ON TABLES to group read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA {0} TO GROUP read_only;

