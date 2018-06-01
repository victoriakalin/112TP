##################
#This interacts with the file directly
#These functions are focused on retreiving data from the file, based on conditions
#Some functions are geared more toward transformations
##################
import csv 
import os

####################  Function taken from class notes  ########################
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
###############################################################################

types = set()
brands = set()
stores = set()
styles = set()

indexes = { "store":0,
            "year": 1,
            "monthNum":2,
            "month":3,
            "type" :4,
            "brand":5,
            "style":6,
            "attribute":7
             }

noType = {"ACC","DON","GIF","JWK","JWL","JWl","SG","SUN"}
noBrands = {"FLJ","SAK","CUS","FIT","FF","HTS","TEL","DOD","SCO","OCM","UND","PUR","BIRK","SUN"}

def initData():
    months = {}
    #Goes through the data from the file and catches it in a directory
    file = "flipflopData.csv"
    with open(file, newline='') as file:
        fileReader = csv.reader(file)
        for s in list(fileReader)[1:]:
            if s[indexes["type"]] not in noType:
                types.add(s[indexes["type"]])
            stores.add(s[indexes["store"]])
            brands.add(s[indexes["brand"]])
            styles.add(s[indexes["style"]])

def findIndex(key):
    #Returns the index of the key from the data
    return indexes[key]
 
def meetsConditions(sale,conditionDir,conditions):
    #Returns true if the sale meets all the conditions in the set conditions
    #Value of conditions are in the conditionDir
    for condition in conditions:
        conditionIndex = findIndex(condition)
        requirment = conditionDir[condition]
        if isinstance(requirment,str):
            #The requirment is a string
            if sale[conditionIndex] != requirment:
                #Therefore the requirment must equal the value of the sale 
                return False
        else:
            #The requirment is a set of possible values
            if sale[conditionIndex] not in conditionDir[condition]:
                #The requirment must be in the set
                return False
    return True
    
def filterDataVisu(checkedDir,conditions,key):
    #Filters the data based on given number of conditions
    posItems = set()
    keyIndex = findIndex(key)
    file = "flipflopData.csv"
    with open(file, newline='') as file:
        fileReader = csv.reader(file)
        for s in list(fileReader)[1:]:
            if meetsConditions(s,checkedDir,conditions):
                if (not s[indexes["type"]] in noType and 
                   not s[indexes["brand"]] in noBrands):
                    posItems.add(s[keyIndex])
    return posItems
    
def findDataHelper(conditionDir,sale):
    #Returns true is all conditions in conditionDir are met
    for condition in conditionDir:
        if sale[findIndex(condition)] not in conditionDir[condition]:
            return False
    return True
    
def findMonthSales(conditionDir,conditions,year):
    monthsCount = {"January": 0, "February":0 , "March":0,
                   "April":0,"May":0,"June":0,"July":0,"August":0,
                   "September":0, "October":0,"November":0, "December":0}
    #Goes through the data from the file and catches it in a directory
    file = "flipflopData.csv"
    with open(file, newline='') as file:
        fileReader = csv.reader(file)
        for s in list(fileReader)[1:]:
            month = s[3]
            if findDataHelper(conditionDir,s) and s[1]==str(year):
                monthsCount[month] = 1 + monthsCount.get(month,0)
    return monthsCount
    
def findYearlySales(conditionDir, month, conditions):
    #Finds the yearly sales for a given month and product
    file = "flipflopData.csv"
    yearCount = {"2013":0,"2014":0,"2015":0,"2016":0,"2017":0} 
    with open(file, newline='') as file:
        fileReader = csv.reader(file)
        for s in list(fileReader)[1:]:
            year = s[indexes["year"]]
            if findDataHelper(conditionDir,s) and s[indexes["month"]] == month:
                yearCount[year] = 1 + yearCount.get(year,0)
    return yearCount

def findDumSeason(month):
    #For modeleing based on season
    #Less variables, therefore less estimateion error
    seasons = {"Spring": ["March","April","May"],
              "Summer":["June","July","August"],
              "Fall":["September","October","November"],
              "Winter":["December","January","February"]}
    thisSeas = ""
    for season in seasons:
        if month in seasons[season]:
            thisSeas = season
    dummies = [0,0,0,0]
    seasons = ["Winter","Spring","Summer","Fall"]
    dummies[seasons.index(thisSeas)] = 1
    return dummies
    
def findDumMonth(month):
    #For modeling based on month 
    #More specifica, however increased error
    # Due to the increase in estimated coefficents
    dummies = [ 0 for  i in range(12)]
    months = ["January", "February" , "March",
                   "April","May","June","July","August",
                   "September", "October","November", "December"]
    dummies[months.index(month)] = 1
    return dummies
    
    
