import psycopg2
import os


class Redshift(object):
    def __init__(self):
        # Config DB credentials
        db_config = {'dbname': os.environ.get('DBNAME', 'database'),
                     'host': os.environ.get('HOST', 'localhost'),
                     'password': os.environ.get('PASSWORD', ''),
                     'port': os.environ.get('PORT', '5439'),
                     'user': os.environ.get('USER', 'user')}

        # Connect to DB
        try:
            print('connecting to Redshift database...')
            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('SELECT VERSION()')
            db_version = cursor.fetchone()
        except Exception as error:
            raise ConnectionError('Error: connection not established {}'.format(error))
        else:
            print('connection established\n{}'.format(db_version[0]))

        # Define connection and cursor objects
        self.connection = connection
        self.cursor = cursor

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
