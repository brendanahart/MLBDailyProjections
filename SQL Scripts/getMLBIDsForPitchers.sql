UPDATE baseball.zipspitcherplatoon
SET mlbID = (SELECT mlbID FROM baseball.pitchers 
		WHERE baseball.pitchers.playerName = baseball.zipspitcherplatoon.Player
        LIMIT 1)
        
