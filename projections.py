from bs4 import BeautifulSoup
from datetime import date
import mysql.connector
import urllib2
import demjson
import numpy as np

def updateLeagueProjections(cursor):
    leagueProjUpdateQuery = "UPDATE leaguebaverages SET wOBA = ((0.693)*(BB - IBB) + (0.723)*HBP + (0.876)*(H - (2B + 3B + HR)) + (1.231)*2B + (1.55)*3B + (1.977)*HR)/(AB + BB - IBB + SF + HBP), ISO = (SLG - BA), KP = SO/PA, BBP = BB/PA, BABIP = (H - HR)/(AB - SO - HR + SF)"
    cursor.execute(leagueProjUpdateQuery)

    print "Updated League Averages"

def getParkFactors(cursor):
    url = "http://www.baseballprospectus.com/sortable/index.php?cid=1819123"

    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    parksData = []
    for tr in soup.find_all('tr')[6:66]:
        tds = tr.find_all('td')

        parkData = {}

        team = tds[4].a.text
        parkData['Team'] = team

        hand = tds[5].text
        if hand == 'RHB':
            hand = 'R'
        if hand == 'LHB':
            hand = 'L'
        parkData['Side'] = hand

        homePA = tds[6].text
        parkData['HomePA'] = homePA

        awayPA = tds[7].text
        parkData['AwayPA'] = awayPA

        homeHR = tds[8].text
        parkData['HomeHR'] = homeHR

        awayHR = tds[9].text
        parkData['AwayHR'] = awayHR

        fbFactor = tds[10].text
        parkData['FBFactor'] = fbFactor

        gbFactor = tds[11].text
        parkData['GBFactor'] = gbFactor

        ldFactor = tds[12].text
        parkData['LDFactor'] = ldFactor

        puFactor = tds[13].text
        parkData['PUFactor'] = puFactor

        firstBaseFactor = tds[14].text
        parkData['1BFactor'] = firstBaseFactor

        secondBaseFactor = tds[15].text
        parkData['2BFactor'] = secondBaseFactor

        thirdBaseFactor = tds[16].text
        parkData['3BFactor'] = thirdBaseFactor

        hrFactor = tds[17].text
        parkData['HRFactor'] = hrFactor

        runsFactor = tds[18].text
        parkData['RunsFactor'] = runsFactor

        parkData['RunsFactorP'] = (float(runsFactor) - 100)/100

        parksData.append(parkData)

    deleteQuery = "DELETE FROM parkFactors"
    cursor.execute(deleteQuery)

    for park in parksData:
        parkQuery = "INSERT INTO parkFactors (Team, Side, HomePA, AwayPA, HomeHR, AwayHR, FBFactor, GBFactor, LDFactor, PUFactor, 1BFactor, 2BFactor, 3BFactor, HRFactor, RunsFactor, RunsFactorP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        parkData = (park['Team'], park['Side'], park['HomePA'], park['AwayPA'], park['HomeHR'], park['AwayHR'], park['FBFactor'],
                    park['GBFactor'], park['LDFactor'], park['PUFactor'], park['1BFactor'], park['2BFactor'], park['3BFactor'], park['HRFactor'], park['RunsFactor'],
                    park['RunsFactorP'])
        cursor.execute(parkQuery, parkData)

    print ("Updated Park Factors")

def getDate(day, month, year, cursor):
    findGame = 'SELECT iddates FROM dates WHERE date = %s'
    findGameData = (date(year, month, day),)
    cursor.execute(findGame, findGameData)

    dateID = -1
    for datez in cursor:
        dateID = datez[0]

    return dateID

