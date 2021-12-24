
# create tables
create_table_games = ("""
    CREATE TABLE IF NOT EXISTS games(
        gameId integer PRIMARY KEY,
        season smallint,
        week smallint,
        gameDate date,
        homeTeamAbbr varchar(3),
        visitorTeamAbbr varchar(3)
    )
""")

create_table_players = ("""
    CREATE TABLE IF NOT EXISTS players(
        nflId integer PRIMARY KEY,
        height varchar(3),
        weight smallint,
        collegeName varchar(40),
        position varchar(3),
        displayName varchar(25)
    )
""")

create_table_plays = ("""
    CREATE TABLE IF NOT EXISTS plays(
        gameId integer,
        playId integer,
        playDescription varchar(450),
        quarter smallint,
        down smallint,
        yardsToGo smallint,
        possessionTeam varchar(3),
        specialTeamsPlayType varchar(13),
        specialTeamsResult varchar(21),
        kickerId integer,
        returnerId integer,
        kickBlockerId integer,
        yardlineSide varchar(3),
        yadlineNumber smallint,
        gameclock varchar(8),
        penaltyCodes varchar(10),
        penaltyJerseyNumbers varchar(10),
        penaltyYards smallint,
        preSnapHomeScore smallint,
        preSnapVisitorScore smallint,
        passResult varchar(10),
        kickLength smallint,
        kickReturnYardage smallint,
        playResult smallint,
        absoluteYardlineNumber smallint,
        primary key (gameId, playId)
    )
""")

create_table_PFFscouting = ("""
CREATE TABLE IF NOT EXISTS pffScouting(
        gameId integer,
        playId integer,
        snapDetail varchar(3),
        snapTime decimal,
        operationTime decimal,
        hangTime decimal,
        kickType varchar(3),
        kickDirectionIntended varchar(3),
        kickDirectionActual varchar(3),
        returnDirectionInteded varchar(3),
        returnDirectionActual varchar(3),
        missedTackler varchar(38),
        assisstTackler varchar(6),
        tackler varchar(6),
        kickoffReturnFormation varchar(6),
        gunners varchar(30),
        puntRushers varchar(86),
        specialTeamsSafeties varchar(46),
        vises varchar(38),
        kickContactType varchar(4),
        PRIMARY KEY (gameId, playId)
    )
""")


create_table_punters = ("""
    CREATE TABLE IF NOT EXISTS punters(
        dummyIndex smallint,
        nflId integer PRIMARY KEY,
        height varchar(3),
        weight smallint,
        collegeName varchar(40),
        position varchar(3),
        displayName varchar(25),
        num_punts smallint,
        normalPuntRatio decimal,
        caughtRatio decimal,
        groundRatio decimal,
        kickTeamTouchedFirstRatio decimal,
        outOfBoundRatio decimal,
        outOfEZRatio decimal,
        intendedDirectionRatio decimal,
        meanHangTime decimal,
        maxHangTime decimal
    )
""")

create_table_kickers = ("""
    CREATE TABLE IF NOT EXISTS kickers(
        dummyIndex smallint,
        nflId integer PRIMARY KEY,
        height varchar(3),
        weight smallint,
        collegeName varchar(40),
        position varchar(3),
        displayName varchar(25),
        num_kickoffs smallint,
        num_field_goals smallint,
        meanKickoffDistance decimal,
        maxKickoffDistance decimal,
        meanKickoffHangtime decimal,
        maxKickoffHangtime decimal,
        intendedDirectionRatio decimal, 
        touchbackRatio decimal,
        OOBRatio decimal,
        onsideRatio decimal,
        onsideRecoveryRate decimal,
        meanKickLength_hit decimal,
        maxKickLength_hit decimal,
        clutchKicksMade smallint,
        meanKickLength_missed decimal,
        maxKickLength_missed decimal,
        shortestKickLength_missed decimal,
        clutchKicksMissed smallint
    )
""")

# insert records

games_insert = ("""
    INSERT INTO games (
        gameId,
        season,
        week,
        gameDate,
        homeTeamAbbr,
        visitorTeamAbbr )
    VALUES (%s, %s, %s, %s, %s, %s)
""")

players_insert = ("""
    INSERT INTO players (
        nflId,
        height,
        weight,
        collegeName,
        position,
        displayName)
    VALUES (%s, %s, %s, %s, %s, %s)
""")

plays_insert = ("""
    INSERT INTO players (
        gameId,
        playId,
        playDescription,
        quarter,
        down,
        yardsToGo,
        possessionTeam,
        specialTeamsPlayType,
        specialTeamsResult,
        kickerId,
        returnerId,
        kickBlockerId,
        yardlineSide,
        yadlineNumber,
        gameclock,
        penaltyCodes,
        penaltyJerseyNumbers,
        penaltyYards,
        preSnapHomeScore,
        preSnapVisitorScore,
        passResult,
        kickLength,
        kickReturnYardage,
        playResult,
        absoluteYardlineNumber)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

insert_pffScouting = ("""
    INSERT INTO pffScouting (
        gameId,
        playId,
        snapDetail,
        snapTime,
        operationTime,
        hangTime,
        kickType,
        kickDirectionIntended,
        kickDirectionActual,
        returnDirectionInteded,
        returnDirectionActual,
        missedTackler,
        assisstTackler,
        tackler,
        kickoffReturnFormation,
        gunners,
        puntRushers,
        specialTeamsSafeties,
        vises,
        kickContactType)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

insert_punters = ("""
    INSERT INTO punters (
        dummyIndex,
        nflId,
        height,
        weight,
        collegeName,
        position,
        displayName,
        num_punts,
        normalPuntRatio,
        caughtRatio,
        groundRatio,
        kickTeamTouchedFirstRatio,
        outOfBoundRatio,
        outOfEZRatio,
        intendedDirectionRatio,
        meanHangTime,
        maxHangTime)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

insert_kickers = ("""
    INSERT INTO kickers (
        dummyIndex,
        nflId,
        height,
        weight,
        collegeName,
        position,
        displayName,
        num_kickoffs,
        num_field_goals,
        meanKickoffDistance,
        maxKickoffDistance,
        meanKickoffHangtime,
        maxKickoffHangtime,
        intendedDirectionRatio, 
        touchbackRatio,
        OOBRatio,
        onsideRatio,
        onsideRecoveryRate,
        meanKickLength_hit,
        maxKickLength_hit,
        clutchKicksMadet,
        meanKickLength_missed,
        maxKickLength_missed,
        shortestKickLength_missed,
        clutchKicksMissed )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")