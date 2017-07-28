import mlbgame
import mysql.connector
from datetime import datetime, date
import math

def alterBatter(batterID, gameID, cursor):
    # daily batter data
    for id in batterID:
        # get batterID
        batQuery = "SELECT idbatters, team, lastOpp FROM batters WHERE mlbID = %s"
        queryData = (id,)
        cursor.execute(batQuery, queryData)

        bat = mlbgame.batter_stats(year, month, day, id)

        # calculate dk points

        # insert into database
        for idbatter in cursor:
            addBatterPerformance = "UPDATE battersdaily SET ab = %s, hits = %s, singles = %s, doubles = %s, triples = %s, homeruns = %s, average = %s, stolenbases = %s, caughtstealing = %s, runs = %s, rbi = %s, walks = %s, errors = %s, hbp = %s, strikeouts = %s WHERE batterID = %s AND bgameID = %s"
            batterPerformanceData = (
                bat['ab'], bat['h'], bat['single'], bat['double'], bat['triple'], bat['hr'], bat['avg'], bat['sb'],
                bat['cs'],
                bat['r'], bat['rbi'], bat['bb'], bat['err'], bat['hbp'], bat['so'], int(idbatter[0]), gameID)
            cursor.execute(addBatterPerformance, batterPerformanceData)
            if cursor.rowcount == 0:
                addBatterPerformance = "INSERT INTO battersdaily (batterID, bgameID, ab, hits, singles, doubles, triples, homeruns, average, stolenbases, caughtstealing, runs, rbi, walks, errors, hbp, strikeouts, team, oppTeam) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                batterPerformanceData = (int(idbatter[0]), gameID, bat['ab'], bat['h'], bat['single'], bat['double'], bat['triple'], bat['hr'], bat['avg'], bat['sb'], bat['cs'], bat['r'], bat['rbi'], bat['bb'], bat['err'], bat['hbp'], bat['so'], idbatter[1], idbatter[2])
                cursor.execute(addBatterPerformance, batterPerformanceData)

def alterPitcher(winningPitchers, losingPitchers, pitcherID, gameID, cursor):
    # daily pitcher data
    for id in pitcherID:
        # get pitcherID
        pitcherQuery = "SELECT idpitchers, team, lastOpp FROM pitchers WHERE mlbID = %s"
        queryData = (id,)
        cursor.execute(pitcherQuery, queryData)

        #retrieve + analyze performance
        pitcher = mlbgame.pitcher_stats(year, month, day, id)

        win = 0
        if id in winningPitchers:
            win = 1
        elif id in losingPitchers:
            win = 0
        else:
            win = 0

        cg = 0
        shutout = 0
        nohit = 0
        if (win == 1 and pitcher['ip'] == '9'):
            cg = 1
        elif (win == 1 and pitcher['ip'] == '9' and pitcher['r'] == '0'):
            cg = 1
            shutout = 1
        elif (win == 1 and pitcher['ip'] == '9' and pitcher['r'] == '0' and pitcher['h'] == '0'):
            cg = 1
            shutout = 1
            nohit = 1

        era = pitcher['era']
        whip = pitcher['whip']
        if (pitcher['era'] == '-' or pitcher['whip'] == '-.--'):
            era = 0
            whip = 0

        # calculate dk points

        # insert into database
        for idpitcher in cursor:
            addPitcherPerformance = "UPDATE pitchersdaily SET walks = %s, earnedRuns = %s, era = %s, hits = %s, hbp = %s, homerunsAllowed = %s, ip = %s, strikeouts = %s, numberPitches = %s, runs = %s, strikes = %s, win = %s, shutout = %s, completegame = %s, nohitter = %s, save = %s, whip = %s WHERE pitcherID = %s AND pgameID = %s"
            pitcherPerformance = (
                pitcher['bb'], pitcher['er'], era, pitcher['h'], pitcher['hbp'], pitcher['hra'], pitcher['ip'],
                pitcher['k'],
                pitcher['np'], pitcher['r'], pitcher['s'], win, cg, shutout, nohit, pitcher['sv'], whip,
                int(idpitcher[0]), gameID)
            cursor.execute(addPitcherPerformance, pitcherPerformance)
            if cursor.rowcount == 0:
                addPitcherPerformance = "INSERT INTO pitchersdaily (pitcherID, pgameID, walks, earnedRuns, era, hits, hbp, homerunsAllowed, ip, strikeouts, numberPitches, runs, strikes, win, shutout, completegame, nohitter, save, whip, team, oppTeam) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                pitcherPerformance = (
                int(idpitcher[0]), gameID, pitcher['bb'], pitcher['er'], era, pitcher['h'], pitcher['hbp'],
                pitcher['hra'], pitcher['ip'], pitcher['k'], pitcher['np'], pitcher['r'], pitcher['s'], win, cg,
                shutout, nohit, pitcher['sv'], whip, idpitcher[1], idpitcher[2])
                cursor.execute(addPitcherPerformance, pitcherPerformance)

