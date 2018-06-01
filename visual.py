##################
#This file is where the user should run the program
#This contains all functions related to visualization of data
#Graph creation function and helper function are in this
##################
import userInterface

def findMaxCount(timeSales):
    #Finds the max values that will be in the graph
    max = 0 
    for time in timeSales:
        if timeSales[time] >= max:
            max = timeSales[time]
    return max
        

def createBarGraph(canvas,data,timeSales,drawMonths,lastYear = None):
    graphTop = data.height//6
    if drawMonths:
        graphBott = data.height-data.border
        options = ["January", "February", "March",
                   "April","May","June","July","August",
                   "September", "October","November", "December"]
    else:
        options = ["2013","2014","2015","2016","2017"] 
        graphBott = data.height-data.border
        if lastYear != None:
            options = options + [str(i) for i in range(2018,int(lastYear)+1)]
            graphBott = data.height-data.border*2
            keySize = 40
            canvas.create_rectangle(data.width//4,data.height- (data.border+keySize//2),
                                    data.width//4+keySize, 
                                    data.height-(data.border-keySize//2),
                                    fill = data.navy)
            canvas.create_text(data.width//4+1.5*keySize,
                               data.height- (data.border+keySize//2),
                               text = "Actual", font = data.checkFont,anchor = "nw")
            canvas.create_rectangle(data.width-data.width//2,data.height- (data.border+keySize//2),
                                    data.width-data.width//2+keySize, 
                                    data.height-(data.border-keySize//2),
                                    fill = data.pink)
            canvas.create_text(data.width-data.width//2+1.5*keySize,
                               data.height- (data.border+keySize//2),
                               text = "Predicted", font = data.checkFont,anchor = "nw")
            
    graphLeft = data.border
    graphRight = data.width - data.border
    graphHeight = graphBott-graphTop
    graphWidth = graphRight - graphLeft
    max = findMaxCount(timeSales)
    color = data.navy
    try:
        incrementY = graphHeight/max
    except: 
        incrementY = 0
    incrementX = graphWidth //len(options)
    for i in range(len(options)):
        time = options[i]
        numSales = timeSales[time] 
        if lastYear != None and int(time)>=2018:
            color = data.pink
        canvas.create_rectangle(graphLeft+i*incrementX,
                                graphBott-incrementY*numSales,
                                graphLeft+(i+1)*incrementX,
                                graphBott,fill = color)
        if drawMonths:
            canvas.create_text(graphLeft+i*incrementX,graphBott,
                            font = data.checkFont, 
                            text = time[0:3],anchor = "nw")
        else: 
            canvas.create_text(graphLeft+i*incrementX,graphBott,
                            font = data.checkFont, 
                            text = time,anchor = "nw")
    canvas.create_rectangle(graphLeft,graphTop,graphRight-5,graphBott,width = 5)
    drawUnits(canvas,max,graphLeft,graphBott, incrementY, data.checkFont)
    

def createLineGraph(canvas,data,timeSales,drawMonths,lastYear = None):
    if drawMonths:
        graphBott = data.height-data.border
        options = ["January", "February", "March",
                   "April","May","June","July","August",
                   "September", "October","November", "December"]
    else:
        #Changes options based on if this is for months or year
        options = ["2013","2014","2015","2016","2017"] 
        graphBott = data.height-data.border
        if lastYear != None:
            #If this contain predicted values
            options = options + [str(i) for i in range(2018,int(lastYear)+1)]
            #Modify options
            graphBott = data.height-data.border*2
            keySize = 40
            #Draw the predicted vs. actual key 
            canvas.create_rectangle(data.width//4,data.height- (data.border+keySize//2),
                                    data.width//4+keySize, 
                                    data.height-(data.border-keySize//2),
                                    fill = data.navy)
            canvas.create_text(data.width//4+1.5*keySize,
                               data.height- (data.border+keySize//2),
                               text = "Actual", font = data.checkFont,anchor = "nw")
            canvas.create_rectangle(data.width-data.width//2,data.height- (data.border+keySize//2),
                                    data.width-data.width//2+keySize, 
                                    data.height-(data.border-keySize//2),
                                    fill = data.pink)
            canvas.create_text(data.width-data.width//2+1.5*keySize,
                               data.height- (data.border+keySize//2),
                               text = "Predicted", font = data.checkFont,anchor = "nw")
            
    graphTop = data.height//6
    graphLeft = data.border
    graphRight = data.width - data.border
    graphHeight = graphBott-graphTop
    graphWidth = graphRight - graphLeft
    max = findMaxCount(timeSales)
    color = data.navy
    try:
        incrementY = graphHeight/max
    except: 
        incrementY = 0
    incrementX = graphWidth //len(options)
    for i in range(0,len(options)-1):
        time = options[i]
        if lastYear != None and int(time)>=2018:
            color = data.pink
        nextTime = options[i+1]
        numSales1 = timeSales[time] 
        numSales2 = timeSales[nextTime] 
        canvas.create_line(graphLeft+i*incrementX+incrementX//2,
                                graphBott-incrementY*numSales1,
                                graphLeft+(i+1)*incrementX+incrementX//2,
                                graphBott-incrementY*numSales2,
                                fill = color,width=5)
        if drawMonths:
            #Slices month to only include abbreviation
            canvas.create_text(graphLeft+i*incrementX,graphBott,
                            font = data.checkFont, 
                            text = time[0:3],anchor = "nw")
        else:
            canvas.create_text(graphLeft+i*incrementX,graphBott,
                            font = data.checkFont, 
                            text = time,anchor = "nw")
    time = options[-1]
    if drawMonths:
        canvas.create_text(graphLeft+(len(options)-1)*incrementX,graphBott,
                            font = data.checkFont, 
                            text = time[0:3],anchor = "nw")
    else:
        canvas.create_text(graphLeft+(len(options)-1)*incrementX,graphBott,
                            font = data.checkFont, 
                            text = time,anchor = "nw")
    canvas.create_rectangle(graphLeft,graphTop,graphRight,graphBott,width = 5)
    drawUnits(canvas,max,graphLeft,graphBott, incrementY, data.checkFont)                  
    
def findMaxRow(matrix):
    #Finds the largest row in a matrix
    max = 0 
    for i in range(len(matrix)):
        curSum = 0
        for j in range(len(matrix[i])):
            curSum += matrix[i][j]
        if curSum >max:
            max =curSum 
    return max
       

def drawMarginGraph(canvas,data,margMatrix,labels):
    months= ["January", "February", "March",
            "April","May","June","July","August",
            "September", "October","November", "December"]
    typeColors = [data.blue,data.pink,data.orange,data.navy,"#ff6600","#ccffcc","#ffcccc","#ccffff", "#ff6666"]
    graphTop = data.height//6
    graphBott = data.height-data.border
    graphLeft = data.border*2
    graphRight = data.width - data.border
    graphHeight = graphBott-graphTop
    graphWidth = graphRight - graphLeft
    incrementX = graphWidth/12
    maxMonth = findMaxRow(margMatrix)
    try:
        incrementY = graphHeight/maxMonth
    except:
        #if max is 0
        incrementY=0 
    for month in range(len(margMatrix)):
        monthLab = months[month]
        canvas.create_text(graphLeft+month*incrementX,graphBott,
                            font = data.checkFont, 
                            text = monthLab[0:3],anchor = "nw")
        xFirst = graphLeft + month*incrementX
        ySecond = graphBott
        for type in range(len(margMatrix[0])):
            margin = margMatrix[month][type]
            yFirst = ySecond-margin*incrementY
            fill = typeColors[type]
            canvas.create_rectangle(xFirst,yFirst,
                                    xFirst+incrementX,ySecond,
                                    fill=fill, width = 0)
            if margin != 0 :
                boxHeight = ySecond - yFirst
                text = "%.2f" %margin
                canvas.create_text(xFirst+incrementX//2,yFirst+boxHeight//2,
                                   text = text,anchor = "c")
            ySecond = yFirst
    canvas.create_rectangle(graphLeft,graphTop,graphBott,graphRight,width = 5)
    keySize = 40
    for i in range(len(labels)):
        fill = typeColors[i]
        canvas.create_rectangle(data.border//2,graphTop+i*keySize,
                                data.border//2+keySize,graphTop+(i+1)*keySize,fill = fill)
        canvas.create_text(data.border+keySize//4,graphTop+i*keySize,
                                text = labels[i], anchor = "nw",
                                font = data.checkFont)
    
def drawUnits(canvas,max,xCord,graphBott, incrementY, font):
    #Draws the units based on the max 
    #Assures the units are draws to be overlapping
    gap = 5
    if max>500:
        step = 100
    elif max>250:
        step = 25
    elif max>150:
        step = 10
    elif max > 75:
        step = 5
    elif max<=1:
        step = 1
    else:
        step = 2
    for i in range(0,max,step):
        #Draws the units of sales
        yCord = graphBott - i*incrementY
        canvas.create_text(xCord-gap,yCord,anchor = "e", 
                           text = str(i),font = font)