from bs4 import BeautifulSoup
import urllib2
import mysql.connector
import demjson

def rotogrindersPitcherBaseball(url, csv_filename, stats):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    jsonData = soup.find_all('script')[12]
    print len(jsonData)

    jsonData = jsonData.text

    junk, jsonData = jsonData.split("var data =")
    jsonData = jsonData.lstrip()
    jsonData = jsonData.rstrip()

    jsonData, junk = jsonData.split("var pageType =")
    jsonData = jsonData.rstrip()
    jsonData = jsonData.lstrip()

    jsonData = jsonData[:-1]

    basketballData = demjson.decode(jsonData)

    for playerData in basketballData:
        player = playerData['player']
        team = playerData['team']
        pos = playerData['pos']
        salary = playerData['salary']
        gp = playerData['gp']
        mins = float(playerData['min']) / float(gp)
        reb = float(playerData['reb']) / float(gp)
        ast = float(playerData['ast']) / float(gp)
        stl = float(playerData['stl']) / float(gp)
        blk = float(playerData['blk']) / float(gp)
        to = float(playerData['to']) / float(gp)
        pts = float(playerData['pts']) / float(gp)
        usg = playerData['usg']
        fpts = playerData['fpts']
        fpts = float(fpts) / float(gp)
        fpts = round(fpts, 2)

        data = (player, team, pos, salary, gp, mins, reb, ast, stl, blk, to, pts, usg, fpts)
        file.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \n' % data)

    file.close()

def rotogrindersBatterBaseball(url, cursor):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    jsonData = soup.find_all('script')[13]
    print len(jsonData)

    jsonData = jsonData.text

    junk,jsonData = jsonData.split("var data =")
    jsonData = jsonData.lstrip()
    jsonData = jsonData.rstrip()

    jsonData,junk = jsonData.split("var pageType =")
    jsonData = jsonData.rstrip()
    jsonData = jsonData.lstrip()

    jsonData = jsonData[:-1]

    baseballData = demjson.decode(jsonData)

    for playerData in baseballData:
        player = playerData['player']
        rotoid = playerData['id']
        team = playerData['team']
        pos = playerData['pos']
        salary = playerData['salary']
        gp = playerData['gp']
        ab = playerData['ab']
        h = playerData['h']
        singles = playerData['1b']
        doubles = playerData['2b']
        triples = playerData['3b']
        hr = playerData['hr']
        runs = playerData['r']
        rbi = playerData['rbi']
        bb = playerData['bb']
        so = playerData['so']
        sb = playerData['sb']
        sf = playerData['sf']
        gidp = playerData['gidp']
        obp = playerData['obp']
        slg = playerData['slg']
        iso = playerData['iso']
        ops = playerData['ops']
        xbh = playerData['xbh']
        kbb = playerData['kbb']
        babip = playerData['babip']
        woba = playerData['woba']
        fpts = playerData['fpts']


if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root',
                                  host='127.0.0.1',
                                  database='baseball')
    cursor = cnx.cursor()

    rotogrindersBatterBaseball("https://rotogrinders.com/game-stats/mlb-hitter?site=fanduel&range=season&split=lefty", cursor)
    rotogrindersBatterBaseball("https://rotogrinders.com/game-stats/mlb-hitter?site=fanduel&range=season&split=righty", cursor)