def getDate(day, month, year, cursor):
    findGame = 'SELECT iddates FROM dates WHERE date = %s'
    findGameData = (date(year, month, day),)
    cursor.execute(findGame, findGameData)

    dateID = -1
    for datez in cursor:
        dateID = datez[0]

    return dateID

def getGeneralData(day, month, year, mode):
    # database connection
    cnx = mysql.connector.connect(user='root',
                                  host='127.0.0.1',
                                  database='baseball')
    cursor = cnx.cursor()

    # get games
    year = year
    month = month
    day = day

    gameID = -1

    # insert if haven't added to games table yet, update otherwise
    if mode == "insert":
        # Insert Into Dates Table

        addGame = "INSERT INTO dates (date) VALUES(%s)"
        gameData = (date(year, month, day),)

        cursor.execute(addGame, gameData)
        gameID = cursor.lastrowid
    elif mode == "update":
        # Find Game ID
        findGame = "SELECT iddates FROM dates WHERE date = %s"
        findGameData = (date(year, month, day),)
        cursor.execute(findGame, findGameData)

        for game in cursor:
            gameID = game[0]

    gamez = mlbgame.games(year,month,day)

    # get stats associated with each game
    # insert into players table
    batterID = []
    pitcherID = []
    winningPitchers = []
    losingPitchers = []
    for games in gamez:
        for game in games:
            if game.game_status != 'OTHER':
                stats = mlbgame.player_stats(game.game_id)
                for batter in stats['away_batting']:
                    try:
                        # insert into batters table, update if not there
                        addBatter = "INSERT INTO batters (mlbID, playerName, team, lastOpp) VALUES(%s, %s, %s, %s)"
                        batterData = (batter.id, batter.name_display_first_last, game.away_team, game.home_team)
                        cursor.execute(addBatter,batterData)
                    except:
                        updateBatter = "UPDATE batters SET playerName = %s, team = %s, lastOpp = %s WHERE mlbID = %s"
                        batterData = (batter.name_display_first_last, game.away_team, game.home_team, batter.id)
                        cursor.execute(updateBatter, batterData)
                    batterID.append(batter.id)
                for batter in stats['home_batting']:
                    try:
                        # insert into batters table, update if not there
                        addBatter = "INSERT INTO batters (mlbID, playerName, team, lastOpp) VALUES(%s, %s, %s, %s)"
                        batterData = (batter.id, batter.name_display_first_last, game.home_team, game.away_team)
                        cursor.execute(addBatter,batterData)
                    except:
                        updateBatter = "UPDATE batters SET playerName = %s, team = %s, lastOpp = %s WHERE mlbID = %s"
                        batterData = (batter.name_display_first_last, game.home_team, game.away_team, batter.id)
                        cursor.execute(updateBatter, batterData)
                    batterID.append(batter.id)
                for pitcher in stats['away_pitching']:
                    try:
                        # insert into batters table, update if not there
                        addPitcher = "INSERT INTO pitchers (mlbID, playerName, pos, team, lastOpp) VALUES(%s, %s, %s, %s, %s)"
                        pitcherData = (pitcher.id, pitcher.name_display_first_last, "P", game.away_team, game.home_team)
                        cursor.execute(addPitcher,pitcherData)
                    except:
                        updatePitcher = "UPDATE pitchers SET playerName = %s, team = %s, lastOpp = %s WHERE mlbID = %s"
                        pitcherData = (pitcher.name_display_first_last, game.away_team, game.home_team, pitcher.id)
                        cursor.execute(updatePitcher, pitcherData)
                    pitcherID.append(pitcher.id)
                    if hasattr(pitcher, 'win'):
                        winningPitchers.append(pitcher.id)
                    if hasattr(pitcher, 'loss'):
                        losingPitchers.append(pitcher.id)
                for pitcher in stats['home_pitching']:
                    try:
                        # insert into batters table, update if not there
                        addPitcher = "INSERT INTO pitchers (mlbID, playerName, pos, team, lastOpp) VALUES(%s, %s, %s, %s, %s)"
                        pitcherData = (pitcher.id, pitcher.name_display_first_last, "P", game.home_team, game.away_team)
                        cursor.execute(addPitcher, pitcherData)
                    except:
                        updatePitcher = "UPDATE pitchers SET playerName = %s, team = %s, lastOpp = %s WHERE mlbID = %s"
                        pitcherData = (pitcher.name_display_first_last, game.home_team, game.away_team, pitcher.id)
                        cursor.execute(updatePitcher, pitcherData)
                    pitcherID.append(pitcher.id)
                    if hasattr(pitcher, 'win'):
                        winningPitchers.append(pitcher.id)
                    if hasattr(pitcher, 'loss'):
                        losingPitchers.append(pitcher.id)

    alterBatter(batterID, gameID, cursor)

    alterPitcher(winningPitchers, losingPitchers, pitcherID, gameID, cursor)

    # close + save
    cursor.close()
    cnx.commit()
    cnx.close()

    print "Updated Baseball Database for Games on %s/%s/%s" % (month, day, year)

