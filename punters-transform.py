# script for extracting and transforming nfl punter data from the nfl big data bowl dataset
# original data can be found here: https://www.kaggle.com/c/nfl-big-data-bowl-2022
###############################################################################################

# imports
import os
import numpy as np 
import pandas as pd 

# path to a logical place where one might store their data
filepath = os.path.expanduser('~/Documents/code/nfl-big-data-bowl/data/')

# get data
players = pd.read_csv(filepath + 'players.csv')
plays = pd.read_csv(filepath + 'plays.csv')
scouting = pd.read_csv(filepath + 'PFFScoutingData.csv')

# 1) ADDING # OF PUNTS 
# isolate the punters
punters = players[players['Position']=='P']

# get the number of punts
num_punts = plays[plays['specialTeamsPlayType']=='Punt']['kickerId'].value_counts().reset_index().rename(columns={'kickerId': 'num_punts', 'index':'nflId'})

# merge number with the punters dataframe
punters = pd.merge(punters, num_punts, how='left',on='nflId')

#print(punters.head())

# 2) ADDING STATISTICS FROM SCOUTING DATA
### 2.1) Get only the punts from the scouting data:  

# dataframe of only the punts
scouting_punts = scouting[scouting['kickType'].isin(['N','A','R'])]

# dropping all the unnecessary fields
scouting_punts = scouting_punts.drop(['missedTackler','assistTackler','tackler',
                                      'kickoffReturnFormation','gunners','puntRushers',
                                      'specialTeamsSafeties','vises','returnDirectionIntended',
                                      'returnDirectionActual',], axis=1)

# the punt_map df is used to join the plays data with the scouting data
punt_map = plays[plays['specialTeamsPlayType']=="Punt"].drop(['specialTeamsPlayType','returnerId','kickBlockerId'], axis=1)
punt_map = punt_map.rename(columns={'kickerId':'punterId'})
scouting_punts = scouting_punts.merge(punt_map, how='left',on=['gameId','playId'])

# adding a column for punts that went the correct direction
scouting_punts['kickDirectionCorrect'] = scouting_punts['kickDirectionIntended']==scouting_punts['kickDirectionActual']

# removing the direction columns that are now useless
scouting_punts = scouting_punts.drop(['kickDirectionIntended','kickDirectionActual'], axis=1)

print(scouting_punts.columns)

### 2.2) Adding categorical statistics. This section adds in various ratios of the punt categories. See README for more information.

# view the number of each of the categorical punts
punters_summed_dummy_columns = pd.get_dummies(scouting_punts, columns=['kickType','kickContactType','kickDirectionCorrect']).groupby(['punterId']).sum()

# styles of punting
punting_styles = punters_summed_dummy_columns[['kickType_A','kickType_N','kickType_R']]
punting_styles['normalPuntRatio'] = punting_styles['kickType_N']/(punting_styles['kickType_A'] + punting_styles['kickType_N'] + punting_styles['kickType_R'])
punting_styles = punting_styles.reset_index()
punting_styles['nflId'] = punting_styles['punterId'] 
punting_styles = punting_styles.drop(['kickType_A','kickType_N','kickType_R','punterId'], axis=1)


# punts fielded
punts_fielded = punters_summed_dummy_columns[['kickContactType_BB','kickContactType_BC','kickContactType_BF',
                                              'kickContactType_BOG','kickContactType_CC','kickContactType_CFFG',
                                              'kickContactType_DEZ','kickContactType_ICC','kickContactType_KTB',
                                              'kickContactType_KTC','kickContactType_KTF','kickContactType_MBC',
                                              'kickContactType_MBDR','kickContactType_OOB']]
punts_fielded_sum = punts_fielded['kickContactType_BB'] + punts_fielded['kickContactType_BC'] + punts_fielded['kickContactType_BF'] + punts_fielded['kickContactType_BOG'] + punts_fielded['kickContactType_CC'] + punts_fielded['kickContactType_CFFG'] + punts_fielded['kickContactType_DEZ'] + punts_fielded['kickContactType_ICC'] + punts_fielded['kickContactType_KTB'] + punts_fielded['kickContactType_KTC'] + punts_fielded['kickContactType_KTF'] + punts_fielded['kickContactType_MBC'] + punts_fielded['kickContactType_MBDR'] + punts_fielded['kickContactType_OOB']
punts_fielded['caughtRatio'] = (punts_fielded['kickContactType_BC'] + punts_fielded['kickContactType_CC'])/punts_fielded_sum
punts_fielded['groundRatio'] = (punts_fielded['kickContactType_BB'] + punts_fielded['kickContactType_BOG'] + punts_fielded['kickContactType_CFFG'])/punts_fielded_sum
punts_fielded['kickTeamTouchedFirstRatio'] = (punts_fielded['kickContactType_KTB'] + punts_fielded['kickContactType_KTF'] + punts_fielded['kickContactType_KTC'])/punts_fielded_sum
punts_fielded['outOfBoundsRatio'] = punts_fielded['kickContactType_OOB']/punts_fielded_sum
punts_fielded['outOfEZRatio'] = punts_fielded['kickContactType_DEZ']/punts_fielded_sum
punts_fielded = punts_fielded.reset_index()
punts_fielded['nflId'] = punts_fielded['punterId']
punts_fielded = punts_fielded.drop(['kickContactType_BB','kickContactType_BC','kickContactType_BF',
                                              'kickContactType_BOG','kickContactType_CC','kickContactType_CFFG',
                                              'kickContactType_DEZ','kickContactType_ICC','kickContactType_KTB',
                                              'kickContactType_KTC','kickContactType_KTF','kickContactType_MBC',
                                              'kickContactType_MBDR','kickContactType_OOB','punterId'], axis=1)


# kick direction intended
punts_kick_direction_intended = punters_summed_dummy_columns[['kickDirectionCorrect_True','kickDirectionCorrect_False']]
punts_kick_direction_intended['intendedDirectionRatio'] = punts_kick_direction_intended['kickDirectionCorrect_True']/(punts_kick_direction_intended['kickDirectionCorrect_True']+punts_kick_direction_intended['kickDirectionCorrect_False'])
punts_kick_direction_intended = punts_kick_direction_intended.reset_index()
punts_kick_direction_intended['nflId'] = punts_kick_direction_intended['punterId']
punts_kick_direction_intended = punts_kick_direction_intended.drop(['punterId','kickDirectionCorrect_True','kickDirectionCorrect_False'], axis=1)

# merge those dataframes to the main punters dataset
punters = punters.merge(punting_styles, on='nflId')
punters = punters.merge(punts_fielded, on='nflId')
punters = punters.merge(punts_kick_direction_intended, on='nflId')

### 2.3) Add numerical categories 
# drop unecessary columns
punt_hts = scouting_punts.drop(['gameId','playId','snapDetail','snapTime','operationTime','kickType','kickContactType','kickDirectionCorrect'], axis=1)

# calculate mean and max ht by punter
punt_hts = punt_hts.groupby('punterId').agg(meanHangTime = ('hangTime','mean'),maxHangTime = ('hangTime','max')).reset_index()
punt_hts = punt_hts.rename(columns={'punterId':'nflId'})

# join it to the main set
punters = punters.merge(punt_hts, on='nflId')

# print(punters.head())

# 3) EXPORT
# will drop it in the same place it got the data from
punters.to_csv(filepath + 'punters.csv')
