# script for extracting and transforming nfl kicker data from the nfl big data bowl dataset
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
games = pd.read_csv(filepath + 'games.csv')

# 1) ADDING NUMBER OF KICKOFFS AND FIELD GOALS
# isolate kickers
kickers = players[players["Position"]=="K"]

# get the number of kickoffs and field goals 
num_kickoffs = plays[plays['specialTeamsPlayType']=='Kickoff']['kickerId'].value_counts().reset_index().rename(columns={'kickerId': 'num_kickoffs', 'index':'nflId'})
num_field_goals = plays[plays['specialTeamsPlayType']=='Field Goal']['kickerId'].value_counts().reset_index().rename(columns={'kickerId': 'num_field_goals', 'index':'nflId'})

# merge numbers with the kickers df
kickers = kickers.merge(num_kickoffs, on='nflId')
kickers = kickers.merge(num_field_goals, on='nflId')

# 2) KICKOFFS
# get kickoffs from the plays df
kickoffs = plays[plays['specialTeamsPlayType'] == 'Kickoff']

# drop unecessary columns
kickoffs = kickoffs.drop(['playDescription', 'quarter', 'down', 'yardsToGo',
       'possessionTeam', 'specialTeamsPlayType',
       'kickBlockerId', 'yardlineSide',
       'yardlineNumber', 'gameClock', 'penaltyCodes', 'penaltyJerseyNumbers',
       'penaltyYards', 'preSnapHomeScore', 'preSnapVisitorScore', 'passResult',],axis=1)

# get kickoffs from the scouting df
scouting_kos = scouting[scouting['kickType'].isin(['D','F','K','O','P','Q','S','B'])]

# add intended direction column
scouting_kos['kickDirectionCorrect'] = scouting_kos['kickDirectionIntended']==scouting_kos['kickDirectionActual']

# drop unecessary columns
scouting_kos = scouting_kos.drop(['snapDetail','snapTime','operationTime',
                                  'kickDirectionIntended','kickDirectionActual',
                                  'missedTackler','assistTackler','tackler',
                                  'gunners','puntRushers','vises',
                                  'specialTeamsSafeties','kickContactType',
                                  'kickoffReturnFormation'], axis=1)

# join with the plays df
kos = scouting_kos.merge(kickoffs, on=['gameId','playId'])

# calculating the mean and max kickoff distances and hangtimes on deep kicks
deep_kos = kos[kos['kickType']=='D']
deep_kos = deep_kos.groupby('kickerId').agg(meanKickoffDistance=('kickLength','mean'),
                                            maxKickoffDistance=('kickLength','max'),
                                            meanKickoffHangtime=('hangTime','mean'),
                                            maxKickoffHantime=('hangTime','max')).reset_index().rename(columns={'kickerId':'nflId'})
# join it to the main set
kickers = kickers.merge(deep_kos, on='nflId', how='left')

# view the number of each of the categorical kicks
# it's going to sum up the gameId's, playId's, hangtimes, etc over each player as well, which is obviously nonsensical, but I'm not using these so it doesn't matter in this context
# those will get dropped from the df before it is merged with the kickers df
kickers_summed_dummy_columns = pd.get_dummies(kos, columns=['kickType','specialTeamsResult','kickDirectionCorrect']).groupby(['kickerId']).sum()

# column for the number of kicks
kickers_summed_dummy_columns['numKickoffs'] = kickers_summed_dummy_columns['kickType_B'] + kickers_summed_dummy_columns['kickType_D'] + kickers_summed_dummy_columns['kickType_F'] + kickers_summed_dummy_columns['kickType_K'] + kickers_summed_dummy_columns['kickType_O'] + kickers_summed_dummy_columns['kickType_P'] + kickers_summed_dummy_columns['kickType_Q'] + kickers_summed_dummy_columns['kickType_S'] 

# direction intended
kickers_summed_dummy_columns['intendedDirectionRatio'] = kickers_summed_dummy_columns['kickDirectionCorrect_True']/(kickers_summed_dummy_columns['kickDirectionCorrect_True']+kickers_summed_dummy_columns['kickDirectionCorrect_False'])

# calculate touchback ratio on deep kicks 
kickers_summed_dummy_columns['touchbackRatio'] = kickers_summed_dummy_columns['specialTeamsResult_Touchback']/kickers_summed_dummy_columns['kickType_D']

# calculate out of bounds ratio
kickers_summed_dummy_columns['OOBRatio'] = kickers_summed_dummy_columns['kickType_B']/kickers_summed_dummy_columns['numKickoffs']

