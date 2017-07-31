import numpy as np
import scipy as sp
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge, LinearRegression
import pandas as pd
import mysql.connector
import os
import datetime as dt
from itertools import chain
import matplotlib.pyplot as plt
import constants
import warnings

def getDate(day, month, year, cursor):
    gameIDP = 0

    findGame = "SELECT iddates FROM dates WHERE date = %s"
    findGameData = (dt.date(year, month, day),)
    cursor.execute(findGame, findGameData)

    for game in cursor:
        gameIDP = game[0]

    return gameIDP

def getDates(day, month, year, numdays, cursor):
    base = dt.date(year, month, day)
    dateList = [base - dt.timedelta(days=x) for x in range(0, numdays)]

    # get date ids from database
    gameIDs = []
    for date in dateList:
        findGame = "SELECT iddates FROM dates WHERE date = %s"
        findGameData = (date,)
        cursor.execute(findGame, findGameData)

        for game in cursor:
            gameIDs.append(game[0])

    return gameIDs

def mapFeatures(X):
    '''
    MAPFEATURE Feature mapping function to polynomial features
    MAPFEATURE(X1, X2) maps the two input features
    to quadratic features used in the regularization exercise.
    Returns a new feature array with more features, comprising of
    X1, X2, X1.^2, X2.^2, X1*X2, X1*X2.^2, etc..
    Inputs X1, X2 must be the same size

    :param X:
    :return: XTransform
    '''

    degree = 4

    poly = PolynomialFeatures(degree)
    XTransform = poly.fit_transform(X)

    return XTransform

def computCostMulti(X, y, theta):
    '''
    COMPUTECOSTMULTI Compute cost for linear regression with multiple variables
    J = COMPUTECOSTMULTI(X, y, theta) computes the cost of using theta as the
    parameter for linear regression to fit the data points in X and y
    '''

    # Initialize some useful values
    m = np.shape(y)[0]

    # Cost
    h = X.dot(np.transpose(theta))
    error = (h - y)
    J = ((np.transpose(error).dot(error))/(2*m))

    return J

def featureNormalize(X):
    '''
    FEATURENORMALIZE Normalizes the features in X FEATURENORMALIZE(X) returns a normalized version of X where
    the mean value of each feature is 0 and the standard deviation is 1. This is often a good preprocessing step
    to do when working with learning algorithms. Ignores the bias feature
    '''

    X_norm = X
    mu = np.zeros((1, np.shape(X)[1]), dtype=float)
    sigma = np.zeros((1, np.shape(X)[1]), dtype=float)

    numFeatures = np.shape(X)[1]

    i = 0
    while i < numFeatures:
        feature = X[:,i]
        mu[1,i] = np.mean(feature)
        sigma[1,i] = np.std(feature)
        feature = (feature - (mu[1,i])) / (sigma[1,i])
        X_norm[:,i] = feature

        i = i + 1

    return X_norm, mu, sigma

def gradientDescentMulti(X, y, theta, alpha, numIters):
    # Initializ some useful values
    m = np.shape(y)[0]

    # number of training examples
    thetaz = np.shape(theta)[1]

    i = 0
    costHistory = []
    iterHistory = []

    previousJ = 1000000000
    optimialIteration = False
    optimalIterNumber = 0
    while i < numIters:
        h = X.dot(np.transpose(theta))
        error = (h - y)

        j = 0
        while j < thetaz:
            xColumn = X[:,j]
            partialD = np.transpose(error).dot(xColumn)
            valueSet = ((theta[0, j]) - (alpha*partialD)/m)
            theta[0, j] = valueSet
            j = j + 1

        J = computCostMulti(X, y, theta)
        if ((previousJ - J[0,0]) <= 0.001) and (not optimialIteration):
            optimalIterNumber = (i + 1)
            optimialIteration = True
            print "Optimal # of Iterations: " + str(optimalIterNumber)

        previousJ = J[0,0]
        costHistory.append(J[0,0])
        iterHistory.append(i)

        i = i + 1


    return theta, costHistory, iterHistory