def updateBatterProjections(day, month, year, cursor):

    gameID = getDate(day, month, year, cursor)

    getLeagueAverages = "SELECT wOBA, KP, BBP, ISO, BABIP, OBP, OPS, SLG FROM leaguebaverages WHERE Year = 2017"
    cursor.execute(getLeagueAverages)

    avgWOBA = 0
    avgKP = 0
    avgBBP = 0
    avgISO = 0
    avgBABIP = 0
    avgOBP = 0
    avgOPS = 0
    avgSLG = 0

    for avg in cursor:
        avgWOBA = avg[0]
        avgKP = avg[1]
        avgBBP = avg[2]
        avgISO = avg[3]
        avgBABIP = avg[4]
        avgOBP = avg[5]
        avgOPS = avg[6]
        avgSLG = avg[7]

    getAllBattersQ = "SELECT batterID FROM battersdaily WHERE bgameID = %s"
    getAllBattersD = (gameID,)
    cursor.execute(getAllBattersQ, getAllBattersD)

    allBatters = cursor.fetchall()

    for bat in allBatters:
        # get dkpoints + calculated variance
        getPerformanceQ = "SELECT dkpoints FROM battersdaily WHERE batterID = %s AND dkpoints IS NOT NULL AND bgameID != %s"
        getPerformanceD = (bat[0], gameID)
        cursor.execute(getPerformanceQ, getPerformanceD)

        varianceBat = 0

        dkpoints = []
        for dkpoint in cursor:
            dkpoints.append(dkpoint[0])

        # remove outliers
        if dkpoints:
            medianDKPoints = np.median(dkpoints)
            upperRange = (1.5)*medianDKPoints
            lowerRange = medianDKPoints - ((1.5)*medianDKPoints - medianDKPoints)

            updatedDKPoints = [i for i in dkpoints if (i <= upperRange)]
            if updatedDKPoints:
                varianceBat = np.std(updatedDKPoints)

        # get batter
        getEligBattersQ = "SELECT * FROM batters WHERE idbatters = %s"
        getEligBattersD = (bat[0],)
        cursor.execute(getEligBattersQ, getEligBattersD)

        for batter in cursor:
            trueBID = batter[0]
            bwOBAL = batter[3]
            bwOBAR = batter[4]
            bISOL = batter[5]
            bISOR = batter[6]
            bOBPL = batter[7]
            bOBPR = batter[8]
            bOPSL = batter[9]
            bOPSR = batter[10]
            bSLGL = batter[11]
            bSLGR = batter[12]
            bKPL = batter[13]
            bKPR = batter[14]
            bBABIPL = batter[15]
            bBABIPR = batter[16]
            bBBL = batter[19]
            bBBR = batter[20]
            bWOBA = batter[30]
            bISO = batter[31]
            bOBP = batter[32]
            bSLG = batter[33]
            bOPS = batter[34]
            bKP = batter[35]
            bBB = batter[36]
            bBABIP = batter[37]
            bwSB = batter[38]

            batterHand = batter[25]
            bmlbID = batter[1]


            queryPitcherID = "SELECT oppPitcher, team FROM battersdaily WHERE (batterID = %s AND bgameID = %s)"
            getPitcherIDData = (trueBID, gameID)
            cursor.execute(queryPitcherID, getPitcherIDData)

            pitcherTrueID = 0
            team = ""
            for id in cursor:
                pitcherTrueID = id[0]
                team = id[1]

            # get park factor
            bTeamToScheduleTeamQ = "SELECT FANGRAPHSABBR FROM teammap WHERE FANGRAPHSTEAM = %s"
            bTeamToScheduleTeamD = (team,)
            cursor.execute(bTeamToScheduleTeamQ, bTeamToScheduleTeamD)

            teamFGA = ""
            for team in cursor:
                teamFGA = team[0]

            # find out home team
            homeTeamQ = "SELECT home FROM games WHERE (home = %s OR away = %s) AND date = %s"
            homeTeamD = (teamFGA, teamFGA, gameID)
            cursor.execute(homeTeamQ, homeTeamD)

            homeFGA = ""
            for team in cursor:
                homeFGA = team[0]

            # get BP Abvreviation
            bpTeamQ = "SELECT BPTEAM FROM teammap WHERE FANGRAPHSABBR = %s"
            bpTeamD = (homeFGA,)
            cursor.execute(bpTeamQ, bpTeamD)

            bpHomeTeam = ""
            for team in cursor:
                bpHomeTeam = team[0]

            getPitcher = "SELECT * FROM pitchers WHERE idpitchers = %s"
            getPitcherData = (pitcherTrueID,)

            cursor.execute(getPitcher, getPitcherData)

            pitchers = cursor.fetchall()

            for pitcher in pitchers:
                pwOBAL = pitcher[3]
                pwOBAR = pitcher[4]
                pAVGL = pitcher[5]
                pAVGR = pitcher[6]
                pOBPL = pitcher[7]
                pOBPR = pitcher[8]
                pSLGL = pitcher[9]
                pSLGR = pitcher[10]
                pKPL = pitcher[11]
                pKPR = pitcher[12]
                pBBL = pitcher[13]
                pBBR = pitcher[14]
                pBABIPL = pitcher[17]
                pBABIPR = pitcher[18]
                ipL = pitcher[23]
                ipR = pitcher[24]
                pSBRate = pitcher[30]
                pISOL = pSLGL - pAVGL
                pISOR = pSLGR - pAVGR
                pOPSL = pOBPL + pSLGL
                pOPSR = pOBPR + pSLGR

                pitcherHand = pitcher[26]
                pmlbID = pitcher[1]

                # ExAvg = ((BAVG * PAVG) / LgAVG) / ((BAVG * PAVG) / LgAVG + ((1-BAVG)*(1-PAVG)/(1-LgAvg)))
                # B x P / (0.84 x B x P + 0.16)

                if ipL < 10 or ipR < 10:
                    getPitcherZipsQ = "SELECT BAL, OBPL, SLGL, OPSL, BAR, OBPR, SLGR, OPSR, BBPL, BBPR, KPL, KPR, ISOL, ISOR, WOBAL, WOBAR, BABIPL, BABIPR FROM zipspitcherplatoon WHERE mlbID = %s"
                    getPitcherZipsD = (pmlbID,)
                    cursor.execute(getPitcherZipsQ, getPitcherZipsD)

                    for zipPitcher in cursor:
                        pwOBAL = zipPitcher[14]
                        pwOBAR = zipPitcher[15]
                        pAVGL = zipPitcher[0]
                        pAVGR = zipPitcher[4]
                        pOBPL = zipPitcher[1]
                        pOBPR = zipPitcher[5]
                        pSLGL = zipPitcher[2]
                        pSLGR = zipPitcher[6]
                        pKPL = zipPitcher[10]
                        pKPR = zipPitcher[11]
                        pBBL = zipPitcher[8]
                        pBBR = zipPitcher[9]
                        pBABIPL = zipPitcher[16]
                        pBABIPR = zipPitcher[17]
                        pISOL = zipPitcher[12]
                        pISOR = zipPitcher[13]
                        pOPSL = zipPitcher[3]
                        pOPSR = zipPitcher[7]

                adjWOBA = 0
                adjKP = 0
                adjKSteve = 0
                adjBBP = 0
                adjBABIP = 0
                adjISO = 0
                adjOBP = 0
                adjOPS = 0
                adjSLG = 0
                parkFactor = 0

                sbRate = pSBRate*bwSB

                if batterHand == 'S':
                    if pitcherHand == 'L':
                        # right handed batter + use left p handed stats
                        adjWOBA = (((bwOBAL * pwOBAR) / avgWOBA) / (((bwOBAL * pwOBAR) / avgWOBA) + (((1-bwOBAL)*(1-pwOBAR))/(1-avgWOBA))))
                        adjKP = (((bKPL * pKPR) / avgKP) / (((bKPL * pKPR) / avgKP) + (((1-bKPL)*(1-pKPR))/(1-avgKP))))
                        adjBBP = (((bBBL * pBBR) / avgBBP) / (((bBBL * pBBR) / avgBBP) + (((1-bBBL)*(1-pBBR))/(1-avgBBP))))
                        adjBABIP = (((bBABIPL * pBABIPR) / avgBABIP) / (((bBABIPL * pBABIPR) / avgBABIP) + (((1-bBABIPL)*(1-pBABIPR))/(1-avgBABIP))))
                        adjISO = (((bISOL * pISOR) / avgISO) / (((bISOL * pISOR) / avgISO) + (((1-bISOL)*(1-pISOR))/(1-avgISO))))
                        adjOBP = (((bOBPL * pOBPR) / avgOBP) / (((bOBPL * pOBPR) / avgOBP) + (((1-bOBPL)*(1-pOBPR))/(1-avgOBP))))
                        adjOPS = (((bOPSL * pOPSR) / avgOPS) / (((bOPSL * pOPSR) / avgOPS) + (((1-bOPSL)*(1-pOPSR))/(1-avgOPS))))
                        adjSLG = (((bSLGL * pSLGR) / avgSLG) / (((bSLGL * pSLGR) / avgSLG) + (((1-bSLGL)*(1-pSLGR))/(1-avgSLG))))

                        # get park factor
                        parkFactorQ = "SELECT RunsFactorP FROM parkFactors WHERE Team = %s AND Side = %s"
                        parkFactorD = (bpHomeTeam, 'R')
                        cursor.execute(parkFactorQ, parkFactorD)

                        for park in cursor:
                            parkFactor = park[0]

                    if pitcherHand == 'R':
                        # left handed batter + use right p handed stats
                        adjWOBA = (((bwOBAR * pwOBAL) / avgWOBA) / (((bwOBAR * pwOBAL) / avgWOBA) + (((1-bwOBAR)*(1-pwOBAL))/(1-avgWOBA))))
                        adjKP = (((bKPR * pKPL) / avgKP) / (((bKPR * pKPL) / avgKP) + (((1-bKPR)*(1-pKPL))/(1-avgKP))))
                        adjBBP = (((bBBR * pBBL) / avgBBP) / (((bBBR * pBBL) / avgBBP) + (((1-bBBR)*(1-pBBL))/(1-avgBBP))))
                        adjBABIP = (((bBABIPR * pBABIPL) / avgBABIP) / (((bBABIPR * pBABIPL) / avgBABIP) + (((1-bBABIPR)*(1-pBABIPL))/(1-avgBABIP))))
                        adjISO = (((bISOR * pISOL) / avgISO) / (((bISOR * pISOL) / avgISO) + (((1-bISOR)*(1-pISOL))/(1-avgISO))))
                        adjOBP = (((bOBPR * pOBPL) / avgOBP) / (((bOBPR * pOBPL) / avgOBP) + (((1-bOBPR)*(1-pOBPL))/(1-avgOBP))))
                        adjOPS = (((bOPSR * pOPSL) / avgOPS) / (((bOPSR * pOPSL) / avgOPS) + (((1-bOPSR)*(1-pOPSL))/(1-avgOPS))))
                        adjSLG = (((bSLGR * pSLGL) / avgSLG) / (((bSLGR * pSLGL) / avgSLG) + (((1-bSLGR)*(1-pSLGL))/(1-avgSLG))))

                        # get park factor
                        parkFactorQ = "SELECT RunsFactorP FROM parkFactors WHERE Team = %s AND Side = %s"
                        parkFactorD = (bpHomeTeam, 'L')
                        cursor.execute(parkFactorQ, parkFactorD)

                        for park in cursor:
                            parkFactor = park[0]

                elif pitcherHand == 'L':
                    # use left handed stats
                    if batterHand == 'R':
                        # use right handed stats
                        adjWOBA = (((bwOBAL * pwOBAR) / avgWOBA) / (((bwOBAL * pwOBAR) / avgWOBA) + (((1-bwOBAL)*(1-pwOBAR))/(1-avgWOBA))))
                        adjKP = (((bKPL * pKPR) / avgKP) / (((bKPL * pKPR) / avgKP) + (((1-bKPL)*(1-pKPR))/(1-avgKP))))
                        adjBBP = (((bBBL * pBBR) / avgBBP) / (((bBBL * pBBR) / avgBBP) + (((1-bBBL)*(1-pBBR))/(1-avgBBP))))
                        adjBABIP = (((bBABIPL * pBABIPR) / avgBABIP) / (((bBABIPL * pBABIPR) / avgBABIP) + (((1-bBABIPL)*(1-pBABIPR))/(1-avgBABIP))))
                        adjISO = (((bISOL * pISOR) / avgISO) / (((bISOL * pISOR) / avgISO) + (((1-bISOL)*(1-pISOR))/(1-avgISO))))
                        adjOBP = (((bOBPL * pOBPR) / avgOBP) / (((bOBPL * pOBPR) / avgOBP) + (((1-bOBPL)*(1-pOBPR))/(1-avgOBP))))
                        adjOPS = (((bOPSL * pOPSR) / avgOPS) / (((bOPSL * pOPSR) / avgOPS) + (((1-bOPSL)*(1-pOPSR))/(1-avgOPS))))
                        adjSLG = (((bSLGL * pSLGR) / avgSLG) / (((bSLGL * pSLGR) / avgSLG) + (((1-bSLGL)*(1-pSLGR))/(1-avgSLG))))
                        adjKSteve = ((bKPL * pKPR) / ((0.84 * bKPL * pKPR) + 0.16))

                        # get park factor
                        parkFactorQ = "SELECT RunsFactorP FROM parkFactors WHERE Team = %s AND Side = %s"
                        parkFactorD = (bpHomeTeam, 'R')
                        cursor.execute(parkFactorQ, parkFactorD)

                        for park in cursor:
                            parkFactor = park[0]
                    if batterHand == 'L':
                        # use left handed stats
                        adjWOBA = (((bwOBAL * pwOBAL) / avgWOBA) / (((bwOBAL * pwOBAL) / avgWOBA) + (((1-bwOBAL)*(1-pwOBAL))/(1-avgWOBA))))
                        adjKP = (((bKPL * pKPL) / avgKP) / (((bKPL * pKPL) / avgKP) + (((1-bKPL)*(1-pKPL))/(1-avgKP))))
                        adjBBP = (((bBBL * pBBL) / avgBBP) / (((bBBL * pBBL) / avgBBP) + (((1-bBBL)*(1-pBBL))/(1-avgBBP))))
                        adjBABIP = (((bBABIPL * pBABIPL) / avgBABIP) / (((bBABIPL * pBABIPL) / avgBABIP) + (((1-bBABIPL)*(1-pBABIPL))/(1-avgBABIP))))
                        adjISO = (((bISOL * pISOL) / avgISO) / (((bISOL * pISOL) / avgISO) + (((1-bISOL)*(1-pISOL))/(1-avgISO))))
                        adjOBP = (((bOBPL * pOBPL) / avgOBP) / (((bOBPL * pOBPL) / avgOBP) + (((1-bOBPL)*(1-pOBPL))/(1-avgOBP))))
                        adjOPS = (((bOPSL * pOPSL) / avgOPS) / (((bOPSL * pOPSL) / avgOPS) + (((1-bOPSL)*(1-pOPSL))/(1-avgOPS))))
                        adjSLG = (((bSLGL * pSLGL) / avgSLG) / (((bSLGL * pSLGL) / avgSLG) + (((1-bSLGL)*(1-pSLGL))/(1-avgSLG))))
                        adjKSteve = ((bKPL * pKPL) / ((0.84 * bKPL * pKPL) + 0.16))

                        # get park factor
                        parkFactorQ = "SELECT RunsFactorP FROM parkFactors WHERE Team = %s AND Side = %s"
                        parkFactorD = (bpHomeTeam, 'L')
                        cursor.execute(parkFactorQ, parkFactorD)

                        for park in cursor:
                            parkFactor = park[0]

                elif pitcherHand == 'R':
                    # use right handed stats
                    if batterHand == 'R':
                        # use right handed stats
                        adjWOBA = (((bwOBAR * pwOBAR) / avgWOBA) / (((bwOBAR * pwOBAR) / avgWOBA) + (((1-bwOBAR)*(1-pwOBAR))/(1-avgWOBA))))
                        adjKP = (((bKPR * pKPR) / avgKP) / (((bKPR * pKPR) / avgKP) + (((1-bKPR)*(1-pKPR))/(1-avgKP))))
                        adjBBP = (((bBBR * pBBR) / avgBBP) / (((bBBR * pBBR) / avgBBP) + (((1-bBBR)*(1-pBBR))/(1-avgBBP))))
                        adjBABIP = (((bBABIPR * pBABIPR) / avgBABIP) / (((bBABIPR * pBABIPR) / avgBABIP) + (((1-bBABIPR)*(1-pBABIPR))/(1-avgBABIP))))
                        adjISO = (((bISOR * pISOR) / avgISO) / (((bISOR * pISOR) / avgISO) + (((1-bISOR)*(1-pISOR))/(1-avgISO))))
                        adjOBP = (((bOBPR * pOBPR) / avgOBP) / (((bOBPR * pOBPR) / avgOBP) + (((1-bOBPR)*(1-pOBPR))/(1-avgOBP))))
                        adjOPS = (((bOPSR * pOPSR) / avgOPS) / (((bOPSR * pOPSR) / avgOPS) + (((1-bOPSR)*(1-pOPSR))/(1-avgOPS))))
                        adjSLG = (((bSLGR * pSLGR) / avgSLG) / (((bSLGR * pSLGR) / avgSLG) + (((1-bSLGR)*(1-pSLGR))/(1-avgSLG))))
                        adjKSteve = ((bKPR * pKPR) / ((0.84 * bKPR * pKPR) + 0.16))

                        # get park factor
                        parkFactorQ = "SELECT RunsFactorP FROM parkFactors WHERE Team = %s AND Side = %s"
                        parkFactorD = (bpHomeTeam, 'R')
                        cursor.execute(parkFactorQ, parkFactorD)

                        for park in cursor:
                            parkFactor = park[0]

                    if batterHand == 'L':
                        # use left handed stats
                        adjWOBA = (((bwOBAR * pwOBAL) / avgWOBA) / (((bwOBAR * pwOBAL) / avgWOBA) + (((1-bwOBAR)*(1-pwOBAL))/(1-avgWOBA))))
                        adjKP = (((bKPR * pKPL) / avgKP) / (((bKPR * pKPL) / avgKP) + (((1-bKPR)*(1-pKPL))/(1-avgKP))))
                        adjBBP = (((bBBR * pBBL) / avgBBP) / (((bBBR * pBBL) / avgBBP) + (((1-bBBR)*(1-pBBL))/(1-avgBBP))))
                        adjBABIP = (((bBABIPR * pBABIPL) / avgBABIP) / (((bBABIPR * pBABIPL) / avgBABIP) + (((1-bBABIPR)*(1-pBABIPL))/(1-avgBABIP))))
                        adjISO = (((bISOR * pISOL) / avgISO) / (((bISOR * pISOL) / avgISO) + (((1-bISOR)*(1-pISOL))/(1-avgISO))))
                        adjOBP = (((bOBPR * pOBPL) / avgOBP) / (((bOBPR * pOBPL) / avgOBP) + (((1-bOBPR)*(1-pOBPL))/(1-avgOBP))))
                        adjOPS = (((bOPSR * pOPSL) / avgOPS) / (((bOPSR * pOPSL) / avgOPS) + (((1-bOPSR)*(1-pOPSL))/(1-avgOPS))))
                        adjSLG = (((bSLGR * pSLGL) / avgSLG) / (((bSLGR * pSLGL) / avgSLG) + (((1-bSLGR)*(1-pSLGL))/(1-avgSLG))))
                        adjKSteve = ((bKPR * pKPL) / ((0.84 * bKPR * pKPL) + 0.16))

                        # get park factor
                        parkFactorQ = "SELECT RunsFactorP FROM parkFactors WHERE Team = %s AND Side = %s"
                        parkFactorD = (bpHomeTeam, 'L')
                        cursor.execute(parkFactorQ, parkFactorD)

                        for park in cursor:
                            parkFactor = park[0]

                adjKP = (adjKP + adjKSteve)/2

                updateBProjectionsQuery = "UPDATE battersdaily SET adjWOBA = %s, adjKP = %s, adjBBP = %s, adjBABIP = %s, adjISO = %s, adjOBP = %s, adjOPS = %s, adjSLG = %s, parkFactor = %s, variance = %s, wOBA = %s, ISO = %s, SLG = %s, OPS = %s, OBP = %s, KP = %s, BB = %s, BABIP = %s, adjSB = %s WHERE batterID = %s AND bgameID = %s"
                updateBProjectionsData = (adjWOBA, adjKP, adjBBP, adjBABIP, adjISO, adjOBP, adjOPS, adjSLG, parkFactor, float(varianceBat), bWOBA, bISO, bSLG, bOPS, bOBP, bKP, bBB, bBABIP, sbRate, trueBID, gameID)
                cursor.execute(updateBProjectionsQuery, updateBProjectionsData)

    print "Updated Projections based on Pitchers and Current Stats"

