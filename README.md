# MLB Daily Projections
Using Machine Learning, Regression Analysis, Sabermetrics, and the Love of the Game to predict daily projections for MLB players

# Instructions

# Software Requirements
	- Python: 2.7
	- Run pip install -r requirements.txt
	- Download MySQL Workbench
	- A Python IDE (PyCharm is bae :))

# Set Up Database
	- Open MySQL Workbench, click File, New Query Tab
	- Open sql queries from SQL Database folder
	- Run SQL Queries in this order:
		1. Run baseball_routines.sql
		2. Run baseball_dates.sql
		3. Run baseball_batters.sql
		4. Run baseball_pitchers.sql
		5. Run baseball_leaguebaverages.sql
		6. Run baseball_leaguepaverages.sql
		7. Run baseball_parkFactors.sql
		8. Run baseball_people.sql
		9. Run baseball_zipsbatters.sql
		10. Run baseball_zipspitchers.sql
		11. Run baseball_zipsbatterplatoon.sql
		12. Run baseball_zipspitcherplatoon.sql
		13. Run baseball_teammap.sql
		14. Run baseball_games.sql
		15. Run baseball_teams.sql
		16. Run baseball_battersdaily.sql
		17. Run baseball_pitchersdaily.sql

# Configure Database User and Password (optional)
	- Default user is root
	- No password
	- Default host is localhost

# Import Static Data into Tables
	- All Static Data to be loaded into the SQL Database is located in Database Data
	- If importing data for the first time:
		○ Importing Batters League Averages
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called 'leaguebattingtotals.csv'
			§ Select 'use existing table' and select baseball.leaguebaverages as the table
			§ Click next
			§ Click next and import the data
		○ Importing Pitchers League Averages
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called 'leaguepitchingtotals.csv'
			§ Select 'use existing table' and select baseball.leaguepaverages as the table
			§ Click next
			§ Click next and import the data
		○ Importing ZiPS Pitcher Platoon Projections
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called '2017 ZiPS Projections - Platoon Splits Pitchers.csv'
			§ Select 'use existing table' and select baseball.zipspitcherplatoon as the table
			§ Click next
			§ Click next and import the data
		○ Importing ZiPS Batters Platoon Projections
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called '2017 ZiPS Projections - Platoon Splits Batters.csv'
			§ Select 'use existing table' and select baseball.zipsbatterplatoon as the table
			§ Click next
			§ Click next and import the data
		○ Importing ZiPS Batters Projections
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called '2017 ZiPS Projections - Batters.csv'
			§ Select 'use existing table' and select baseball.zipsbatters as the table
			§ Click next
			§ Click next and import the data
		○ Importing ZiPS Pitcher Projections
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called '2017 ZiPS Projections - Pitchers.csv'
			§ Select 'use existing table' and select baseball.zipspitchers as the table
			§ Click next
			§ Click next and import the data
		○ Importing Teams
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called 'teammap.csv'
			§ Select 'use existing table' and select baseball.teammap as the table
			§ Click next
			§ Click next and import the data
		○ Importing Player Data
			§ Warning: takes awhile
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called 'peopleMaster.csv'
			§ Select 'use existing table' and select baseball.people as the table
			§ Click next
			§ Click next and import the data
	- If importing data after the first time
		○ Note: Update tables below that need to be updated every Monday (weekly). This ensures that you are not missing any players in your projections and league averages are updated. In order to get the data to update the tables with, you must pull from the repository every Monday to get the updated tables
			§ Note: peopleMaster will most likely be updated more often than weekly (think daily or every other day) due to errors importing rotowire and rotogrinders data and player's IDs cooresponding to those websites not being present in the database
		○ Importing Batters League Averages
			§ Run resetLeagueBAverages.sql
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called 'leaguebattingtotals.csv'
			§ Select 'use existing table' and select baseball.leaguebaverages as the table
			§ Click next
			§ Click next and import the data
		○ Importing Pitchers League Averages
			§ Run resetLeaguePAverages.sql
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called 'leaguepitchingtotals.csv'
			§ Select 'use existing table' and select baseball.leaguepaverages as the table
			§ Click next
			§ Click next and import the data
		○ Importing Player Data
			§ Run resetPeople.sql
			§ Warning: takes awhile
			§ Right click on tables and select 'Table Import Wizard'
			§ Browse for file in Database Data called 'peopleMaster.csv'
			§ Select 'use existing table' and select baseball.people as the table
			§ Click next
			§ Click next and import the data

# Process of Optimizing Lineups
	- Initialize constants in constants.py
		○ Set yearP, monthP, and dayP to the date you are projecting (most likely the current date)
		○ Set database information to the database information you set up
		○ Set gdStartYear, gdStartMonth, gdStartDay to the day you want the gradient descent algorithm to start gathering data
			§ Most likely the day before the projection day
		○ Set numdaysGradientDescent to the amount of days you want to go back to collect data for Gradient Descent optimization
			§ The farthest day you can go back is the first day you run projections.py
	- Run fangraphs.py - Updates Statistics
		○ Can run as many times as want
	- Run odds.py - Gets odds + games for the day
		○ Run before games start
		○ Money Lines cannot be null in feed
		○ Important: RUN ONLY ONCE
			§ Advanced: If mess up, delete records from the game table which coorespond to the wrong gameID
	- Run lineups.py - Gets lineups for the day
		○ Run around 5:30 PM
		○ Can run as many times as you want
	- Run projections.py - creates projections for batters based on pitcher + batter matchups + splits
		○ Can run as many times as want
	- Run gradientDescent.py - Projects DraftKings points
		○ Can run as many times as want
	- Run optimizer.py
		○ Update teams playing according to the competition entered
		○ With initial run, run the function that normalizes percentage owned and calculates and normalizes contR, then do not run!
			§ Function Name: percentageOwnedandVarianceNormalization
			§ Do not run by commenting out the function in python (with the # operator)
		○ Keep running optimizer till the point difference is equal to the point threshold by testing different number of lineups creation
			§ Guess a little bit higher or lower than the projected number of lineups
			§ Must adjust the numLineups paramater in the optimzer code
		○ Pick lineups with highest and lowest contrariance
	- Run generaldata.py - gets data from day before to train model
		○ Run AFTER all the games are over
		○ Run with the "update" variable

# Process of Pulling Data for Algorithms
	- Run generaldata.py
		○ Insert data into battersdaily and pitchersdaily for gradient descent data
		○ Specify yearP, monthP, dayP in constants
			§ Can be any date in baseball calendar where games were played on a day
				□ Ideally, start at opening day and keep making way to current day
		○ Run generaldata.py with insert parameter if not have run the optimizer on that date
		○ Run fangraphs.py
