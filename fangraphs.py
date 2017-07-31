from bs4 import BeautifulSoup
import urllib2
import mysql.connector
import numpy as np
import math
import constants
import csv

def fangraphsTeamStats(url, cursor):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('tbody')[0]

    for player in data.find_all('tr'):
        tds = player.find_all('td')
        teamName = tds[1].a.text
        bbRate = float(tds[8].text[:-2])/100
        kRate = float(tds[9].text[:-2])/100
        iso = tds[10].text
        babip = tds[11].text
        avg = tds[12].text
        obp = tds[13].text
        slg = tds[14].text
        wOBA = tds[15].text

        # Insert or Update
        queryMLBID = "SELECT DKTEAM from teammap WHERE FANGRAPHSTEAM = %s"
        queryMLBIDData = (teamName,)

        cursor.execute(queryMLBID, queryMLBIDData)

        for team in cursor:
            try:
                # insert into batters table, update if not there
                addTeam = "INSERT INTO teams (teamName, teamAbbrv, BBP, KP, ISO, BABIP, AVG, OBP, SLG, wOBA) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                teamData = (teamName, team[0], bbRate, kRate, iso, babip, avg, obp, slg, wOBA)
                cursor.execute(addTeam, teamData)
            except:
                addTeam = "UPDATE teams SET BBP = %s, KP = %s, ISO = %s, BABIP = %s, AVG = %s, OBP = %s, SLG = %s, wOBA = %s WHERE teamAbbrv = %s and teamName = %s"
                teamData = (bbRate, kRate, iso, babip, avg, obp, slg, wOBA, team[0], teamName)
                cursor.execute(addTeam, teamData)

def fangraphsPitcherAdvSplits(url, cursor, split):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('tbody')[0]

    for player in data.find_all('tr'):
        tds = player.find_all('td')
        playerName = tds[1].a.text
        playerID = tds[1].a['href']
        junk,ID = playerID.split('playerid=')
        ID,junk = ID.split('&position=')
        kRate = float(tds[7].text[:-2])/100
        bbRate = float(tds[8].text[:-2])/100
        whip = tds[11].text
        babip = tds[12].text
        xfip = tds[17].text


        # Insert or Update
        queryMLBID = "SELECT key_mlbam from people WHERE key_fangraphs = %s"
        queryMLBIDData = (ID,)

        cursor.execute(queryMLBID, queryMLBIDData)

        for idpitcher in cursor:
            if split == 'L':
                try:
                    # insert into batters table, update if not there
                    addPitcher = "INSERT INTO pitchers (mlbID, KPL, BBL, WHIPL, BABIPL, xFIPL) VALUES(%s, %s, %s, %s, %s, %s)"
                    pitcherData = (int(idpitcher[0]), kRate, bbRate, whip, babip, xfip)
                    cursor.execute(addPitcher, pitcherData)
                except:
                    addPitcher = "UPDATE pitchers SET KPL = %s, BBL = %s, WHIPL = %s, BABIPL = %s, xFIPL = %s WHERE mlbID = %s"
                    pitcherData = (kRate, bbRate, whip, babip, xfip, int(idpitcher[0]))
                    cursor.execute(addPitcher, pitcherData)
            else:
                try:
                    # insert into batters table, update if not there
                    addPitcher = "INSERT INTO pitchers (mlbID, KPR, BBR, WHIPR, BABIPR, xFIPR) VALUES(%s, %s, %s, %s, %s, %s)"
                    pitcherData = (int(idpitcher[0]), kRate, bbRate, whip, babip, xfip)
                    cursor.execute(addPitcher, pitcherData)
                except:
                    addPitcher = "UPDATE pitchers SET KPR = %s, BBR = %s, WHIPR = %s, BABIPR = %s, xFIPR = %s WHERE mlbID = %s"
                    pitcherData = (kRate, bbRate, whip, babip, xfip, int(idpitcher[0]))
                    cursor.execute(addPitcher, pitcherData)

