-- remove user from group read_only and them drop user
ALTER GROUP read_only DROP USER {0};
DROP USER {0};