import psycopg2
import os


class Redshift(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

            try:
                db_config = {'dbname': os.environ['DBNAME'],
                             'host': os.environ['HOST'],
                             'password': os.environ['PWD'],
                             'port': os.environ['PORT'],
                             'user': os.environ['USER']}
            except KeyError as error:
                Redshift._instance = None
                raise KeyError('Error: Please set connection credentials as environmental vars. {}'.format(error))

            try:
                print('connecting to Redshift database...')
                connection = Redshift._instance.connection = psycopg2.connect(**db_config)
                cursor = Redshift._instance.cursor = connection.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()
            except Exception as error:
                Redshift._instance = None
                raise ConnectionError('Error: connection not established {}'.format(error))
            else:
                print('connection established\n{}'.format(db_version[0]))

        return cls._instance

    def __init__(self):
            self.connection = self._instance.connection
            self.cursor = self._instance.cursor

    def query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as error:
            raise ValueError('Error executing query "{}", error: {}'.format(query, error))
        else:
            return self.cursor

    def __del__(self):
            self.connection.close()
            self.cursor.close()
            print('Redshift connection closed.')

