from datetime import date
import mysql.connector
from pydfs_lineup_optimizer import *
from decimal import *
import numpy as np

def getDate(day, month, year, cursor):
    findGame = 'SELECT iddates FROM dates WHERE date = %s'
    findGameData = (date(year, month, day),)
    cursor.execute(findGame, findGameData)

    dateID = -1
    for datez in cursor:
        dateID = datez[0]

    return dateID

def percentageOwnedandVarianceNormalization(day, month, year, cursor):
    # do only once
    gameID = getDate(day, month, year, cursor)

    # pitchers
    getPitchers = 'SELECT dkPointsPred, pOWN, pitcherID, variance FROM pitchersdaily WHERE pgameID = %s AND dkPointsPred IS NOT NULL AND dkSalary IS NOT NULL'
    getPitchersD = (gameID,)
    cursor.execute(getPitchers, getPitchersD)

    pitchers = cursor.fetchall()
    contRPitchers = []
    variancePitchers = []

    for pitch in pitchers:
        pOWN = .001
        if pitch[1] is not None:
            pOWN = pitch[1]

        contR = float(pitch[0])/pOWN
        contRPitchers.append(contR)
        variancePitchers.append(pitch[3])

    contRPMean = np.mean(contRPitchers)
    contRPSTD = np.std(contRPitchers)

    variancePMean = np.mean(variancePitchers)
    variancePSTD = np.std(variancePitchers)

    j = 0
    for pitch in pitchers:
        trueContR = ((contRPitchers[j] - contRPMean)/contRPSTD)
        trueVariance = ((variancePitchers[j] - variancePMean)/variancePSTD)

        setContR = 'UPDATE pitchersdaily SET contR = %s, variance = %s WHERE pgameID = %s and pitcherID = %s'
        setContRD = (float(trueContR), float(trueVariance), gameID, pitch[2])
        cursor.execute(setContR, setContRD)

        j = j + 1

    #batters
    getBatters = 'SELECT dkPointsPred, pOWN, batterID, variance FROM battersdaily WHERE bgameID = %s AND dkPointsPred IS NOT NULL AND dkSalary IS NOT NULL'
    getBattersD = (gameID,)
    cursor.execute(getBatters, getBattersD)

    batters = cursor.fetchall()

    contRBatters = []
    varianceBatters = []

    for bat in batters:
        pOWN = .001
        if bat[1] is not None:
            pOWN = bat[1]

        contR = float(bat[0])/pOWN
        contRBatters.append(contR)
        varianceBatters.append(bat[3])

    contRBMean = np.mean(contRBatters)
    contRBSTD = np.std(contRBatters)

    varianceBMean = np.mean(varianceBatters)
    varianceBSTD = np.mean(varianceBatters)

    i = 0
    for bat in batters:
        trueContR = ((contRBatters[i] - contRBMean)/contRBSTD)
        trueVariance = ((varianceBatters[i] - varianceBMean)/varianceBSTD)

        setContR = 'UPDATE battersdaily SET contR = %s, variance = %s WHERE bgameID = %s and batterID = %s'
        setContRD = (float(trueContR), float(trueVariance), gameID, bat[2])
        cursor.execute(setContR, setContRD)

        i = i + 1

    print ("Updated Contrarian Rating and Variance for Batters and Pitchers")

