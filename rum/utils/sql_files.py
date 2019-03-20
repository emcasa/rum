
def open_sql_file(filename: str) -> str:
    with open('sqls/{}.sql'.format(filename)) as sql_file:
        return sql_file.read()