def rotowireProjections(day, month, year, cursor):
    url = "http://www.rotowire.com/daily/mlb/optimizer.htm?site=DraftKings&sport=MLB"

    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    rotoWireData = []

    for tr in soup.find_all('tr')[4:]:
        tds = tr.find_all('td')

        playerData = {}

        playerID = tr['data-playerid']
        playerData['id'] = playerID

        # name
        playerInfo = tds[1]

        playerName = playerInfo.a
        playerName = playerName.text
        playerName = str(playerName.encode('utf-8'))
        firstName, lastName = playerName.split(" ", 1)
        playerData['firstName'] = firstName
        playerData['lastName'] = lastName

        salary = tds[6]['data-salary']
        salary = salary.replace(",", "")
        playerData['salary'] = salary

        projPts = tds[7]['data-points']
        playerData['points'] = projPts

        team = tds[2]['data-team']
        team = str(team.encode('utf-8'))
        playerData['team'] = team

        position = tds[3].text
        position = str(position.encode('utf-8'))
        playerData['position'] = position

        rotoWireData.append(playerData)

    for player in rotoWireData:
        if player['position'] == "P":
            # update rotowire projection and salary - get from rotowire id, if null get from first name + last name
            playerRetrieveQuery = "SELECT key_mlbam FROM people WHERE rotowireID = %s"
            playerRetrieveData = (player['id'],)
            cursor.execute(playerRetrieveQuery, playerRetrieveData)

            playerMLBID = 0
            if not cursor.rowcount:
                playerRetrieveQuery = "SELECT key_mlbam FROM people WHERE (name_first = %s AND name_last = %s)"
                playerRetrieveData = (player['firstName'], player['lastName'])
                cursor.execute(playerRetrieveQuery, playerRetrieveData)

                for mlbID in cursor:
                    playerMLBID = mlbID[0]

                # update rotowire ID
                playerUpdateRotoIDQ = "UPDATE people SET rotowireID = %s WHERE key_mlbam = %s"
                playerUpdateRotoIDD = (player['id'], playerMLBID)
                cursor.execute(playerUpdateRotoIDQ, playerUpdateRotoIDD)

            else:
                for mlbID in cursor:
                    playerMLBID = mlbID[0]

            playerDateQuery = "SELECT idpitchers FROM pitchers WHERE mlbID = %s"
            playerDateData = (playerMLBID,)
            cursor.execute(playerDateQuery, playerDateData)

            idPitcher = 0
            for idP in cursor:
                idPitcher = idP[0]

            gameID = getDate(day, month, year, cursor)

            updatePProjectionQuery = "UPDATE pitchersdaily SET rotowirePoints = %s, dkSalary = %s WHERE pitcherID = %s AND pgameID = %s"
            updatePProjectionData = (player['points'], player['salary'], idPitcher, gameID)
            cursor.execute(updatePProjectionQuery, updatePProjectionData)
        else:
            playerRetrieveQuery = "SELECT key_mlbam FROM people WHERE rotowireID = %s"
            playerRetrieveData = (player['id'],)
            cursor.execute(playerRetrieveQuery, playerRetrieveData)

            playerMLBID = 0
            if not cursor.rowcount:
                playerRetrieveQuery = "SELECT key_mlbam FROM people WHERE (name_first = %s AND name_last = %s)"
                playerRetrieveData = (player['firstName'], player['lastName'])
                cursor.execute(playerRetrieveQuery, playerRetrieveData)

                for mlbID in cursor:
                    playerMLBID = mlbID[0]

                # update rotowire ID
                playerUpdateRotoIDQ = "UPDATE people SET rotowireID = %s WHERE key_mlbam = %s"
                playerUpdateRotoIDD = (player['id'], playerMLBID)
                cursor.execute(playerUpdateRotoIDQ, playerUpdateRotoIDD)

            else:
                for mlbID in cursor:
                    playerMLBID = mlbID[0]

            playerDateQuery = "SELECT idpitchers FROM pitchers WHERE mlbID = %s"
            playerDateData = (playerMLBID,)
            cursor.execute(playerDateQuery, playerDateData)

            # update player postion
            playerUpdatePositionQ = "UPDATE batters SET pos = %s WHERE mlbID = %s"
            playerUpdatePositionD = (player['position'], playerMLBID)
            cursor.execute(playerUpdatePositionQ, playerUpdatePositionD)

            # set dk salary
            playerDateQuery = "SELECT idbatters FROM batters WHERE mlbID = %s"
            playerDateData = (playerMLBID,)
            cursor.execute(playerDateQuery, playerDateData)

            idBatter = 0
            for idP in cursor:
                idBatter = idP[0]

            gameID = getDate(day, month, year, cursor)

            updatePProjectionQuery = "UPDATE battersdaily SET dkSalary = %s WHERE batterID = %s AND bgameID = %s"
            updatePProjectionData = (player['salary'], idBatter, gameID)
            cursor.execute(updatePProjectionQuery, updatePProjectionData)

    print ("Updated Rotowire Projection for Pitchers")
    print ("Update Salaries and Positions for All Players")

    return

