#################
#This file handles web requests
# And helper functions relating to web requests
#################
import webbrowser
import ssl


STORE = "store"
TYPE = "type"
BRAND = "brand"
STYLE = "style"
ATTR = "attribute"
SEASON = "season"

coreBrands = {"COB": "cobian", "HAV": "havaianas","REF":"reef",
                "OLU":"olukai","RNB":"rainbow","SAN":"sanuk"}

def findBrandUrl(brand):
    cores = {"COB": "cobianusa", "HAV": "havaianas","REF":"reef",
                "OLU":"olukai","RNB":"rainbow","SAN":"sanuk",
                "EDC":"everydaycalifornia","UA":"underarmour",
                "CHA":"chacos","ROX":"roxy","BIR":"birkenstock",
                "MIN":"minnetonka","QUI":"quiksilver","MUK":"mukluks",
                "CRO":"crocs","SPE":"speedousa"}
    core = cores.get(brand,None)
    if core != None:
        url = "http://"+core+".com"
    return url
    
    
def webRequestAll(data):
    #General template of context and .open() taken from python.org
    #https://docs.python.org/3.1/howto/urllib2.html
    brand = data.information[BRAND]
    url = findBrandUrl(brand)
    context = ssl._create_unverified_context()
    webbrowser.open(url)
    
   
def webRequestCore(data):
    #General template of context and .open() taken from python.org
    #https://docs.python.org/3.1/howto/urllib2.html
    context = ssl._create_unverified_context()
    url= "https://flipflopshops.com/"
    addOn = coreBrands[data.information[BRAND]] + "/"
    url +=addOn
    webbrowser.open(url)
    

        
    