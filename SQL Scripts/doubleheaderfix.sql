# teams are teams in double header
# oppPitcher ID is the ID for the pitchers not in the games we are optimizing
# bgameID is the id for the date of the double header 

DELETE FROM baseball.battersdaily 
WHERE (team = 'Rockies' OR team = 'Nationals') AND bgameID = 166 AND (oppPitcher = 0 OR oppPitcher = 1744)