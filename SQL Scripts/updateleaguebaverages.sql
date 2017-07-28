UPDATE baseball.leaguebaverages
SET wOBA = ((0.69)*(BB - IBB) + (0.72)*HBP + (0.89)*(H - (2B + 3B + HR)) + (1.27)*2B + (1.62)*3B + (2.10)*HR)/(AB + BB - IBB + SF + HBP),
ISO = (SLG - BA),
KP = SO/PA,
BBP = BB/PA,
BABIP = (H - HR)/(AB - SO - HR + SF)

