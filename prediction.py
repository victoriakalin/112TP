##################
#This file contains the functions needed for prediction 
#None of these function interact with the file directly
#How ever functions from processing are used
##################
import string
import numpy as np
import processing

STORE = "store"
TYPE = "type"
BRAND = "brand"
STYLE = "style"
ATTR = "attribute"


####################  Functions taken from class notes  ########################
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
    
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# Because Python prints 2d lists on one row,
# we might want to write our own function
# that prints 2d lists a bit nicer.
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")

#### Matrix Math for Regression Model ####
def getMinor(A,c,r):
    #Code modeled off of getMatrixMinor function in :
    # https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy/39881366
    return [row[:r]+row[r+1:] for row in (A[:c]+A[c+1:])]
    
import copy    
def transposeMatrix(lst):
    transList = [[row[i] for row in lst] for i in range(len(lst[0]))]
    return transList

def multiplyMatrices(A,B):
    #Multiplies matrix A by B
    colsA = len(A[0])
    rowsA = len(A)
    colsB = len(B[0])
    rowsB = len(B)
    answer = [[0 for j in range(colsB)] for i in range(rowsA)]
    if colsA != rowsB:
        print("Something went wrong")
        return 
    for i in range(rowsA):
        for j in range(colsB):
            for k in range(rowsB):
                answer[i][j] += A[i][k]*B[k][j]
    return answer

def findDet(A):
    #Recursively finds the determinant of A
    #Finding minor was modeled from:
    # https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy/39881366
    #The rest of the code was written before looking for help online
    #Though it shares similarities with:
    #Function getMatrixDeternminant(m) from same post in stackoverflow
    if len(A) == 2 and len(A[0]) == 2:
        #Base case, a 2x2 matrix
        ans =  A[0][0]*A[1][1] - A[0][1]*A[1][0]
        return ans
    else:
        result = 0 
        for i in range(len(A[0])):
            if i %2 == 0:
                #Find the sign of the term
                sign = 1
            else:
                sign = -1
            newA = copy.deepcopy(A)
            newM = getMinor(newA,0,i)
            result += (sign*A[0][i])*findDet(newM)
    return result
        
    
def findCofactor(A):
    #Returns the cofactor of a given matrix
    #Coded with mathmatical help from:
    #http://www.mathwords.com/c/cofactor_matrix.htm
    cofactor = [[0 for i in range(len(A[0]))] for i in range(len(A))]
    for r in range(len(A)):
        cofactRow = []
        for c in range(len(A[0])):
            minor = getMinor(copy.deepcopy(A),c,r)
            elem = findDet(minor)
            if (r+c) %2 == 0:
                sign = 1
            else:
                sign = -1
            cofactor[c][r] = sign*elem 
    return cofactor

def findInverse(A):
    #Returns the inverse of a given matrix
    #Coded with mathmatical help from:
    #http://www.mathwords.com/i/inverse_of_a_matrix.htm
    #under Adjoint Method Section
    inverse = [[0 for i in range(len(A[0]))] for i in range(len(A))]
    det = findDet(A)
    if det == 0:
        return
    cofactor = findCofactor(A)
    adjoint = transposeMatrix(cofactor)
    for r in range(len(adjoint)):
        for c in range(len(adjoint[0])):
            inverse[r][c] = adjoint[r][c]/det
    return inverse
    
##########Prediction From Scratch###############
def startPredScratch(year,month,information):
    stores = information[STORE]
    types = information[TYPE]
    #These two will be sets of all possible stores and types
    brand = information[BRAND]
    style = information[STYLE]
    attribute = information[ATTR]
    #These two will be the specific style and attribute and brand
    firstYear = 2013
    testYear = int(year)-firstYear
    timeSales = processing.filterDataPred2(brand,
                                       stores,types,style,attribute)
    listX, listY = processing.trans2List2(timeSales)
    xTest = processing.transTestInfo(year,month)
    prediction= runLRModelScratch(listX,listY,xTest)
    return roundHalfUp(prediction)
    
def runLRModelScratch(salesX,salesY,xTest):
    Xprime = transposeMatrix(salesX)
    productX = multiplyMatrices(Xprime,salesX)
    inverseProd = findInverse(productX)
    if inverseProd != None:
        prodInverse= multiplyMatrices(inverseProd,Xprime)
        coefficents = multiplyMatrices(prodInverse,salesY)
    else:
        #We are unable to compute with inversion
        #Must use np built-in to get pseudo inverse
        productX = np.array(productX)
        prodInverse = np.linalg.pinv(productX)
        prodInverse.tolist()
        prodInverse = multiplyMatrices(prodInverse,Xprime)
        coefficents = multiplyMatrices(prodInverse,salesY)
    intercept = coefficents[0]
    coefficents = coefficents[1:]
    testVals = [list(xTest)]
    pred = multiplyMatrices(testVals,coefficents)
    value = float(pred[0][0] + intercept)
    if value<0:
        return 0
    return value
    
##########Prebooks Predictions#############   
def getSeasonPred(year,season,information):
    #Returns a list of np arrays
    # Correspond to the sale predictions for a given shoe, year and season
    seasons = {"Spring": ["March","April","May"],"Summer":["June","July","August"],"Fall":["September","October","November"], "Winter":["December","January","February"]}
    predictions = []
    for month in seasons[season]:
        pred = startPredScratch(year,month,information)
        predictions.append(pred)
    return predictions
    
    
def preBookHelper(monthPreds,maxOrder):
    if len(monthPreds)<=1:
        return [monthPreds]
    length = len(monthPreds)
    if length %2 !=0:
        mid = len(monthPreds)//2 +1
    else:
        mid = len(monthPreds)//2
    first = monthPreds[:mid]
    last = monthPreds[mid:]
    if sum(first)<=maxOrder and sum(last)<=maxOrder:
        return [first,last]
    else: 
        return preBookHelper(first,maxOrder) + preBookHelper(last,maxOrder)
    

def preBookTimes(year,season,information):
    #Returns the minimum of orders to be made for a prebook
    #Returns a tuple of a list of the months
    # and corresponding order count for easch order 
    seasons = {"Spring": ["March","April","May"],
              "Summer":["June","July","August"],
              "Fall":["September","October","November"],
              "Winter":["December","January","February"]}
    maxOrder = 100
    predBreakdown = getSeasonPred(year,season,information)
    totalOrder = sum(predBreakdown)
    if  totalOrder <= maxOrder:
        #Order the entire needed amount in the first month
        return (seasons[season][0],totalOrder)
    else:
        orders = preBookHelper(predBreakdown, maxOrder)
        orderList = []
        for i in range(len(orders)):
            orderTot= sum(orders[i])
            orderList.append((seasons[season][i],orderTot))
        return orderList
        
################ Find yearly predictions ####################
def findYearlyPreds(yearCap,month,information):
    predictions = dict()
    currentYear = 2018
    for year in range(currentYear,int(yearCap)+1):
        yearSum = 0
        pred = startPredScratch(year, month, information)
        predictions[str(year)] = pred
    return predictions
            
  