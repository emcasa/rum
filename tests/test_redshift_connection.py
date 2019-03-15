from unittest import mock
from rum.connection.database import Redshift


@mock.patch("psycopg2.connect")
def test_redshift_connection_init(patched_db_connection):
    expected = patched_db_connection.return_value
    result = Redshift().connection

    assert expected == result


