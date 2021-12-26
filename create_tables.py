import psycopg2 as pg
import os
from pathlib import Path
from config import config 
from sql_queries import create_tables, drop_tables 


# get the config file 
path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_filepath = os.path.join(ROOT_DIR, "config.ini")

# connection credentials to the default database
# requires credentials stored in config.ini in the same directory
pg_params = config(config_filepath, 'postgres')
nfl_params = config(config_filepath, 'NFL')

def createDatabase():
    """ 
    creates a fresh database called nflSpecialTeams
    returns the connection and cursor to the new database

    """
    # connect to the user's default db to create working db
    conn = pg.connect(**pg_params)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create db
    cur.execute("DROP DATABASE IF EXISTS nflSpecialTeams")
    cur.execute("CREATE DATABASE nflSpecialTeams WITH ENCODING 'utf8' TEMPLATE template0")
  
    conn.close()

    # connect to the nfl database
    conn = pg.connect(**nfl_params)
    cur = conn.cursor()

    return cur, conn

def createTables(cur, conn):
    """
    creates each table
    """
    for query in create_tables:
        cur.execute(query)
        conn.commit()

def dropTables(cur, conn):
    """
    drops each table
    """
    for query in drop_tables:
        cur.execute(query)
        conn.commit()

def main():
    """
    Drops (if exists) and Creates the nfl database, establishes a connection, gets a cursor
    Drops all the tables
    Creates all tables needed
    Closes the connection
    """
    conn = None
    try: 
        print("Creating the Database...")
        cur, conn = createDatabase()
        
        dropTables(cur, conn)

        print("Building tables...")
        createTables(cur, conn)

        conn.close()
    
    except (Exception, pg.DatabaseError) as error:
        print(error)

    finally: 
        if conn is not None:
            conn.close()
            print("Database Connection closed.")

if __name__ == "__main__":
    main()