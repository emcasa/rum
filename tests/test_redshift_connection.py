from unittest import mock
from rum.connection.database import Redshift
import os

os.environ['dbname'] = ''
os.environ['host'] = ''
os.environ['pwd'] = ''
os.environ['port'] = ''
os.environ['user'] = ''


@mock.patch("psycopg2.connect")
def test_redshift_connection_init(patched_db_connection):
    expected = patched_db_connection.return_value
    result = Redshift().connection

    assert expected == result


@mock.patch("psycopg2.connect")
def test_redshift_query(patched_db_connection):
    mock_cur = patched_db_connection.return_value.cursor.return_value
    expected = mock_cur.execute.return_value
    result = Redshift().query('SELECT * FROM A')

    assert expected == result