if __name__ == "__main__":
    print "Loading data..."

    cnx = mysql.connector.connect(user=constants.databaseUser,
                                  host=constants.databaseHost,
                                  database=constants.databaseName,
                                  password=constants.databasePassword)
    cursor = cnx.cursor()

    # predict data
    # date to predict
    yearP = constants.yearP
    monthP = constants.monthP
    dayP = constants.dayP

    # dates to retrieve data for batter test data
    # start date
    year = constants.gdStartYear
    month = constants.gdStartMonth
    day = constants.gdStartDay

    numdays = constants.numdaysGradientDescent

    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

    gameIDs = getDates(day, month, year, numdays, cursor)

    # select data with cooresponding game id and other constraints
    batterConstraints = ['paL', 'paR']
    batterConstraintsValues = {}
    batterConstraintsTypes = {}

    for con in batterConstraints:
        var1 = raw_input("Enter operand/statement for constraint " + con + ": ")
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

    features = ['adjwOBA', 'adjBBP', 'adjBABIP', 'adjISO', 'adjOBP', 'adjSLG', 'adjKP', 'battingOrder', 'parkFactor',
                'battersdaily.wOBA', 'battersdaily.ISO', 'battersdaily.SLG', 'battersdaily.OBP', 'battersdaily.BB',
                'battersdaily.BABIP', 'battersdaily.adjSB', 'tab', 'thits', 'tsingles', 'tdoubles', 'ttriples', 'thomeruns',
                'tstolenbases', 'truns', 'trbis', 'twalks', 'terrors', 'thbp', 'tstrikeouts']
    targets = ['dkpoints']

    featuresString = ""
    for feat in features:
        featuresString = featuresString + feat
        if features[-1] != feat:
            featuresString = featuresString + ", "

    targetsString = ""
    for tar in targets:
        targetsString = targetsString + tar
        if targets[-1] != tar:
            featuresString = targetsString + ", "

    print "Loading data..."

    # constants: take into affect parkFactor being null for some data, asahd khaled, batters not having predictions b/c didn't start
    getTestData = "SELECT batterID, "
    getTestData = getTestData + featuresString
    getTestData = getTestData + ", "
    getTestData = getTestData + targetsString
    getTestData = getTestData + " FROM battersdaily LEFT JOIN batters ON battersdaily.batterID = batters.idbatters " \
                                "WHERE battersdaily.bgameID = %s AND oppPitcher != 0 AND dkPointsPred IS NOT NULL AND "
    getTestData = getTestData + constraintsString

    numpyDataArrays = []
    # execute command + load into numpy array
    for game in gameIDs:
        testVariables = (game,)
        cursor.execute(getTestData, testVariables)

        results = cursor.fetchall()
        numRows = cursor.rowcount

        D = np.fromiter(chain.from_iterable(results), dtype=float, count=-1)

        D = D.reshape(numRows, -1)
        numpyDataArrays.append(D)

    iterDataSets = iter(numpyDataArrays)
    next(iterDataSets)
    testData = numpyDataArrays[0]
    for dataArray in iterDataSets:
        testData = np.vstack((testData, dataArray))

    # split data
    numFeatures = len(features)
    batterIDs, testX = np.split(testData, [1], 1)
    testX, testY = np.split(testX, [numFeatures], 1)

    print "Number of training examples: " + str(np.shape(testX)[0])

    # add bias term
    ones = np.ones((np.shape(testX)[0], 1), dtype=float)
    testX = np.hstack((ones, testX))

    # learning rate + iterations
    alpha = 0.01
    num_iters = 1000

    # theta initialization
    theta = np.zeros(((numFeatures + 1), 1))
    theta = np.transpose(theta)

    theta, JHistory, iterHistory = gradientDescentMulti(testX, testY, theta, alpha, num_iters)

    print "Batter Theta Values from Homemade Gradient Descent"
    print theta

    reg = LinearRegression(fit_intercept=False, normalize=True)
    reg.fit(testX, testY)
    thetaSKLearn = reg.coef_

    print "Batter Theta Values from Sklearn Linear Regression"
    print thetaSKLearn

    ridge = Ridge(alpha=1, fit_intercept=False, normalize=True)
    ridge.fit(testX, testY)
    thetaSKLearnRidge = ridge.coef_

    print "Batter Theta Values from Sklearn Ridge Regression"
    print thetaSKLearnRidge

    ridgeP = Ridge(alpha=150, fit_intercept=False, normalize=True)
    newFeatures = mapFeatures(testX)
    ridgeP.fit(newFeatures, testY)
    thetaSKLearnRidgeP = ridgeP.coef_

    print "Batter Theta Values from Sklearn Ridge Regression w/ Polynomial Feature Mapping"
    print thetaSKLearnRidgeP

    gameIDP = getDate(dayP, monthP, yearP, cursor)

    # get projections

    # predict for all in battersdaily - don't project for pitchers/pinch hitters/newbies
    getPredictData = "SELECT batterID, "
    getPredictData = getPredictData + featuresString
    getPredictData = getPredictData + " FROM battersdaily LEFT JOIN batters ON battersdaily.batterID = batters.idbatters " \
                                      "WHERE battersdaily.bgameID = %s AND start = 1 AND dkSalary IS NOT NULL"

    testVariables = (gameIDP,)
    cursor.execute(getPredictData, testVariables)

    results = cursor.fetchall()
    numRows = cursor.rowcount

    D = np.fromiter(chain.from_iterable(results), dtype=float, count=-1)

    targetData = D.reshape(numRows, -1)

    # split data
    batterIDs, targetX = np.split(targetData, [1], 1)

    print "Number of targets: " + str(np.shape(targetX)[0])

    # add bias term
    ones = np.ones((np.shape(targetX)[0], 1), dtype=float)
    targetX = np.hstack((ones, targetX))

    # predict
    targetY = targetX.dot(np.transpose(theta))
    targetYSKLearn = targetX.dot(np.transpose(thetaSKLearn))
    targetYSKLearnRidge = targetX.dot(np.transpose(thetaSKLearnRidge))

    newTargetX = mapFeatures(targetX)
    targetYSKLearnRidgeP = newTargetX.dot(np.transpose(thetaSKLearnRidgeP))

    # load predictions into database

    bID = 0
    numBatters = np.shape(batterIDs)[0]
    while bID < numBatters:
        batterID = int(batterIDs[bID, 0])
        batterProjection = float(targetY[bID, 0])
        batterProjectionSKLearn = float(targetYSKLearn[bID, 0])
        batterProjectionSKLearnRidge = float(targetYSKLearnRidge[bID, 0])
        batterProjectionSKLearnRidgeP = float(targetYSKLearnRidgeP[bID, 0])

        updateBattersDKPoints = "UPDATE battersdaily SET dkPointsPred = %s, dkPointsPredSKLin = %s, dkPointsPredRidge = %s, dkPointsPredRidgeP = %s WHERE bgameID = %s AND batterID = %s"
        updateBatterDKPointsData = (batterProjection, batterProjectionSKLearn, batterProjectionSKLearnRidge, batterProjectionSKLearnRidgeP, gameIDP, batterID)
        cursor.execute(updateBattersDKPoints, updateBatterDKPointsData)

        bID = bID + 1

    print "Predicted DK Points for Batters"

    cursor.close()
    cnx.commit()
    cnx.close()

