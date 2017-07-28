import mysql.connector
import urllib2
import lxml.etree as etree
import mlbgame
from datetime import date


def getMLBOdds(year, month, day, cursor):
    findGame = 'SELECT iddates FROM dates WHERE date = %s'
    findGameData = (date(year, month, day),)
    cursor.execute(findGame, findGameData)

    dateID = -1
    for datez in cursor:
        dateID = datez[0]

    base_url = "http://sportsfeeds.bovada.lv/basic/MLB.xml"
    data = urllib2.urlopen(base_url)
    xml = etree.parse(data)

    root = xml.getroot()

    mlbOdds = {}
    for game in root.iterfind(".//Event"):
        for team in game.iterfind(".//Competitor"):
            bballTeam = team.get("NAME")
            for line in team.iterfind(".//Line"):
                if line.get("TYPE") == "Moneyline":
                    odds = line.find(".//Odds")
                    odd = odds.get("Line")
                    if odd == "EVEN":
                        odd = "+100"
                    mlbOdds[bballTeam] = odd

    for key, value in mlbOdds.iteritems():
        # convert value to probability
        lineC = value[1:]
        probability = 0
        if value[0] == '+':
            probability = (100/(float(lineC) + 100))
        else:
            probability = (float(lineC)/(float(lineC) + 100))

        getAbbrev = "SELECT FANGRAPHSABBR FROM teammap WHERE BOVADA = %s"
        getAbbrevD = (key,)
        cursor.execute(getAbbrev, getAbbrevD)

        teamAbbr = ""
        for data in cursor:
            teamAbbr = data[0]

        getGameQ = "SELECT * FROM games WHERE date = %s and home = %s"
        getGameD = (dateID, teamAbbr)
        cursor.execute(getGameQ, getGameD)

        gameData = cursor.fetchall()

        # away team - data is empty
        if not gameData:
            setGameOddQ = "UPDATE games SET moneyLineAway = %s, awayWinProb = %s WHERE date = %s and away = %s"
            getGameOddD = (value, probability, dateID, teamAbbr)
            cursor.execute(setGameOddQ, getGameOddD)
        # home team
        else:
            setGameOddQ = "UPDATE games SET moneyLineHome = %s, homeWinProb = %s WHERE date = %s and home = %s"
            getGameOddD = (value, probability, dateID, teamAbbr)
            cursor.execute(setGameOddQ, getGameOddD)

    print "Set Odds for Games on %s/%s/%s" % (month, day, year)

def getSchedule(year, month, day, cursor):
    addDate = "INSERT INTO dates (date) VALUES(%s)"
    dateData = (date(year, month, day),)

    cursor.execute(addDate, dateData)
    gameID = cursor.lastrowid

    games = mlbgame.day(year, month, day)
    for game in games:
        awayTeam = game.away_team
        homeTeam = game.home_team

        # select fangraphs abbrev
        awayTeamQ = "SELECT FANGRAPHSABBR FROM teammap WHERE MLBAPI = %s"
        awayTeamD = (awayTeam, )
        cursor.execute(awayTeamQ, awayTeamD)
        awayTeamAbbr = ""
        for team in cursor:
            awayTeamAbbr = team[0]

        homeTeamQ = "SELECT FANGRAPHSABBR FROM teammap WHERE MLBAPI = %s"
        homeTeamD = (homeTeam,)
        cursor.execute(homeTeamQ, homeTeamD)
        homeTeamAbbr = ""
        for team in cursor:
            homeTeamAbbr = team[0]

        # insert into games
        addGame = "INSERT INTO games (home, away, date) VALUES (%s, %s, %s)"
        gameData = (homeTeamAbbr, awayTeamAbbr, gameID)
        cursor.execute(addGame, gameData)

    print "Loaded Games for %s/%s/%s" % (month, day, year)


if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root',
                                  host='127.0.0.1',
                                  database='baseball')
    cursor = cnx.cursor()

    # get games
    year = 2017
    month = 7
    day = 28

    getSchedule(year, month, day, cursor)
    getMLBOdds(year, month, day, cursor)

    cursor.close()
    cnx.commit()
    cnx.close()