def fangraphsBatterStats(url, cursor):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('tbody')[0]

    stolenBasesDict = {}
    stolenBaseData = []

    for player in data.find_all('tr'):
        tds = player.find_all('td')
        ID = -1
        if tds[1].find_all('a'):
            playerID = tds[1].a['href']
            junk,ID = playerID.split('playerid=')
            ID,junk = ID.split('&position=')
        bbRate = float(tds[4].text[:-2])/100
        kRate = float(tds[5].text[:-2])/100
        obp = tds[8].text
        slg = tds[9].text
        ops = tds[10].text
        iso = tds[11].text
        babip = tds[13].text
        wSB = tds[16].text
        wSB = float(wSB)
        wOBA = tds[19].text
        stolenBaseData.append(wSB)

        # Insert or Update
        queryMLBID = "SELECT key_mlbam from people WHERE key_fangraphs = %s"
        queryMLBIDData = (ID,)

        cursor.execute(queryMLBID, queryMLBIDData)

        for idbatter in cursor:
            stolenBasesDict[int(idbatter[0])] = wSB
            try:
                # insert into batters table, update if not there
                addBatter = "INSERT INTO batters (mlbID, wOBA, ISO, OBP, SLG, OPS, KP, BB, BABIP, wSB) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                batterData = (int(idbatter[0]), wOBA, iso, obp, slg, ops, kRate, bbRate, babip, wSB)
                cursor.execute(addBatter, batterData)
            except:
                addBatter = "UPDATE batters SET wOBA = %s, ISO = %s, OBP = %s, SLG = %s, OPS = %s, KP = %s, BB = %s, BABIP = %s, wSB = %s WHERE mlbID = %s"
                batterData = (wOBA, iso, obp, slg, ops, kRate, bbRate, babip, wSB, int(idbatter[0]))
                cursor.execute(addBatter, batterData)

    stolenBaseMax = np.amax(stolenBaseData)
    stolenBaseMin = np.amin(stolenBaseData)

    for k,v in stolenBasesDict.iteritems():
        newWSB = (v - stolenBaseMin)/(stolenBaseMax - stolenBaseMin)
        queryUpdateSBQ = "UPDATE batters SET wSB = %s WHERE mlbID = %s"
        queryUpdateSBD = (float(newWSB), k)
        cursor.execute(queryUpdateSBQ, queryUpdateSBD)

def fangraphsPitcherBasicSplits(url, cursor, split):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('tbody')[0]

    for player in data.find_all('tr'):
        tds = player.find_all('td')
        playerName = tds[1].a.text
        playerID = tds[1].a['href']
        junk,ID = playerID.split('playerid=')
        ID,junk = ID.split('&position=')
        ip = tds[3].text
        era = tds[4].text
        avg = tds[14].text
        obp = tds[15].text
        slg = tds[16].text
        woba = tds[17].text

        # Insert or Update
        queryMLBID = "SELECT key_mlbam from people WHERE key_fangraphs = %s"
        queryMLBIDData = (ID,)

        cursor.execute(queryMLBID, queryMLBIDData)

        for idpitcher in cursor:
            if split == 'L':
                try:
                    # insert into batters table, update if not there
                    addPitcher = "INSERT INTO pitchers (mlbID, ERAL, AVGL, OBPL, SLGL, WOBAL, IPL) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    pitcherData = (int(idpitcher[0]), era, avg, obp, slg, woba, ip)
                    cursor.execute(addPitcher, pitcherData)
                except:
                    addPitcher = "UPDATE pitchers SET ERAL = %s, AVGL = %s, OBPL = %s, SLGL = %s, WOBAL = %s, IPL = %s WHERE mlbID = %s"
                    pitcherData = (era, avg, obp, slg, woba, ip, int(idpitcher[0]))
                    cursor.execute(addPitcher, pitcherData)
            else:
                try:
                    # insert into batters table, update if not there
                    addPitcher = "INSERT INTO pitchers (mlbID, ERAR, AVGR, OBPR, SLGR, WOBAR, IPR) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    pitcherData = (int(idpitcher[0]), era, avg, obp, slg, woba, ip)
                    cursor.execute(addPitcher, pitcherData)
                except:
                    addPitcher = "UPDATE pitchers SET ERAR = %s, AVGR = %s, OBPR = %s, SLGR = %s, WOBAR = %s, IPR = %s WHERE mlbID = %s"
                    pitcherData = (era, avg, obp, slg, woba, ip, int(idpitcher[0]))
                    cursor.execute(addPitcher, pitcherData)

def fangraphsBatterAdvSplits(url, cursor, split):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('tbody')[0]

    for player in data.find_all('tr'):
        tds = player.find_all('td')
        playerID = tds[1].a['href']
        junk,ID = playerID.split('playerid=')
        ID,junk = ID.split('&position=')
        pa = tds[3].text
        bbRate = float(tds[4].text[:-2])/100
        kRate = float(tds[5].text[:-2])/100
        obp = tds[8].text
        slg = tds[9].text
        ops = tds[10].text
        iso = tds[11].text
        babip = tds[13].text
        wOBA = tds[16].text

        # Insert or Update
        queryMLBID = "SELECT key_mlbam from people WHERE key_fangraphs = %s"
        queryMLBIDData = (ID,)

        cursor.execute(queryMLBID, queryMLBIDData)

        for idbatter in cursor:
            if split == 'L':
                try:
                    # insert into batters table, update if not there
                    addBatter = "INSERT INTO batters (mlbID, paL, BBL, KPL, OBPL, SLGL, OPSL, ISOL, BABIPL, wOBAL) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    batterData = (int(idbatter[0]), pa, bbRate, kRate, obp, slg, ops, iso, babip, wOBA)
                    cursor.execute(addBatter, batterData)
                except:
                    addBatter = "UPDATE batters SET paL = %s, BBL = %s, KPL = %s, OBPL = %s, SLGL = %s, OPSL = %s, ISOL = %s, BABIPL = %s, wOBAL = %s WHERE mlbID = %s"
                    batterData = (pa, bbRate, kRate, obp, slg, ops, iso, babip, wOBA, int(idbatter[0]))
                    cursor.execute(addBatter, batterData)
            else:
                try:
                    # insert into batters table, update if not there
                    addBatter = "INSERT INTO batters (mlbID, paR, BBR, KPR, OBPR, SLGR, OPSR, ISOR, BABIPR, wOBAR) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    batterData = (int(idbatter[0]), pa, bbRate, kRate, obp, slg, ops, iso, babip, wOBA)
                    cursor.execute(addBatter, batterData)
                except:
                    addBatter = "UPDATE batters SET paR = %s, BBR = %s, KPR = %s, OBPR = %s, SLGR = %s, OPSR = %s, ISOR = %s, BABIPR = %s, wOBAR = %s WHERE mlbID = %s"
                    batterData = (pa, bbRate, kRate, obp, slg, ops, iso, babip, wOBA, int(idbatter[0]))
                    cursor.execute(addBatter, batterData)