def saberSimProjections(day, month, year, cursor):
    url = "http://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim&team=0&lg=all&players=0"

    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    saberSimData = []
    for tr in soup.find_all('tr')[4:]:
        tds = tr.find_all('td')

        playerData = {}

        playerInfo = tds[0]

        playerName = playerInfo.a
        playerName = playerName.text
        playerName = str(playerName.encode('utf-8'))
        firstName, lastName = playerName.split(" ", 1)
        playerData['firstName'] = firstName
        playerData['lastName'] = lastName

        playerID = playerInfo.a['href']
        junk,ID = playerID.split('playerid=')
        ID,position = ID.split('&position=')

        playerData['id'] = ID
        playerData['position'] = position

        dkPoints = tds[15].text
        dkPoints = dkPoints.strip()
        playerData['points'] = dkPoints

        saberSimData.append(playerData)

    for player in saberSimData:
        playerRetrieveQuery = "SELECT key_mlbam FROM people WHERE key_fangraphs = %s"
        playerRetrieveData = (player['id'],)
        cursor.execute(playerRetrieveQuery, playerRetrieveData)

        playerMLBID = 0
        for mlbID in cursor:
            playerMLBID = mlbID[0]

        playerDateQuery = "SELECT idpitchers FROM pitchers WHERE mlbID = %s"
        playerDateData = (playerMLBID,)
        cursor.execute(playerDateQuery, playerDateData)

        idPitcher = 0
        for idP in cursor:
            idPitcher = idP[0]

        gameID = getDate(day, month, year, cursor)

        updatePProjectionQuery = "UPDATE pitchersdaily SET saberSimPoints = %s WHERE pitcherID = %s AND pgameID = %s"
        updatePProjectionData = (player['points'], idPitcher, gameID)
        cursor.execute(updatePProjectionQuery, updatePProjectionData)

    print ("Updated SaberSim Projection for Pitchers")

    return

