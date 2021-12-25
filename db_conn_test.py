import psycopg2 as pg
from configparser import ConfigParser
import os
from pathlib import Path

# get the config file 
path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_filepath = os.path.join(ROOT_DIR, "config.ini")


# taken from https://www.geeksforgeeks.org/postgresql-connect-to-postgresql-database-server-in-python/
def config(filename, section):
    # create a parser
    config = ConfigParser()
    # read config file
    config.read(filename)

    # get section
    db = {}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """Connect to the db server"""
    conn = None
    try:
        # connection parameters
        params = config(config_filepath, 'NFL')

        # connect to the db
        print("Connecting to the database server....")
        conn = pg.connect(**params)

        cur = conn.cursor()

        # test statement
        print("PostgreSQL version:")
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        cur.close()

    except (Exception, pg.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect()