import numpy as np
import pandas as pd
import os 
import csv
import psycopg2 as pg
from sqlalchemy import create_engine
from sql_queries import *
from config import config

data_path = os.path.expanduser('~/Documents/code/nfl-big-data-bowl/data/')
config_filepath = os.path.expanduser('~/Documents/code/nfl-big-data-bowl/') + 'config.ini'

nfl_params = config(config_filepath, 'NFL')

def loadGames(cur, conn, query):
    """
    Load Games:
    Accepts a database cursor, a database connection, and an insertion query
    Gets the data from a csv file
    Attempts to load data into the database 
    """
    try:
        games_csv = csv.reader(open(data_path + 'games.csv'))
        header = next(games_csv)

        print(' - loading games')
        for row in games_csv:
            print(row)
            cur.execute(query, row)

        print(' - games loaded.')
        conn.commit()

    except FileNotFoundError:
        print("CSV file not found.")

def loadPlays(cur, conn, query):
    """
    Load Plays:
    Accepts a database cursor, a database connection, and an insertion query
    Gets the data from a csv file
    Attempts to load data into the database 
    """
    try:
        plays_csv = csv.reader(open(data_path + 'plays.csv'))
        header = next(plays_csv)

        print(' - loading plays')
        for row in plays_csv:
            print(row)
            cur.execute(query, row)

        print(' - plays loaded.')
        conn.commit()

    except FileNotFoundError:
        print("CSV file not found.")

def loadPlayers(cur, conn, query):
    """
    Load Players
    Accepts a database cursor, a database connection, and an insertion query
    Gets the data from a csv file
    Attempts to load data into the database 
    """
    try:
        players_csv = csv.reader(open(data_path + 'players.csv'))
        header = next(players_csv)

        print(' - loading players')
        for row in players_csv:
            print(row)
            cur.execute(query, row)

        print(' - players loaded.')
        conn.commit()

    except FileNotFoundError:
        print("CSV file not found.")

def loadPunters(cur, conn, query):
    """
    Load Punters:
    Accepts a database cursor, a database connection, and an insertion query
    Gets the data from a csv file
    Attempts to load data into the database 
    """
    try:
        punters_csv = csv.reader(open(data_path + 'punters.csv'))
        header = next(punters_csv)

        print(' - loading punters')
        for row in punters_csv:
            print(row)
            cur.execute(query, row)

        print(' - punters loaded.')
        conn.commit()

    except FileNotFoundError:
        print("CSV file not found.")

def loadKickers(cur, conn, query):
    """
    Load Kickers
    Accepts a database cursor, a database connection, and an insertion query
    Gets the data from a csv file
    Attempts to load data into the database 
    """
    try:
        kickers_csv = csv.reader(open(data_path + 'kickers.csv'))
        header = next(kickers_csv)

        print(' - loading kickers')
        for row in kickers_csv:
            print(row)
            cur.execute(query, row)

        print(' - kickers loaded.')
        conn.commit()

    except FileNotFoundError:
        print("CSV file not found.")

def loadPFFScouting(cur, conn, query):
    """
    Load PFF Scouting
    Accepts a database cursor, a database connection, and an insertion query
    Gets the data from a csv file
    Attempts to load data into the database 
    """
    try:
        scouting_csv = csv.reader(open(data_path + 'PFFScoutingData.csv'))
        header = next(scouting_csv)

        print(' - loading PFF Scouting')
        for row in scouting_csv:
            print(row)
            cur.execute(query, row)

        print(' - PFF Scouting loaded.')
        conn.commit()

    except FileNotFoundError:
        print("CSV file not found.")

def test():
    # quick test connection function
    conn = None
    
    try:
        print("Connecting ... ")
        
        games = pd.read_csv(data_path + 'games.csv')        
        connection_info = 'postgresql+psycopg2://'+nfl_params['user']+':'+nfl_params['password']+'@'+nfl_params['host']+':'+nfl_params['port']+'/'+nfl_params['database']
        engine = create_engine(connection_info)

        games.to_sql('games',con=engine, if_exists='replace')
        engine.execute(games_insert)        

        sample = engine.fetchall()
        print(sample)
        conn.close()


    finally:
        if conn is not None:
            conn.close()
            print("Database Connection closed.")

def main():
    """
    Establishes a connection to the db
    Executes all the load functions
    """
    conn = None
    try: 
        # connect
        print("Connecting ... ")
        conn = pg.connect(**nfl_params)
        cur = conn.cursor()

        # load
        print("Loading games ... ")
        loadGames(cur, conn, games_insert)

        print("Loading plays ...")
        loadPlays(cur, conn, plays_insert)

        print("Load players ...")
        loadPlayers(cur, conn, players_insert)

        print("Load PFF Scouting ...")
        loadPFFScouting(cur, conn, insert_pffScouting)

        print("Load Punters ...")
        loadPunters(cur, conn, insert_punters)

        print("Load Kickers ...")
        loadKickers(cur, conn, insert_kickers)
        
        conn.close()
    
    except (Exception, pg.DatabaseError) as error:
        print(error)

    finally: 
        if conn is not None:
            conn.close()
            print("Database Connection closed.")

if __name__ == "__main__":
    main()
    # test()