# calculate onside ratio and recovery rate
kickers_summed_dummy_columns['onsideRatio'] = kickers_summed_dummy_columns['kickType_O']/kickers_summed_dummy_columns['numKickoffs']
kickers_summed_dummy_columns['onsideRecoveryRate'] = kickers_summed_dummy_columns['specialTeamsResult_Kickoff Team Recovery']/kickers_summed_dummy_columns['kickType_O']

# fix the df for joining
kickers_summed_dummy_columns = kickers_summed_dummy_columns.reset_index().rename(columns={'kickerId':'nflId'})
kickers_summed_dummy_columns = kickers_summed_dummy_columns.drop(kickers_summed_dummy_columns.columns[[x for x in range(1,26)]], axis=1)

# join the new stats columns to the main kickers df
kickers = kickers.merge(kickers_summed_dummy_columns, on='nflId')

# 3) FIELD GOALS 

# functions for the clutch kick indicator
def encodeKickingTeamScore(df):
    """ Uses the home, away, and possession teams from the games df to add a kicking team
        score column when applied (with df.apply()) to the games df"""

    if df['possessionTeam'] == df['homeTeamAbbr']:
        return df['preSnapHomeScore']
    else:
        return df['preSnapVisitorScore']
    
def encodeDefendingTeamScore(df):
    """ Uses the home, away, and possession teams from the games df to add a defending team
        score column when applied (with df.apply()) to the games df"""

    if df['possessionTeam'] == df['visitorTeamAbbr']:
        return df['preSnapHomeScore']
    else:
        return df['preSnapVisitorScore']

def clutchKickIndicator(df):
    """ Function to apply to the df to indicate that a given kick was made in the clutch
        i.e. last three minutes of the game to tie or take the lead"""

    if df['clutchKickIndicator']:
        if 0<= df['defendingTeamScore']-df['kickingTeamScore'] <= 3:
            if df['specialTeamsResult']=='Kick Attempt Good':
                return 1
            elif df['specialTeamsResult']=='Kick Attempt No Good':
                return 0
    else:
        return np.NaN

# get a field goals df, drop unecessary columns
field_goals = plays[plays['specialTeamsPlayType'] == 'Field Goal'].drop(['playDescription', 
                                                                         'specialTeamsPlayType', 'yardlineSide','yardlineNumber',
                                                                         'returnerId', 'kickBlockerId', 'yardsToGo',
                                                                         'penaltyCodes', 'penaltyJerseyNumbers',
                                                                         'penaltyYards', 'passResult',
                                                                         'kickReturnYardage', 'playResult',
                                                                         ], axis=1)

# bring in the home and away columns from the games dataset 
field_goals = field_goals.merge(games[['gameId','homeTeamAbbr','visitorTeamAbbr']], on='gameId')

# add the clutch kick indicator
field_goals['clutchKickIndicator'] = (field_goals['gameClock'].str.slice(start=0, stop=2).isin(['02','01','00'])) & (field_goals['quarter'] == 4)

# add the more useful score columns
field_goals['kickingTeamScore'] = field_goals.apply(encodeKickingTeamScore, axis=1).astype('int64')
field_goals['defendingTeamScore'] = field_goals.apply(encodeDefendingTeamScore, axis=1).astype('int64')

# add the clutch kick made and missed for stats
field_goals['clutchKickMade'] = field_goals.apply(clutchKickIndicator, axis=1)
field_goals['clutchKickMissed'] = field_goals['clutchKickMade'] == 0

# get rid of a couple columns now made redundant
field_goals = field_goals.drop(['preSnapHomeScore','preSnapVisitorScore',], axis=1)

# mean and max kicks made
kicks_made_stats = field_goals[field_goals['specialTeamsResult'] == 'Kick Attempt Good'].groupby('kickerId').agg(meanKickLength_hit=('kickLength','mean'),
                                                                                                                 maxKickLength_hit=('kickLength','max'),
                                                                                                                 clutchKicksMade=('clutchKickMade','sum')).reset_index().rename(columns={'kickerId':'nflId'})

# mean, min and max kicks missed
kicks_missed_stats = field_goals[field_goals['specialTeamsResult'] == 'Kick Attempt No Good'].groupby('kickerId').agg(meanKickLength_missed=('kickLength','mean'),
                                                                                                                 maxKickLength_missed=('kickLength','max'),
                                                                                                                 shortestKickLength_missed=('kickLength','min'),
                                                                                                                 clutchKicksMissed=('clutchKickMissed','sum')).reset_index().rename(columns={'kickerId':'nflId'})

# finally, add these to the kickers df
kickers = kickers.merge(kicks_made_stats, on='nflId')
kickers = kickers.merge(kicks_missed_stats, on='nflId')

# print(kickers.head())

# 4) EXPORT 
# will drop it in the same place it got the data from
kickers.to_csv(filepath + 'kickers.csv')