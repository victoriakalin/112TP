##################
#This file contains the necessary function to create the user interface
#Functions related to user inputs are also in this (mousepressed and keypressed)
#The class CheckBox is also initalized in this
##################

from tkinter import *
import processing
import visual
import prediction
import web

############################################
#CheckBox Class
############################################

#Global variables for seperate check box types
STORE = "store"
TYPE = "type"
BRAND = "brand"
STYLE = "style"
ATTR = "attribute"
SEASON = "season"


class CheckBox(object):
    def __init__(self,cx,cy,size,value,text,category,height):
        self.cx= cx
        self.cy=cy
        self.size=size
        self.text=text
        self.value = value
        self.category = category
        self.isChecked = False
        self.checkFont = "verdana %s" % str(height//40)
        
    def drawCheckBox(self,canvas):
        if self.isChecked:
            fill = "Black"
        else: 
            fill = "White"
        canvas.create_rectangle(self.cx-self.size,self.cy-self.size,
                                self.cx+self.size,self.cy+self.size,
                                width = 3,fill = fill)
        canvas.create_text(self.cx+2*self.size,self.cy,
                               anchor = "w",text=self.text,font =self.checkFont)
    
    def isLegalClick(self,data):
        #Checks to make sure that this checkbox can be changed
        if data.brandsUp and (self.category == STORE or 
                              self.category == TYPE):
            return False
        if (data.information[BRAND] !="" and 
                                not self.isChecked and self.category == BRAND):
            #Only one brand can be selected
            return False
        elif (data.predSeason != None and 
                                not self.isChecked and self.category == SEASON):
            return False
        return True
            
    def isClick(self,data,event):
        #Deals with checking if a checkbox is clicked 
        #Changes check box as needed
        if (self.cx-self.size<=event.x <=self.cx+self.size and
            self.cy-self.size <= event.y <=self.cy+self.size):
            if self.isLegalClick(data):
                if self.isChecked:
                    self.isChecked = False 
                    if self.category == BRAND:
                        data.information[self.category]= ""
                    elif self.category == SEASON:
                        data.predSeason = None
                    else:
                        data.information[self.category].remove(self.value)    
                else:
                    self.isChecked = True
                    if self.category == BRAND:
                        data.information[self.category]= self.value
                    elif self.category == SEASON:
                        data.predSeason = self.value
                    else:
                        data.information[self.category].add(self.value)    
                    
############################################
#Animation framework taken from class notes
############################################
def init(data):
    processing.initData()
    data.information = {BRAND: "", TYPE: set(),STORE: set(),STYLE:"", ATTR: ""}
    data.visuYears= ["2013","2014","2015","2016","2017"]
    data.predYears = [str(2019+i) for i in range(5)]
    data.months = ["January", "February", "March",
                   "April","May","June","July","August",
                   "September", "October","November", "December"]
    data.coreBrands = (["HAV", "COB","OLU","RNB","SAN","REF"])
    data.visuYear = None
    data.predMonth = None
    data.predYear = None
    data.pred = None
    data.predSeason = None
    data.predAnalysis = None
    #All of the screens there will be
    data.screen = "welcome"
    #Always start at welcome screen
    data.largeFont = "verdana %s" % str(data.height//18)
    data.smallFont = "verdana %s" % str(data.height//30)
    data.checkFont = "verdana %s" % str(data.height//40)
    data.blue = "#00ace6"
    data.orange = "#ffa64d"
    data.navy = "#004d99"
    data.pink = "#cc0066"
    data.icon = PhotoImage(file="flipflops.gif")
    data.iconHeight = PhotoImage.width(data.icon)
    data.iconWidth = PhotoImage.height(data.icon)
    data.border = data.width//12
    data.butHeight= data.height//3
    data.webButHeight = data.height//9
    data.weButWidth = data.width //6
    data.checkBoxes = []
    data.footerSize =60
    data.brandsUp = False
    data.stylesEntered = False
    data.attrEntered = False 
    data.drawByMonths = True
    data.graphButtsUp = False
    data.webButtUp = False
    data.coreWebUp = False
    data.seasonsUp = False
    gapY = 20
    gapX = 200
    data.webPoint1 = (data.width//8,data.height//2+(5*gapY))
    data.webPoint2 = (data.width//8+200,data.height//2+(5*gapY)+50)
    data.dataCond = set([STORE,TYPE])
    data.xstartBox = data.width//6
    data.firstTitles = data.xstartBox
    data.ystartBox = data.height//4
    data.boxSize= data.width//100
    data.boxGap = 150
    data.monthSales = dict()
    data.yearlySales = dict()
    data.lastRealIndex =0
    
def initCheckBoxes(data):
    #Initializes the check boxes needed for visualize screen
    stores = list(sorted(processing.stores))
    types = list(sorted(processing.types))
    typeKey = {"WF":"Women's Flip Flops","MF":"Men's Flip Flops","KF":"Kids Flip Flops","WSA":"Women's Sandals","MSA":"Men's Sandals","KSA":"Kid's Sandals","WSH":"Women's Shoes","MSH":"Men's Shoes","KSH":"Kids Shoes"}
    storeKey = {"KOP":"King of Prussia","WG":"Willow Grove","PP":"Penns Purchase"}
    size = data.boxSize
    border = data.width//15
    xstart = data.xstartBox
    ystart= data.ystartBox
    for i in range(len(stores)):
        #Iterates over all the stores
        store = stores[i]
        check = CheckBox(xstart,ystart+(i*2*size),size,store,storeKey[store],STORE,data.height)
        data.checkBoxes.append(check)
    ystart = ystart+len(stores)*2*size + border
    for i in range(len(types)):
        #Iterates over each type
        type = types[i]
        check = CheckBox(xstart,ystart+(i*2*size),size,type,typeKey[type],TYPE,data.height)
        data.checkBoxes.append(check)
    data.xstartBox =data.width//4+1.2*data.boxGap
   
def resetCheckBoxes(data):
    for checkBox in data.checkBoxes:
        if checkBox.category not in data.dataCond:
            data.checkBoxes.remove(checkBox)

def hitBarGraph(data,event):
    return  (data.border <= event.x <= data.width//2-data.border and
            data.height//2+1.5*data.border <= event.y <=data.height-data.border)

def hitLineGraph(data,event):
    return  (data.width//2+data.border<= event.x <= data.width-data.border and
            1.5*data.border+data.height//2 <= event.y <=data.height-data.border)
            
def webClick(data,event):
    left = data.webPoint1[0]
    right =data.webPoint2[0]
    top = data.webPoint1[1]
    bottom =data.webPoint2[1] 
    return left<=event.x <=right and top <=event.y<=bottom

def webCoreClick(data,event):
    left = data.webPoint1[0]
    right =data.webPoint2[0]
    buttHeight = data.webPoint2[1]-data.webPoint1[1]
    gapY = 20
    top= data.webPoint1[1]+buttHeight + gapY
    bottom = data.webPoint1[1]+2*buttHeight+gapY
    return left<=event.x <=right and top <=event.y<=bottom
    
    
def isTopHit(data,event):
    return (data.border <= event.x <=data.width-data.border and
        data.border*2 <= event.y <= data.border*2+data.butHeight)

def isBotHit(data,event):
    return (data.border <= event.x <=data.width-data.border and
              data.border*3+data.butHeight <= event.y <=
              data.border*3+2*data.butHeight)
              
def leftHit(data,event):
    buttonHeight = 100
    buttonWidth = 150
    yOffset = 20
    top = data.height//2+yOffset
    bott= data.height//2+yOffset+buttonHeight
    right= data.width//2-data.iconWidth//3+buttonWidth
    left = data.width//2-data.iconWidth//3
    return (left <=event.x <= right and top <=event.y <=bott)
    
    
def rightHit(data,event):
    buttonHeight = 100
    buttonWidth = 150
    yOffset = 20
    xOffset = 10
    top = data.height//2+yOffset
    bott= data.height//2+yOffset+buttonHeight
    right= data.width//2+data.iconWidth//8+buttonWidth-xOffset
    left = data.width//2+data.iconWidth//8-xOffset
    return (left <=event.x <= right and top <=event.y <=bott)
    
            
def mousePressed(event, data):
    # use event.x and event.y
    if data.screen == "welcome":
        if leftHit(data,event):
            data.screen = "visualizeSel"
        elif rightHit(data,event):
             data.screen = "predictSel"
    elif data.screen == "visualizeSel":
        if isTopHit(data,event):
            data.screen= "visualizeMarg"
            initCheckBoxes(data)
        elif isBotHit(data,event):
             initCheckBoxes(data)
             data.screen="visualizeMerch"
    elif data.screen == "predictSel":
        if isTopHit(data,event):
            data.screen= "predictMonth"
            initCheckBoxes(data)
        elif isBotHit(data,event):
             initCheckBoxes(data)
             data.screen="predictPrebook"
    if data.screen == "visualizeMerch" or "predict":
        for check in data.checkBoxes:
            #Did we click a checkbox?
            check.isClick(data,event)
            clickedBrand = data.information[BRAND]
            if clickedBrand != "": 
                #Was a brand clicked?
                data.webButtUp = True
                if clickedBrand in data.coreBrands:
                    #If so, is this check box indicative of a core brand?
                    data.coreWebUp = True
            else:
                data.webButtUp = False
                data.coreWebUp = False
        if data.webButtUp and webClick(data,event):
            web.webRequestAll(data)
        if data.coreWebUp and webCoreClick(data,event):
            web.webRequestCore(data)
    if data.screen == "visualizeMerch" and data.graphButtsUp:
        if hitBarGraph(data,event):
                data.monthSales = processing.findMonthSales(data.information,
                                                    data.dataCond,data.visuYear)
                data.screen = "drawBarGraph"
        if hitLineGraph(data,event):
                data.monthSales = processing.findMonthSales(data.information,
                                                    data.dataCond,data.visuYear)
                data.screen = "drawLineGraph"
    if data.screen == "displayPredMonth":
        if hitBarGraph(data,event):
                data.yearlySales = processing.findYearlySales(data.information,
                                                              data.predMonth,
                                                              data.dataCond)
                data.lastRealIndex = len(data.yearlySales)
                yearlyPreds = prediction.findYearlyPreds(data.predYear,data.predMonth,data.information)
                data.yearlySales.update(yearlyPreds)
                data.screen = "drawBarGraph"
        if hitLineGraph(data,event):
                data.yearlySales = processing.findYearlySales(data.information,data.predMonth,
                                                              data.dataCond)
                data.lastRealIndex = len(data.yearlySales)
                yearlyPreds = prediction.findYearlyPreds(data.predYear,data.predMonth,data.information)
                data.yearlySales.update(yearlyPreds)
                data.screen = "drawLineGraph"
                

def createBoxes(data,posItems,category):
    ystart = data.ystartBox
    border = 20
    for item in posItems:
        #Iterates over each item in the possible items
        if ystart >=data.height-data.footerSize:
            data.xstartBox+=data.boxGap
            ystart=data.ystartBox 
        check = CheckBox(data.xstartBox,ystart,data.boxSize,
                         item,item,category,data.height)
        data.checkBoxes.append(check)
        ystart+=data.boxSize*2
    data.xstartBox +=data.boxGap
     
def getBrand(data):
    posBrand = processing.filterDataVisu(data.information,data.dataCond,BRAND)
    data.brandsUp = True
    createBoxes(data,posBrand,BRAND)
    data.dataCond.add(BRAND)
    
def getStyle(data):
    posStyles = processing.filterDataVisu(data.information,data.dataCond,STYLE)
    posStyles = list(sorted(posStyles))
    valueStyle = posStyles[0]
    drawDropMenu(data,posStyles,valueStyle,STYLE)
       
    
def getAttr(data):
    posAttr= processing.filterDataVisu(data.information,data.dataCond,ATTR)
    posAttr = list(sorted(posAttr))
    valueAttr = posAttr[0]
    drawDropMenu(data,posAttr,valueAttr,ATTR)
    

def getSeason(data):
    seasons = ["Spring", "Summer", "Fall", "Winter"]
    data.ystartBox = data.height//3+data.boxSize*18
    createBoxes(data,seasons,SEASON)
    data.xstartBox -=data.boxGap
    data.seasonsUp = True
    
    
def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "BackSpace":
        if data.screen == "welcome":
            return
        elif data.screen == "predictSel" or data.screen=="visualizeSel":
            init(data)
        elif data.screen == "visualizeMarg" or data.screen == "visualizeMerch":
            init(data)
            data.screen = "visualizeSel"
        elif data.screen == "disMarginVisu":
            init(data)
            data.screen = "visualizeSel"
        elif data.screen == "predictMonth" or data.screen == "predictPrebook":
            print(data.screen)
            init(data)
            data.screen = "predictSel"
        elif data.screen == "displayPredMonth":
            init(data)
            data.screen = "predictMonth"
            initCheckBoxes(data)
        elif data.screen == "displayPredPre":
            init(data)
            data.screen = "predictPrebook"
            initCheckBoxes(data)
        elif data.screen == "drawLineGraph" or data.screen == "drawBarGraph":
            if data.drawByMonths:
                init(data)
                data.screen = "visualizeMerch"
                initCheckBoxes(data)
            else:
                init(data)
                data.screen = "predictSel"
    elif event.keysym == "Return":
        if (data.screen == "visualizeMerch" or 
           data.screen== "predictMonth" or 
           data.screen == "predictPrebook"):
            if not data.brandsUp:
                getBrand(data)
            elif not data.stylesEntered:
                getStyle(data)
            elif not data.attrEntered: 
                getAttr(data)
            elif data.screen == "visualizeMerch" and data.visuYear == None:
                drawYearMenu(data,data.visuYears,data.visuYears[0])
            elif ((data.screen == "predictMonth" or 
                  data.screen == "predictPrebook") and 
                  data.predYear == None):
                drawYearMenu(data,data.predYears,data.predYears[0],pred = True)
            elif data.screen == "predictPrebook" and data.predSeason == None:
                getSeason(data)
            elif data.screen == "predictMonth" and data.predMonth==None:
                drawMonthMenu(data,data.months,data.months[0])
            elif data.screen == "predictPrebook" and data.predSeason != None:
                orders = prediction.preBookTimes(data.predYear,data.predSeason,data.information)
                data.pred = orders
                data.screen = "displayPredPre"
        elif data.screen == "visualizeMarg":
            if data.visuYear == None:
                drawYearMenu(data,data.visuYears,data.visuYears[0])
            else:
                data.screen = "disMarginVisu"
            
                                         
def timerFired(data):
    pass

def drawWebButt(data,canvas):
    gapY = 20
    gapX = 200
    canvas.create_text(data.width//8,data.height//2+(4*gapY),
                       text = "Want a refresher?", 
                       font = data.checkFont,anchor = "w")
    canvas.create_rectangle(data.webPoint1,
                            data.webPoint2, 
                            fill = data.navy)
    CX = data.webPoint1[0]+(data.webPoint2[0]-data.webPoint1[0])//2
    CY = data.webPoint1[1]+(data.webPoint2[1]-data.webPoint1[1])//2
    canvas.create_text(CX,CY,
                       text = "Click here for the\nbrand website!",
                       font = data.checkFont,fill="white")

def drawCoreWeb(data,canvas):
    buttHeight = data.webPoint2[1]-data.webPoint1[1]
    buttWidth = data.webPoint2[0]-data.webPoint1[0]
    gapY = 20
    point1 = (data.webPoint1[0],data.webPoint1[1]+buttHeight + gapY)
    point2 = (data.webPoint2[0],data.webPoint1[1]+2*buttHeight+gapY)
    canvas.create_rectangle(point1,point2,fill = data.navy)
    CX = point1[0]+buttWidth//2
    CY = point1[1]+(buttHeight//2)
    canvas.create_text(CX,CY,
                       text = "Click here for the\ncore brand info!",
                       font = data.checkFont, anchor = "c",fill="white")
    

def drawHeader(canvas,data,bigText,  smallText):
    #Draws the header with given text
    diffRatio = 12
    topGap = 20
    canvas.create_text(data.width//2, topGap, text = bigText,
                        anchor = "n", font= data.largeFont)
    canvas.create_text(data.width//2, data.height//diffRatio+topGap, 
                        text = smallText, anchor = "n",
                        font = data.smallFont)
    canvas.create_rectangle(0,0,data.width,topGap*1.25,fill = data.blue,width=0)
    canvas.create_rectangle(0,data.height//diffRatio,data.width,data.height//diffRatio+topGap*1,fill = data.orange,width=0)

def drawFooter(canvas,data,text):
    #Draws a footer with given text
    canvas.create_text(data.width//2, data.height, text = text,
                        anchor = "s", font= data.smallFont)
                            
    
def redrawWelc(canvas,data):
    diffRatio = 13
    drawHeader(canvas,data,"Welcome to DataPro","Select your tool below")
    butHeight = data.butHeight
    canvas.create_image(data.width//2,data.height//2+data.height//diffRatio, image=data.icon,anchor = "c")
    buttonHeight = 100
    buttonWidth = 150
    yOffset = 20
    xOffset = 10
    canvas.create_rectangle(data.width//2-data.iconWidth//3,data.height//2+yOffset,
                            data.width//2-data.iconWidth//3+buttonWidth,
                            data.height//2+yOffset+buttonHeight,
                            fill = "white",width=0)
    canvas.create_rectangle(data.width//2+data.iconWidth//8-xOffset,
                            data.height//2+yOffset,
                            data.width//2+data.iconWidth//8+buttonWidth-xOffset,
                            data.height//2+yOffset+buttonHeight,
                            fill ="white", width=0)
    leftBoxCX = data.width//2-data.iconWidth//3 + buttonWidth//2
    leftBoxCY = data.height//2+yOffset +buttonHeight//2
    rightBoxCX = data.width//2+data.iconWidth//8-xOffset + buttonWidth//2
    rightBoxCY= data.height//2+yOffset + buttonHeight//2
    
    canvas.create_text(leftBoxCX,leftBoxCY, text = "Visualize",font = data.smallFont)
    canvas.create_text(rightBoxCX,rightBoxCY, text = "Predict",font = data.smallFont)
    
  
def redrawVisuSel(canvas,data):
    drawHeader(canvas,data,"Select a Method","Choose to explore your Margins or Merchandise")
    drawFooter(canvas,data,"Press backspace to leave page")
    butHeight = data.butHeight
    canvas.create_rectangle(data.border, data.border*2,
                            data.width-data.border, data.border*2+butHeight,
                            fill = data.navy)
    canvas.create_rectangle(data.border, data.border*3+butHeight,
                            data.width-data.border,data.border*3+2*butHeight,
                            fill = data.navy)
    canvas.create_text(data.width//2,data.height//2-butHeight//2,
                        text = "Margins", font = data.largeFont,
                        fill = "White", anchor = "c")
    canvas.create_text(data.width//2,data.height-butHeight//2-data.border,
                        text = "Merchandise", font = data.largeFont,
                        fill = "White", anchor = "c")
    
def redrawPredSel(canvas,data):
    drawHeader(canvas,data,"Select a Prediction Tool","Choose to predict by months or prebooks")
    drawFooter(canvas,data,"Press backspace to leave page")
    butHeight = data.butHeight
    canvas.create_rectangle(data.border, data.border*2,
                            data.width-data.border, data.border*2+butHeight,
                            fill = data.navy)
    canvas.create_rectangle(data.border, data.border*3+butHeight,
                            data.width-data.border,data.border*3+2*butHeight,
                            fill = data.navy)
    canvas.create_text(data.width//2,data.height//2-butHeight//2,
                        text = "Predict by Month", font = data.largeFont,
                        fill = "White", anchor = "c")
    canvas.create_text(data.width//2,data.height-butHeight//2-data.border,
                        text = "Prebook Tool", font = data.largeFont,
                        fill = "White", anchor = "c")
                        
def drawCheckHeaders(canvas,data):
    canvas.create_text(data.firstTitles,data.height//4-data.boxSize*2,text="Stores",
                       font = data.smallFont, anchor = "s")
    canvas.create_text(data.firstTitles,data.height//4+data.boxSize*6,text="Types",
                       font = data.smallFont, anchor = "n")
    if data.brandsUp:
        canvas.create_text(data.xstartBox-data.boxGap+data.boxSize,
                           data.height//4-data.boxSize*2,text="Brands",
                        font = data.smallFont, anchor = "s")
    
def drawCheckboxes(canvas,data):
    for i in range(len(data.checkBoxes)):
        check = data.checkBoxes[i]
        check.drawCheckBox(canvas)
        
def drawDropMenu(data,options,value,category):
    #General Template taken from: https://www.daniweb.com/programming
    root2 = Tk()
    title = "Choose the " + category
    root2.title(title)
    canvas2 = Canvas(root2, width=200, height=900)
    canvas2.pack()
    var = StringVar(canvas2)
    var.set(value) # initial value
    menu = OptionMenu(canvas2, var, *options)
    menu.config(width = data.width//25)
    menu.pack()
    def select():
        userInput = var.get()
        data.information[category]=userInput
        data.dataCond.add(category)
        if category == STYLE:
            data.stylesEntered = True
        elif category == ATTR:
            data.attrEntered = True
        root2.destroy()
        timerFired(data)
    button = Button(root2, text="Select", command=select)
    button.pack()
    root2.mainloop()
    
def drawYearMenu(data,options, value,pred =False):
    #General Template taken from: https://www.daniweb.com/programming
    root2 = Tk()
    title = "Choose the year"
    root2.title(title)
    canvas2 = Canvas(root2, width=200, height=900)
    canvas2.pack()
    var = StringVar(canvas2)
    var.set(value) # initial value
    menu = OptionMenu(canvas2, var, *options)
    menu.config(width = data.width//25)
    menu.pack()
    def select():
        userInput = var.get()
        if not pred:
            data.visuYear=userInput
        else:
            data.predYear = userInput
        root2.destroy()
        timerFired(data)
    button = Button(root2, text="Select", command=select)
    button.pack()
    root2.mainloop()

def drawMonthMenu(data,options, value):
    #General Template taken from: https://www.daniweb.com/programming
    root2 = Tk()
    title = "Choose the month"
    root2.title(title)
    canvas2 = Canvas(root2, width=200, height=900)
    canvas2.pack()
    var = StringVar(canvas2)
    var.set(value) # initial value
    menu = OptionMenu(canvas2, var, *options)
    menu.config(width = data.width//25)
    menu.pack()
    def select():
        userInput = var.get()
        data.predMonth=userInput
        data.pred =prediction.startPredScratch(data.predYear,
                                                data.predMonth,
                                                data.information)
        data.drawByMonths = False
        brand = data.information[BRAND]
        types = data.information[TYPE]
        style = data.information[STYLE]
        attribute= data.information[ATTR] 
        data.predAnalysis =processing.revCostQuanity(data.pred,
                                                    brand,types,
                                                    style,attribute)
        data.screen = "displayPredMonth"
        root2.destroy()
        timerFired(data)
    button = Button(root2, text="Select", command=select)
    button.pack()
    root2.mainloop()
        

def drawFirstVal(canvas,data,title,value):
    canvas.create_text(data.xstartBox,data.height//4,
                       text = value,
                       font=data.checkFont,anchor = "w")
    canvas.create_text(data.xstartBox-data.boxSize,
                           data.height//4-data.boxSize*2,text=title,
                       font = data.smallFont, anchor = "sw")
                       
def drawSecondVal(canvas,data,title,value):
    heightRatio = 4
    canvas.create_text(data.xstartBox, data.height//4+data.boxSize*9,
                       text = value,
                       font=data.checkFont,anchor = "w")
    canvas.create_text(data.xstartBox-data.boxSize,
                            data.height//4+data.boxSize*7,text=title,
                        font = data.smallFont, anchor = "sw")
       
def drawThirdVal(canvas,data,title,value):
    heightRatio = 3
    canvas.create_text(data.xstartBox-data.boxSize, data.height//4+data.boxSize*15.5,
                       text = title,
                       font=data.smallFont,anchor = "sw")
    canvas.create_text(data.xstartBox,data.height//4+data.boxSize*17.5,
                       text=value, font = data.checkFont, anchor = "w")
                        
def drawFourthVal(canvas,data,title,value):
    canvas.create_text(data.xstartBox,data.height//4+data.boxSize*25,
                       text = value,
                       font=data.checkFont,anchor = "w")
    canvas.create_text(data.xstartBox-data.boxSize, data.height//4+data.boxSize*22,text=title,
                        font = data.smallFont, anchor = "w")
def redrawPredMonth(canvas,data):
    drawHeader(canvas,data,"Prediction by Month",
                "Make selections below, press Enter to move on")
    drawFooter(canvas,data,"Press backspace to leave page")
    drawCheckboxes(canvas,data)
    drawCheckHeaders(canvas,data)
    if data.stylesEntered:
        drawFirstVal(canvas,data,"Style",data.information[STYLE])
    if data.attrEntered:
        drawSecondVal(canvas,data,"Attribute",data.information[ATTR])
    if data.predYear !=None:
        drawThirdVal(canvas,data,"Year",data.predYear)
    if data.predMonth != None:
        drawFourthVal(canvas,data,"Month",data.predMonth)
    if data.webButtUp:
        drawWebButt(data,canvas)
    if data.coreWebUp:
        drawCoreWeb(data,canvas)
    
def redrawPredPre(canvas,data):
    drawHeader(canvas,data,"Prebook Tool",
                "Make selections below, press Enter to move on")
    drawFooter(canvas,data,"Press backspace to leave page")
    drawCheckboxes(canvas,data)
    drawCheckHeaders(canvas,data)
    if data.stylesEntered:
        drawFirstVal(canvas,data,"Style",data.information[STYLE])
    if data.attrEntered:
        drawSecondVal(canvas,data,"Attribute",data.information[ATTR])
    if data.predYear != None:
        drawThirdVal(canvas,data,"Year",data.predYear)
    if data.webButtUp:
        drawWebButt(data,canvas)
    if data.coreWebUp:
        drawCoreWeb(data,canvas)
    if data.seasonsUp:
        drawFourthVal(canvas,data,"Season","")
    
def drawGraphChoice(canvas,data,label1,label2):
    canvas.create_rectangle(data.border,data.height*(2/3)+1.5*data.border,data.width//2-data.border,
                            data.height-data.border,fill = data.navy)
    canvas.create_rectangle(data.width//2+data.border,1.5*data.border+data.height*(2/3),
                            data.width-data.border,data.height-data.border,
                            fill = data.navy) 
    canvas.create_text(data.border + (data.width//2-2*data.border)//2,
                                      data.height*(2/3)+2.25*data.border, 
                                      text = label1,font = data.smallFont,
                                      anchor = "c",fill="White")
    canvas.create_text(data.width-data.width//4,data.height*(2/3)+2.25*data.border, 
                       text = label2,font = data.smallFont,fill = "White",
                       anchor = "c")
    data.graphButtsUp = True
    
def redrawVisuMarg(canvas,data):
    drawHeader(canvas,data,"Percent Margin Visualization","Make selections below, press Enter to move on")
    drawFooter(canvas,data,"Press backspace to leave page")
    drawCheckboxes(canvas,data)
    drawCheckHeaders(canvas,data)
    if data.visuYear !=None:
        drawFirstVal(canvas,data,"Year",data.visuYear)
        
def redrawVisuMerch(canvas,data):
    drawHeader(canvas,data,"Merchandise Tools",
                "Make selections below, press Enter to move on")
    drawFooter(canvas,data,"Press backspace to leave page")
    drawCheckboxes(canvas,data)
    drawCheckHeaders(canvas,data)
    if data.stylesEntered:
        drawFirstVal(canvas,data,"Style",data.information[STYLE])
    if data.attrEntered:
        drawSecondVal(canvas,data,"Attribute",data.information[ATTR])
    if data.visuYear !=None:
        drawThirdVal(canvas,data,"Year",data.visuYear)
        drawGraphChoice(canvas,data,"Run Bar Graph","Run Line Graph" )
    if data.webButtUp:
        drawWebButt(data,canvas)
    if data.coreWebUp:
        drawCoreWeb(data,canvas)

def redrawBarDisplay(canvas,data):
    if data.drawByMonths:
        visual.createBarGraph(canvas,data,data.monthSales,data.drawByMonths)
        title = "Monthly Sales"
        subTitle = "for %s in %s" %(data.information[STYLE], 
                                    data.information[ATTR])
        drawHeader(canvas,data,title,subTitle)
    else:
        visual.createBarGraph(canvas,data,data.yearlySales,data.drawByMonths,data.predYear)
        title = "%s Sales by Year" % data.predMonth
        subTitle = "for %s in %s" %(data.information[STYLE], 
                                    data.information[ATTR])
        drawHeader(canvas,data,title,subTitle)
        
def redrawLineDisplay(canvas,data):
    if data.drawByMonths:
        visual.createLineGraph(canvas,data,data.monthSales,data.drawByMonths)
        title = "Monthly Sales"
        subTitle = "for %s in %s" %(data.information[STYLE], 
                                        data.information[ATTR])
        drawHeader(canvas,data,title,subTitle)
    else:
        title = "%s Sales by Year" % data.predMonth
        subTitle = "for %s in %s" %(data.information[STYLE], 
                                    data.information[ATTR])
        drawHeader(canvas,data,title,subTitle)
        visual.createLineGraph(canvas,data,data.yearlySales,data.drawByMonths,data.predYear)

def redrawDisPredMonth(canvas,data,pred,information):
    style = information[STYLE]
    attribute = information[ATTR]
    stores = ""
    for store in information[STORE]:
        stores+=store
        stores+=" and "
    stores = stores[0:len(stores)-5]
    subTitle  = "For %s in %s at %s" % (style, attribute,stores)
    title = "%s Prediction Result for %s" %(data.predMonth, data.predYear)
    drawHeader(canvas,data,title,subTitle)
    drawFooter(canvas,data,"Press backspace to leave page")
    values = [data.pred] + list(data.predAnalysis)
    labels = ["Quantity Sold","Revenue ($)",
              "Cost of Sold ($)","Gross Margin ($)"]
    gapY = 75
    topChart = data.height//4
    leftChart = data.width//4
    canvas.create_text(data.width//2,topChart-10,text = "Values Based on Prediction",
                       anchor = "s", font = data.smallFont)
    for i in range(4):
        value = values[i]
        label  = labels[i]
        canvas.create_rectangle(leftChart,topChart+gapY*i,
                                leftChart+data.width//2,topChart+gapY*(i+1),
                                outline = "grey", width = 5)
        canvas.create_line(data.width//2,topChart+gapY*i, data.width//2,
                            topChart+gapY+gapY*i,fill = "grey",width = 5)
        canvas.create_text(leftChart+data.width//8,topChart+(gapY*i)+gapY//2,
                            text = label,font = data.checkFont)
        canvas.create_text(leftChart+data.width//8+leftChart,
                            topChart+(gapY*i)+gapY//2, 
                            text = value,font = data.checkFont)
    drawGraphChoice(canvas,data,"Run yearly \nBar Graph",
                                "Run yearly \nLine Graph") 

def redrawDisPrebook(canvas,data):
    style = data.information[STYLE]
    attribute = data.information[ATTR]
    subTitle = "%s pre-orders for %s in %s" % (data.predSeason,style,attribute) 
    drawHeader(canvas,data,"Prebook Results",subTitle)
    drawFooter(canvas,data,"Press backspace to leave page")
    i =0
    gapY = 75
    topChart = data.height//4
    leftChart = data.width//4
    canvas.create_rectangle(leftChart,topChart,
                            leftChart+data.width//2,topChart+gapY,
                            outline = "grey", width = 5, fill = "white")
    canvas.create_line(data.width//2,topChart, data.width//2, topChart+gapY,
                       fill = "grey", width = 5)
    canvas.create_text(leftChart+data.width//8,topChart+gapY//2, text = "Month", font = data.smallFont)
    canvas.create_text(leftChart+data.width//8+leftChart,topChart+gapY//2, text = "Count", font = data.smallFont)
    if len(data.pred)>2:
        for i in range(len(data.pred)):
            order = data.pred[i]
            canvas.create_rectangle(leftChart,topChart+gapY*(i+1),
                                    leftChart+data.width//2,topChart+gapY*(i+2),
                                    outline = "grey", width = 5)
            canvas.create_line(data.width//2,topChart+gapY*(i+1), data.width//2,
                               topChart+gapY+gapY*(i+1),fill = "grey",width = 5)
            canvas.create_text(leftChart+data.width//8,topChart+gapY*(1+i)+gapY//2,
                               text = order[0],font = data.checkFont)
            canvas.create_text(leftChart+data.width//8+leftChart,
                                topChart+gapY*(1+i)+gapY//2, 
                                text = str(order[1]),font = data.checkFont)
    else: 
        order=data.pred
        canvas.create_rectangle(leftChart,topChart+gapY,
                                leftChart+data.width//2,topChart+gapY*2,
                                outline = "grey", width = 5)
        canvas.create_line(data.width//2,topChart+gapY, data.width//2,
                            topChart+gapY*2,fill = "grey",width = 5)
        canvas.create_text(leftChart+data.width//8,topChart+gapY+gapY//2, 
                            text = order[0],font = data.checkFont)
        canvas.create_text(leftChart+data.width//8+leftChart,
                            topChart+gapY+gapY//2, 
                            text = str(order[1]),font = data.checkFont)
                        
    
def redrawDisMargin(canvas,data):
    matrix, labels = processing.prepMarginGraph(data.visuYear,
                                        data.information[STORE],
                                        data.information[TYPE])
    visual.drawMarginGraph(canvas,data,matrix,labels)
    title = "Percent Margins for %s" % data.visuYear
    drawHeader(canvas,data,title,"Press backspace to leave page")

def redrawAll(canvas, data):
    if data.screen == "welcome":
        redrawWelc(canvas,data)
    if data.screen == "predictMonth":
        redrawPredMonth(canvas,data)
    if data.screen == "visualizeSel":
        redrawVisuSel(canvas,data)
    if data.screen == "visualizeMarg":
        redrawVisuMarg(canvas,data)
    if data.screen == "visualizeMerch":
        redrawVisuMerch(canvas,data)
    if data.screen == "drawBarGraph":
        redrawBarDisplay(canvas,data)
    if data.screen == "drawLineGraph":
        redrawLineDisplay(canvas,data)
    if data.screen == "predictSel":
        redrawPredSel(canvas,data)
    if data.screen == "displayPredMonth":
        redrawDisPredMonth(canvas,data,data.pred, data.information)
    if data.screen == "disMarginVisu":
        redrawDisMargin(canvas,data)
    if data.screen=="predictPrebook":
        redrawPredPre(canvas,data)
    if data.screen =="displayPredPre":
        redrawDisPrebook(canvas,data)
        
    
    
                           
###########################################
# Run function taken from class notes
###########################################
def run(width=900, height=900):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()