def optimize(day, month, year, cursor):

    gameID = getDate(day, month, year, cursor)

    # teams
    DIAMONDBACKS = 'Diamondbacks'
    BRAVES = 'Braves'
    ORIOLES = 'Orioles'
    REDSOX = 'Red Sox'
    CUBS = 'Cubs'
    WHITESOX = 'White Sox'
    REDS = 'Reds'
    INDIANS = 'Indians'
    ROCKIES = 'Rockies'
    TIGERS = 'Tigers'
    ASTROS = 'Astros'
    ROYALS = 'Royals'
    ANGELS = 'Angels'
    DODGERS = 'Dodgers'
    MARLINS = 'Marlins'
    BREWERS = 'Brewers'
    TWINS = 'Twins'
    METS = 'Mets'
    YANKEES = 'Yankees'
    ATHLETICS = 'Athletics'
    PHILLIES = 'Phillies'
    PIRATES = 'Pirates'
    PADRES = 'Padres'
    MARINERS = 'Mariners'
    GIANTS = 'Giants'
    CARDINALS = 'Cardinals'
    RAYS = 'Rays'
    RANGERS = 'Rangers'
    BLUEJAYS = 'Blue Jays'
    NATIONALS = 'Nationals'

    # teams constraints
    teamsBConstraint = '('
    teamsPConstraint = '('
    teamsPlaying = [RAYS, YANKEES, REDS, MARLINS, DIAMONDBACKS, CARDINALS, CUBS, WHITESOX, METS, PADRES]

    for team in teamsPlaying:
        stringConstraint = 'battersdaily.team = ' + "'" + team + "'" + ' '
        if teamsPlaying[-1] != team:
            stringConstraint = stringConstraint + 'OR '
        teamsBConstraint = teamsBConstraint + stringConstraint

    teamsBConstraint = teamsBConstraint + ')'

    for team in teamsPlaying:
        stringConstraint = 'pitchersdaily.team = ' + "'" + team + "'" + ' '
        if teamsPlaying[-1] != team:
            stringConstraint = stringConstraint + 'OR '
        teamsPConstraint = teamsPConstraint + stringConstraint

    teamsPConstraint = teamsPConstraint + ')'

    # other batter constraints
    batterConstraints = ['paL', 'paR']
    batterConstraintsValues = {}
    batterConstraintsTypes ={}

    for con in batterConstraints:
        var1 = raw_input("Enter operand for constraint " + con + ": ")
        batterConstraintsTypes[con] = var1
        var0 = raw_input("Enter value for constraint " + con + ": ")
        batterConstraintsValues[con] = var0


    constraintsString = "("
    for constraint in batterConstraints:
        constraintString = constraint + " " + batterConstraintsTypes[constraint] + " " + batterConstraintsValues[constraint]
        if batterConstraints[-1] != constraint:
            constraintString = constraintString + ' AND '
        constraintsString = constraintsString + constraintString

    constraintsString = constraintsString + ")"

    # get players
    playas = []

    getBPlayersQuery = "SELECT playerName, mlbID, pos, pos1, battersdaily.team, dkPointsPred, dkSalary, variance, contR, dkpoints FROM battersdaily LEFT JOIN batters ON battersdaily.batterID = batters.idbatters WHERE battersdaily.bgameID = %s AND pos != 'P' AND dkSalary IS NOT NULL AND "
    getBPlayersQuery = getBPlayersQuery + constraintsString
    getBPlayersQuery = getBPlayersQuery + " AND "
    getBPlayersQuery = getBPlayersQuery + teamsBConstraint
    getBPlayersData = (gameID,)
    print ("Batter Query: " + getBPlayersQuery)
    cursor.execute(getBPlayersQuery, getBPlayersData)

    numBatters = float(cursor.rowcount)
    print ("Number of batters being considered: " + str(cursor.rowcount))
    batters = cursor.fetchall()
    varianceDict = {}
    contRDict = {}
    dkPointsDict = {}
    highestPoints = 0
    lowestPoints = 1000000000

    # construct batters
    for bat in batters:
        varianceDict[bat[1]] = bat[7]
        contRDict[bat[1]] = bat[8]
        dkPointsDict[bat[1]] = float(bat[9])
        if bat[5] > highestPoints:
            highestPoints = bat[5]
        if bat[5] < lowestPoints:
            lowestPoints = bat[5]

        positions = []
        positions.append(str(bat[2]))

        if bat[3] is not None:
            secretPositions = []
            secretPositions.append(str(bat[3]))
            newPlayerOne = Player(bat[1], bat[0], "", secretPositions, bat[4], int(bat[6]), float(bat[5]))
            playas.append(newPlayerOne)

        newPlaya = Player(bat[1], bat[0], "", positions, bat[4], int(bat[6]), float(bat[5]))
        playas.append(newPlaya)

    getPPlayersQuery = "SELECT playerName, mlbID, pos, pitchersdaily.team, dkPointsPred, dkSalary, variance, contR, dkpoints FROM baseball.pitchersdaily LEFT JOIN baseball.pitchers ON pitchersdaily.pitcherID = pitchers.idpitchers WHERE pitchersdaily.pgameID = %s AND dkSalary IS NOT NULL AND dkPointsPred IS NOT NULL AND "
    getPPlayersQuery = getPPlayersQuery + teamsPConstraint
    getPPlayersData = (gameID,)
    print ("Pitcher Query: " + getPPlayersQuery)
    cursor.execute(getPPlayersQuery, getPPlayersData)

    pitchers = cursor.fetchall()

    print ("Number of pitchers being considered: " + str(cursor.rowcount))

    for pitch in pitchers:
        positions = []
        positions.append(pitch[2])

        varianceDict[pitch[1]] = pitch[6]
        contRDict[pitch[1]] = pitch[7]
        dkPointsDict[pitch[1]] = float(pitch[8])

        newPlaya = Player(pitch[1], pitch[0], "", positions, pitch[3], int(pitch[5]), float(pitch[4]))
        playas.append(newPlaya)

    #instantiate optimizer + run

    optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASEBALL)
    optimizer.load_players(playas)

    # if duplicate player, increase n + generate next lineup,
    # next lineup will generate lineup with next highest amount of points
    numLineups = 9
    battersInOptimizer = 8
    pointThreshold = (float((highestPoints - lowestPoints))/numBatters)*battersInOptimizer
    lineups = optimizer.optimize(n=numLineups)

    highestVariance = -1000000000
    highestVarianceLineup = -1
    lowestVariance = 10000000000
    lowestVarianceLineup = -1

    highestContR = -1000000000
    highestContRLineup = -1
    lowestContR = 10000000000
    lowestContRLineup = -1

    highestContraiance = -1000000000
    highestContraianceLineup = -1
    lowestContraiance = 10000000000
    lowestContraianceLineup = -1

    highestPoints = -1000000000
    lowestPoints = 1000000000

    lineupCounter = 1
    for lineup in lineups:
        variance = 0
        contR = 0
        dkpoints = 0
        playerIDList = []
        for player in lineup.lineup:
            playerIDList.append(player.id)
        print ("Lineup #: " + str(lineupCounter))
        print(lineup)
        for player in playerIDList:
            variance = variance + varianceDict[player]
            contR = contR + contRDict[player]
            dkpoints = dkpoints + dkPointsDict[player]
        contrainance = (.6)*variance + (.4)*contR
        if variance > highestVariance:
            highestVariance = variance
            highestVarianceLineup = lineupCounter
        if variance < lowestVariance:
            lowestVariance = variance
            lowestVarianceLineup = lineupCounter
        if contR > highestContR:
            highestContR = contR
            highestContRLineup = lineupCounter
        if contR < lowestContR:
            lowestContR = contR
            lowestContRLineup = lineupCounter
        if contrainance > highestContraiance:
            highestContraiance = contrainance
            highestContraianceLineup = lineupCounter
        if contrainance < lowestContraiance:
            lowestContraiance = contrainance
            lowestContraianceLineup = lineupCounter
        if lineup.fantasy_points_projection > highestPoints:
            highestPoints = lineup.fantasy_points_projection
        if lineup.fantasy_points_projection < lowestPoints:
            lowestPoints = lineup.fantasy_points_projection
        print "Variance of Players in Lineup: " + str(variance)
        print "Contrarian Rating of Players in Lineup: " + str(contR)
        print "DK Points Scored for Lineup: " + str(dkpoints)
        lineupCounter = lineupCounter + 1
        print ("\n")

    print ("Optimizer Summary: ")
    pointDifference = highestPoints - lowestPoints
    print("Point threshold for competition is: " + str(pointThreshold))
    print("Point difference for current lineups is: " + str(pointDifference))

    optimalLineupNumber = (numLineups/(pointDifference))*pointThreshold

    print("Optimal number of lineups needed to be made are: " + str(optimalLineupNumber))
    print ("\n")

    print "Highest Variance Lineup Number for GPPs: " + str(highestVarianceLineup)
    print "Variance of Players in GPP Lineup: " + str(highestVariance)

    print "Lowest Variance Lineup Number for 50/50s: " + str(lowestVarianceLineup)
    print "Variance of Players in GPP Lineup: " + str(lowestVariance)
    print ("\n")

    print "Highest Contrarian Rating Lineup Number for GPPs: " + str(highestContRLineup)
    print "Contrarian Rating for Players in Highest Contrarian Lineup " + str(highestContR)

    print "Lowest Contrarian Rating for Lineup Number for 50/50s: " + str(lowestContRLineup)
    print "Contrarian Rating for Players in Lowest Contrarian Lineup " + str(lowestContR)
    print ("\n")

    print "Highest Contraiance Lineup Number (Contrarian Rating + Variance) for GPPs: " + str(highestContraianceLineup)
    print "Contraiance Rating: " + str(highestContraiance)

    print "Lowest Contraiance Lineup Number (Contrarian Rating + Variance) for 50/50s: " + str(lowestContraianceLineup)
    print "Contraiance Rating: " + str(lowestContraiance)

if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root',
                                  host='127.0.0.1',
                                  database='baseball')
    cursor = cnx.cursor(buffered=True)

    year = 2017
    month = 7
    day = 28

    percentageOwnedandVarianceNormalization(day, month, year, cursor)
    optimize(day, month, year, cursor)

    cursor.close()
    cnx.commit()
    cnx.close()