def fangraphsFielding(url, cursor):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('tbody')[0]

    for player in data.find_all('tr'):
        tds = player.find_all('td')
        playerName = tds[1].a.text
        playerID = tds[1].a['href']
        junk,ID = playerID.split('playerid=')
        ID,junk = ID.split('&position=')
        ip = tds[6].text
        sb = tds[17].text
        adjIP = math.ceil(float(ip))
        sbProbaility = 0
        if adjIP != 0:
            sbProbaility = float(sb)/adjIP

        # Insert or Update
        queryMLBID = "SELECT key_mlbam from people WHERE key_fangraphs = %s"
        queryMLBIDData = (ID,)

        cursor.execute(queryMLBID, queryMLBIDData)

        for idpitcher in cursor:
            addPitcher = "UPDATE pitchers SET sbRate = %s WHERE mlbID = %s"
            pitcherData = (sbProbaility, int(idpitcher[0]))
            cursor.execute(addPitcher, pitcherData)

def fangraphsUpdateSeasonStats(path, filename, day, month, year, cursor):
    file = path + filename + str(day) + str(month) + str(year) + '.csv'
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            queryMLBID = "SELECT key_mlbam from people WHERE key_fangraphs = %s"
            queryMLBIDData = (row['playerid'],)

            cursor.execute(queryMLBID, queryMLBIDData)

            for idbatter in cursor:
                try:
                    # insert into batters table, update if not there
                    addBatter = "INSERT INTO batters (mlbID, wOBA, ISO, OBP, SLG, OPS, KP, BB, BABIP, wSB) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    batterData = (int(idbatter[0]), row['w OBA'], row['ISO'], row['OBP'], row['SLG'], row['OPS'], row['K%'], row['BB%'], row['BABIP'])
                    cursor.execute(addBatter, batterData)
                except:
                    addBatter = "UPDATE batters SET wOBA = %s, ISO = %s, OBP = %s, SLG = %s, OPS = %s, KP = %s, BB = %s, BABIP = %s WHERE mlbID = %s"
                    batterData = (row['w OBA'], row['ISO'], row['OBP'], row['SLG'], row['OPS'], row['K%'], row['BB%'], row['BABIP'], int(idbatter[0]))
                    cursor.execute(addBatter, batterData)
    return

if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.databaseUser,
                                  host=constants.databaseHost,
                                  database=constants.databaseName,
                                  password=constants.databasePassword)
    cursor = cnx.cursor()

    '''
    fangraphsUpdateSeasonStats('/Development/Baseball/FangraphsStats/', 'FanGraphsSplitsLeaderboardData',
    constants.dayP, constants.monthP, constants.yearP, cursor)
    print ("Updated Season Stats")

    '''

    fangraphsBatterAdvSplits(constants.BatterAdvSplitsL, cursor, 'L')
    fangraphsBatterAdvSplits(constants.BatterAdvSplitsR, cursor, 'R')

    print "Updated Splits for Batters from Fangraphs for Season"

    fangraphsBatterStats(constants.BatterStatsSeason, cursor)

    print "Updated Stats for Batters from Fangraphs for Season"

    fangraphsPitcherBasicSplits(constants.PitcherBasicSplitsL, cursor, 'L')
    fangraphsPitcherBasicSplits(constants.PitcherBasicSplitsR, cursor, 'R')

    print "Updated Basic Splits for Pitchers from Fangraphs for Season"

    fangraphsPitcherAdvSplits(constants.PitcherAdvSplitsL, cursor, 'L')
    fangraphsPitcherAdvSplits(constants.PitcherAdvSplitsR, cursor, 'R')

    print "Updated Advanced Splits for Pitchers from Fangraphs for Season"

    fangraphsFielding(constants.Fielding, cursor)
    print "Updated Stolen Base Data for Pitchers from Fangraphs for Season"

    fangraphsTeamStats(constants.TeamStats, cursor)

    print "Updated Team Data from Fangraphs for past 30 days"

    cursor.close()
    cnx.commit()
    cnx.close()