# nfl-big-data-bowl
Repository for general work on the [NFL Big Data Bowl 2022](https://www.kaggle.com/c/nfl-big-data-bowl-2022). The Big Data Bowl is a competition hosted by the NFL on kaggle where the NFL makes various data available for the public to use for analysis. 

### From the NFL:

*Your challenge is to generate actionable, practical, and novel insights from player tracking data that corresponds to special teams play. There are several potential topics for participants to analyze.*

*These include, but are not limited to:*

* *Create a new special teams metric. The winning algorithm from the 2020 Big Data Bowl has been adopted by the NFL/NFL Network for on air distribution, and we are hopeful that there could be a new stat for special teams plays that could come from this year’s competition*
* *Quantify special teams strategy. Special teams’ coaches are among the most creative and innovative in the league. Compare/contrast how each team game plans. Which strategies yield the best results? What are other strategies that could be adopted?*
* *Rank special teams players. Each team employs a variety of players (including longsnappers, kickers, punters, and other utility special teams players). How do they stack up with respect to one another?*

*The above list is not comprehensive, nor is it meant to be a guide for participants to cover. We are open to all special teams related ideas in this year’s competition.*

I did not do that.

This repository contains a quasi-ETL pipeline. I wanted to add a bunch of statistics to the punters and kickers data for readily available analysis, and then upload these into a database with the other data. At the moment this 'project' is fairly disjointed. The result is not a standard practices Data Warehouse by any stretch, though if I can find the time I will hopefully be able to implement something of that nature. At the moment it is something akin to a snowflake schema DW. The main purpose of this was to play around with PostgreSQL and Psycopg2, data manipulations with python, etc., using some data I'm familiar with from personal interest in the NFL.

# Data
### games.csv, players.csv, plays.csv 
These three are straightforward and come directly from the NFL.

Each game has a gameId that uniquely identifies it; each player has a nflId that uniquely identifies them. Plays are uniquely identified by the combination gameId & playId; playId's are not unique across games.

### PFFScouting.csv
Another dataset of plays identified the same way as plays.csv. Contains different information from [Pro Football Focus](https://www.pff.com/).

### kickers.csv, punters.csv
Datasets generated by kickers-transform.py and punters-tranform.py, respectively. Each player here is uniquely identified by his nflId (there is currently a dummy index that I intend to get rid of next time I update the code - this is a result of pandas' to_csv() function).

# Files
### kickers-transform.py & punters-transform.py

Data transformation pipelines. Takes in all the other data and performs calculations and manipulations. Spits out kickers.csv, punters.csv.

### sql_queries.py
Stores SQL queries to create and drop tables and insert data as strings.
(See notes at the bottom for datatype issues)

### create_tables.py
Builds the database from scratch. In it's current version, this will delete the existing nfl database and build a new empty one.
It connects to the database by retrieving db credentials from a config.ini file using the config() function.

### config.py
Contains the config() function, which uses a ConfigParser instance to retrieve the relevant connections to the database. Returns them in a dictionary which is unpacked as **kwargs.

### load.py
Loads data from csv files into the database.
(See note 2).

### datafix.py
Quick fix that needs to be more properly implemented; I used this when trying to solve the null issue (note 2) to replace 'NULL' or 'NA' (strings) with numpy NaN objects.

# Notes
1. Data types: Because of how pandas handles the data, many elements that could be stored as integers (returnerID's, kickBlockerId's in the plays data) or as smallint (num_punts, num_kickoffs) were turned into decimals and then stored as plaintext in the csv's.

2. Load functions' speed: Each table has it's own function that iterates each line and loads it into the db using a prewritten query - however, they also iterate through each item in the row and change the empty strings to None type so that they can be uploaded as NULL's. This would pose a huge speed problem for bigger datasets (like the gb-sized player movement-tracking datasets provided by the NFL I didn't include here)

3. At the moment the data pipeline goes from csv -> pandas dataframe -> csv -> database. I know there are better ways to do this that require some playing around. This is my first time implementing an ETL pipeline from scratch in python, rather than using a tool like Talend.

