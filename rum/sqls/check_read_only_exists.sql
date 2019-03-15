-- Checks if read_only group is already created
select 'read_only' in (select groname from pg_group)