def filterDataPred2(brand,stores,types,style,attribute):
    #Filter data for the prediction by scratch
    timeSales = {}
    firstYear = 2013
    #Goes through the data from the file and catches it in a directory
    file = "flipflopData.csv"
    with open(file, newline='') as file:
        fileReader = csv.reader(file)
        for s in list(fileReader)[1:]:
            if (s[indexes["store"]] in stores and 
                s[indexes["type"]] in types and
                s[indexes["brand"]] == brand and
                s[indexes["style"]]==style and 
                s[indexes["attribute"]]==attribute):
                year =int(s[indexes["year"]])
                month = s[indexes["month"]]
                yearsIn = year - firstYear
                row = (1,yearsIn)
                monthDums = findDumSeason(month)
                row += tuple(monthDums)
                timeSales[row] = 1 + timeSales.get(row,0)
    return timeSales
    
def trimByYearStore(year,stores):
    #Goes through the data from the file and catches it in a directory
    file = "flipflopData.csv"
    newData = []
    with open(file, newline='') as file:
        fileReader = csv.reader(file)
        for s in list(fileReader)[1:]:
            if s[indexes["year"]]==year and s[indexes["store"]] in stores:
                newData.append(s)
    return newData
    
def findAveTypeMarg(data,types):
    #Finds the average margin of a type for a each month
    #Done for a given year
    sumInd = 0
    countInd = 1
    margInd = 14
    allData = dict()
    for type in types:
        sumMonth = [0 for i in range(12)]
        sumType = [0 for i in range(12)]
        allData[type] = (sumMonth,sumType)
    for sale in data:
        type = sale[indexes["type"]]
        if type in allData:
            monthInd = int(sale[indexes["monthNum"]])-1
            #Gives backs the index in the list of the month
            #Starting with january = 0
            margin = sale[margInd]
            tupInfo = allData[type]
            tupInfo[sumInd][monthInd] +=float(margin)
            tupInfo[countInd][monthInd]+=1
    typeList = [type for  type in types]
    aveMargMatrix = [[0 for i in range(len(typeList))] for i in range(12)]
    for m in range(12):
        for t in range(len(typeList)):
            type = typeList[t]
            try:
                aveMargin = allData[type][sumInd][m] / allData[type][countInd][m]
                aveMargin = abs(aveMargin)
            except:
                aveMargin = 0
            aveMargMatrix[m][t] = aveMargin
    return (aveMargMatrix,typeList)

def prepMarginGraph(year,stores,types):
    #Returns a matrix of average margins for each given type in each month
    #All for a specified year
    data = trimByYearStore(year,stores)
    (matrix, labels) = findAveTypeMarg(data,types)
    return (matrix,labels)
                
def trans2List(data):
    #Returns data transformed into a list from a directory
    listX = []
    listY = []
    for elem in data:
        salesCount = data[elem]
        newTime = [elem[0],elem[1]]
        listX.append(newTime)
        listY.append([salesCount])
    return (listX, listY)
  
def trans2List2(data):
    #Returns data transformed into a list with the keys as the Y values
    listX = []
    listY = []
    for elem in data:
        salesCount = data[elem]
        newTime = list(elem)
        listX.append(newTime)
        listY.append([salesCount])
    return listX,listY
    
def findCostRevenue(brand,types,style,attribute):
    #Returns a tuple of the integer Cost and Price of an item
    #Returns most recent price and cost
    file = "flipflopData.csv"
    revIndex = 11
    costIndex = 12
    with open(file, newline='') as file:
        fileReader = csv.reader(file)
        for s in list(fileReader)[:0:-1]:
            #Iterates backwards through the data
            #In order to find msot recent
            if (s[indexes["type"]] in types and
                s[indexes["brand"]] == brand and
                s[indexes["style"]]==style and 
                s[indexes["attribute"]]==attribute):
                cost = float(s[costIndex])
                sellPrice = float(s[revIndex])
                return (cost,sellPrice)
                
def revCostQuanity(numSold,brand,types,style,attribute):
    #Returns the revenue, and cost of quantity sold
    #Also returns the grossMargin
    #All based on am amount  sold 
    cost, price = findCostRevenue(brand,types,style,attribute)
    price = abs(price)
    cost = abs(cost)
    CoGS = cost*numSold
    CoGS = roundHalfUp(CoGS) 
    quantRev = price*numSold
    quantRev = roundHalfUp(quantRev)
    grossMarg = roundHalfUp(quantRev - CoGS)
    return (quantRev,CoGS,grossMarg)


def transTestInfo(year,month):
    #Transforms the test data for the of model
    #Transforms the data for the thing we want to predict 
    firstYear = 2013
    yearsIn = int(year) - firstYear
    monthDums = findDumSeason(month)
    monthDums.insert(0,yearsIn)
    test = tuple(monthDums)
    return test
    