def updateDKPointsBatters(day, month, year):
    # database connection
    cnx = mysql.connector.connect(user='root',
                                  host='127.0.0.1',
                                  database='baseball')
    cursor = cnx.cursor()

    gameID = getDate(day, month, year, cursor)
    # batters
    dkQuery = "SELECT * from battersdaily WHERE bgameID = %s"
    bGameIDData = (gameID,)
    cursor.execute(dkQuery, bGameIDData)

    data = cursor.fetchall()

    for batters in data:
        pointTotal = (batters[3])*3 + (batters[4])*5 + (batters[5])*8 + (batters[6]*10) + (batters[11])*2 + (batters[10])*2 + (batters[12])*2 + (batters[14])*2 + (batters[8])*5
        updateBat = "UPDATE battersdaily SET dkpoints = %s WHERE id = %s"
        updateBatData = (pointTotal, batters[0])
        cursor.execute(updateBat, updateBatData)

    cursor.close()
    cnx.commit()
    cnx.close()

    print "Updated Batters DK Points"

def updateDKPointsPitchers(day, month, year):
    cnx = mysql.connector.connect(user='root',
                                  host='127.0.0.1',
                                  database='baseball')
    cursor = cnx.cursor()

    gameID = getDate(day, month, year, cursor)
    # batters
    dkQuery = "SELECT * from pitchersdaily WHERE pgameID = %s AND pitcherID != 0"
    pGameIDData = (gameID,)
    cursor.execute(dkQuery, pGameIDData)

    data = cursor.fetchall()

    for pitchers in data:
        ip = float((pitchers[9]) % 1)
        tol = 1e-9
        pointsTotal = 0
        if abs(ip-.1) <= max(tol * max(abs(ip), abs(.1)), tol):
            pointsTotal = pointsTotal + .75
        if abs(ip-.2) <= max(tol * max(abs(ip), abs(.2)), tol):
            pointsTotal = pointsTotal + 1.5

        pointsTotal = pointsTotal + (float(math.floor(pitchers[9])))*2.25 + (float(pitchers[10])*2) + (float(pitchers[14])*4) + \
                      (float(pitchers[15])*2.5) + (float(pitchers[16])*2.5) + (float(pitchers[17])*5) - (float(pitchers[4])*2) - \
                      (float(pitchers[6])*.6) - (float(pitchers[3])*.6) - (float(pitchers[7])*.6)

        updatePitcherQuery = "UPDATE pitchersdaily SET dkpoints = %s WHERE idpitchersdaily = %s"
        updatePitcherData = (pointsTotal, pitchers[0])
        cursor.execute(updatePitcherQuery, updatePitcherData)

    cursor.close()
    cnx.commit()
    cnx.close()

    print "Updated Pitchers DK Points"

if __name__ == "__main__":
    year = 2017
    month = 7
    day = 27
    getGeneralData(day, month, year, "update")
    updateDKPointsBatters(day, month, year)
    updateDKPointsPitchers(day, month, year)