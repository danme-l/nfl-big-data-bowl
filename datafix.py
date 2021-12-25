import numpy as np
import pandas as pd
import os

# tables have NA's that need to be replaced with null's 

# data location
filepath = os.path.expanduser('~/Documents/code/nfl-big-data-bowl/data/')

# get data
players = pd.read_csv(filepath + 'players.csv')
plays = pd.read_csv(filepath + 'plays.csv')
PFFScoutingData = pd.read_csv(filepath + 'PFFScoutingData.csv')
punters = pd.read_csv(filepath + 'punters.csv')
kickers = pd.read_csv(filepath + 'kickers.csv')

# make a dictionary to iterate over
data = {'players': players,
        'plays': plays,
        'PFFScoutingData': PFFScoutingData,
        'punters': punters,
        'kickers': kickers}

for file, df in data.items():
	# nulls 
    df = df.replace('NULL', np.nan)
    df.to_csv(filepath + f'{file}.csv', index=False)