def rotogrindersProjections(day, month, year, cursor, type, link):
    url = link

    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    # get object
    script = soup.find_all("script")
    script = script[14].text

    # strip all junk
    scriptJunk, rotoObject = script.split("=")
    rotoObject, scriptJunk = rotoObject.split("projectedStats.init(data")
    rotoObject = rotoObject.lstrip()
    rotoObject = rotoObject.rstrip()
    rotoObject = rotoObject[:-1]

    rotoProj = demjson.decode(rotoObject)

    rotogrindersData = []

    for line in rotoProj:
        playerData = {}

        firstName = (line['player']['first_name'])
        lastName = (line['player']['last_name'])
        playerData['firstName'] = firstName
        playerData['lastName'] = lastName

        id = (line['player']['id'])
        playerData['id'] = id

        position = (line['position'])
        playerData['position'] = position

        team = (line['team'])
        playerData['team'] = team

        points = (line['points'])
        playerData['points'] = points

        pOwn = (line['pown%'])
        if pOwn is None:
            playerData['pOWN'] = .001
        else:
            pOwn = pOwn.replace("%", "")
            pOwn = float(pOwn)
            pOwn = pOwn/100
            playerData['pOWN'] = pOwn

        rotogrindersData.append(playerData)

    for player in rotogrindersData:
        playerRetrieveQuery = "SELECT key_mlbam FROM people WHERE rotogrindersID = %s"
        playerRetrieveData = (player['id'],)
        cursor.execute(playerRetrieveQuery, playerRetrieveData)

        playerMLBID = 0
        if not cursor.rowcount:
            playerRetrieveQuery = "SELECT key_mlbam, rotogrindersID FROM people WHERE (name_first = %s AND name_last = %s)"
            playerRetrieveData = (player['firstName'], player['lastName'])
            cursor.execute(playerRetrieveQuery, playerRetrieveData)

            for mlbID in cursor:
                playerMLBID = mlbID[0]

            # update rotogrinders ID
            playerUpdateRotoIDQ = "UPDATE people SET rotogrindersID = %s WHERE key_mlbam = %s"
            playerUpdateRotoIDD = (player['id'], playerMLBID)
            cursor.execute(playerUpdateRotoIDQ, playerUpdateRotoIDD)
        else:
            for mlbID in cursor:
                playerMLBID = mlbID[0]

        if type == "pitcher":
            playerDateQuery = "SELECT idpitchers FROM pitchers WHERE mlbID = %s"
            playerDateData = (playerMLBID,)
            cursor.execute(playerDateQuery, playerDateData)

            idPitcher = 0
            for idP in cursor:
                idPitcher = idP[0]

            gameID = getDate(day, month, year, cursor)

            updatePProjectionQuery = "UPDATE pitchersdaily SET rotogrindersPoints = %s, pOWN = %s WHERE pitcherID = %s AND pgameID = %s"
            updatePProjectionData = (player['points'], player['pOWN'], idPitcher, gameID)
            cursor.execute(updatePProjectionQuery, updatePProjectionData)

        if type == "batter":
            playerDateQuery = "SELECT idbatters FROM batters WHERE mlbID = %s"
            playerDateData = (playerMLBID,)
            cursor.execute(playerDateQuery, playerDateData)

            idBatter = 0
            for idP in cursor:
                idBatter = idP[0]

            gameID = getDate(day, month, year, cursor)

            updateBProjectionQuery = "UPDATE battersdaily SET rotogrindersPoints = %s, pOWN = %s WHERE batterID = %s AND bgameID = %s"
            updateBProjectionData = (player['points'], player['pOWN'], idBatter, gameID)
            cursor.execute(updateBProjectionQuery, updateBProjectionData)


    print ("Updated Rotogrinders Projection for " + type)

