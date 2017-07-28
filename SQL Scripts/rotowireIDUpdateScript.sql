UPDATE baseball.people 
    SET people.rotowireID = (
        SELECT ROTOWIREID
        FROM baseball.master
        WHERE master.MLBID = people.key_mlbam
    );