def pitcherAggProjections(day, month, year, cursor):

    gameID = getDate(day, month, year, cursor)
    numProjections = 2

    getEligPitchersQ = "SELECT * FROM pitchers WHERE start = 1"
    cursor.execute(getEligPitchersQ)

    allPitchers = cursor.fetchall()

    for pitcher in allPitchers:
        # get dkpoints + calculated variance
        getPerformanceQ = "SELECT dkpoints FROM pitchersdaily WHERE pitcherID = %s AND dkpoints IS NOT NULL AND pgameID != %s"
        getPerformanceD = (pitcher[0], gameID)
        cursor.execute(getPerformanceQ, getPerformanceD)

        variancePitch = 0

        dkpoints = []
        for dkpoint in cursor:
            dkpoints.append(dkpoint[0])

        # remove outliers
        if dkpoints:
            medianDKPoints = np.median(dkpoints)
            medianDKPoints = float(medianDKPoints)
            upperRange = (1.5)*(medianDKPoints)
            lowerRange = medianDKPoints - ((1.5)*medianDKPoints - medianDKPoints)

            updatedDKPoints = [i for i in dkpoints if (i <= upperRange)]
            if updatedDKPoints:
                variancePitch = np.std(updatedDKPoints)

        pitcherID = pitcher[0]

        # get projections
        getProjectionsPQ = "SELECT rotogrindersPoints, saberSimPoints, rotowirePoints FROM pitchersdaily WHERE pitcherID = %s AND pgameID = %s"
        getProjectionsPD = (pitcherID, gameID)
        cursor.execute(getProjectionsPQ, getProjectionsPD)

        for projections in cursor:
            aggregateProjections = 0
            try:
                aggregateProjections = (projections[0] + projections[1])/numProjections
            except:
                pass

            updateProjectionsQ = "UPDATE pitchersdaily SET dkPointsPred = %s, variance = %s WHERE pitcherID = %s and pgameID = %s"
            updateProjectionsD = (aggregateProjections, variancePitch, pitcherID, gameID)

            cursor.execute(updateProjectionsQ, updateProjectionsD)

    print ("Updated Projections for Pitchers")

if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root',
                                  host='127.0.0.1',
                                  database='baseball')
    cursor = cnx.cursor(buffered=True)

    year = 2017
    month = 7
    day = 28

    updateLeagueProjections(cursor)
    getParkFactors(cursor)
    updateBatterProjections(day, month, year, cursor)
    rotowireProjections(day, month, year, cursor)
    saberSimProjections(day, month, year, cursor)
    rotogrindersProjections(day, month, year, cursor, "pitcher", "https://rotogrinders.com/projected-stats/mlb-pitcher?site=draftkings")
    rotogrindersProjections(day, month, year, cursor, "batter", "https://rotogrinders.com/projected-stats/mlb-hitter?site=draftkings")
    pitcherAggProjections(day, month, year, cursor)

    cursor.close()
    cnx.commit()
    cnx.close()