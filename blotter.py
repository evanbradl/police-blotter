import urllib.request
import ssl
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import xlrd

workbook = xlrd.open_workbook('barproject.xls')
worksheet = workbook.sheet_by_name('Sheet1')

#Function returns info from iowa city arrest blotter of past 2 months in string from HTML table format
def getWebPage(url="http://www.iowa-city.org/IcgovApps/Police/ArrestBlotter"):

    global requestResult
    global resultBytes
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    requestResult = urllib.request.urlopen(url, context=context)
    resultBytes = requestResult.read()
    pageOfResults = resultBytes.decode('utf-8')
    requestResult.close()
    return pageOfResults

#Function returns dictionary in form key = bar name, value = count of tickets
def createUnderageDictWeb():
    words = getWebPage()

    dfs = pd.read_html(words)
    df = dfs[0]

    length = len(df.loc[:,'Charges'])

    j = 0
    count = 0
    barDictionary = {}
    while(j < length):
        if "In a Bar After 10 pm While Underage" in df.loc[j,'Charges']:
            count = count + 1
            if df.loc[j,'Location'] in barDictionary:
                barDictionary[df.loc[j,'Location']] = barDictionary[df.loc[j,'Location']] + 1
            else:
                barDictionary[df.loc[j,'Location']] = 1
        j = j + 1
    return barDictionary


#function takes in string name, if string is included in key function will take delete from dict and return count
def combiningNames(barName,barDictionary):
    count = 0
    keysToDelete = []
    for key, value in barDictionary.items():
        if barName in key:
            count +=  value
            keysToDelete.append(key)
    for i in keysToDelete:
        del barDictionary[i]
    return count 
    
#function takes in dictionary of bars and combines bars listed with names and bars listed with addresses, returns dictionary with combined values
def barNameCondensor(barDict):
    edenVal = combiningNames("EDEN", barDict) + combiningNames("217 IO", barDict) + combiningNames("217 E IO", barDict)

    martinisVal = combiningNames("MARTINI", barDict) + combiningNames("127 E CO", barDict) + combiningNames("127E CO", barDict)

    fieldValue = combiningNames("FIELD", barDict) + combiningNames("118 S DU", barDict) + combiningNames("22 C CL",barDict)

    summitVal = combiningNames("SUMMIT", barDict) + combiningNames("10 S CL", barDict)

    airlinerVal = combiningNames("AIRLINER", barDict) + combiningNames("22 S CL", barDict)

    spocoVal = combiningNames("SPORT", barDict) + combiningNames("12 S DU", barDict)

    unionVal = combiningNames("UNION", barDict) + combiningNames("121 E CO", barDict)

    bojamesVal = combiningNames("BO", barDict) + combiningNames("118 E WA", barDict)
    
    pintVal = combiningNames("PIN", barDict) + combiningNames("118 S CL", barDict)
    
    brotherVal = combiningNames("BRO", barDict) + combiningNames("125 S DU", barDict)
   
    dcVal = combiningNames("DC", barDict) + combiningNames("124 S DU", barDict) + combiningNames("124S DU", barDict) + combiningNames("124 D DU", barDict)
    
    deadwoodVal = combiningNames("DEAD", barDict) + combiningNames("6 S DU", barDict)
    
    bardotVal = combiningNames("BARDOT", barDict) + combiningNames("347 S GI", barDict)
    
    vineVal = combiningNames("VINE", barDict) + combiningNames("330 E PR", barDict)
    
    studioVal = combiningNames("STUDIO", barDict) + combiningNames("13 S LI", barDict)
    
    saloonVal = combiningNames("SALOON", barDict) + combiningNames("112 E CO", barDict)
    
    gabeVal = combiningNames("GABE", barDict) + combiningNames("330 E WA", barDict)
    
    vanbVal = combiningNames("VAN", barDict) + combiningNames("505 E WA", barDict)

    bluemooseVal = combiningNames("BLUE", barDict) + combiningNames("211 IO", barDict)

    barDict["FIELDHOUSE"] = fieldValue
    barDict["SUMMIT"] = summitVal
    barDict["AIRLINER"] = airlinerVal
    barDict["SPOCO"] = spocoVal
    barDict["UNION"] = unionVal
    barDict["BO JAMES"] = bojamesVal
    barDict["EDEN"] = edenVal
    barDict["MARTINIS"] = martinisVal
    barDict["PINTS"] = pintVal
    barDict["BROTHERS"] = brotherVal
    barDict["DC's"] = dcVal
    barDict["DEADWOOD"] = deadwoodVal
    barDict["BARDOT"] = bardotVal
    barDict["THE VINE"] = vineVal
    barDict["STUDIO 13"] = studioVal
    barDict["SALOON"] = saloonVal
    barDict["GABE'S"] = gabeVal
    barDict["VAN B'S"] = vanbVal
    barDict["BLUE MOOSE"] = bluemooseVal
    
    return barDict

#function takes in barDict (key = barName value = num of tickets) and returns 2 lists to be graphed
def toList(barDict):
    keyList = []
    valueList = []
    for key, value in barDict.items():
        if not(value == 0): #doesn't include items with no tickets in graph
            keyList.append(key)
            valueList.append(value)
    return keyList, valueList



#puts data from web blotter into bar graph and prints to console
def graphWebData():
    
    barDictionary = createUnderageDictWeb()
    condensedDict = barNameCondensor(barDictionary)

    print(condensedDict)
    
    keyList, valueList = toList(condensedDict)

    y_pos = np.arange(len(keyList))

    plt.barh(y_pos, valueList, align='center', alpha=0.5)
    plt.yticks(y_pos, keyList)
    plt.xlabel('Tickets')
    plt.title('Tickets given in IC bars past 2 months') #still need to use get date fct. and take 2 months off to display dates

    plt.show()




barDict2 = {}
rowIndex = 2
columnIndex = 4
totalTix = 0
while(not(worksheet.cell(rowIndex, 0).value == 1)):
    if(worksheet.cell(rowIndex, columnIndex).value == 'UNDER 21 IN BAR AFTER 10 PM'):
        if worksheet.cell(rowIndex, columnIndex-1).value in barDict2:
            barDict2[worksheet.cell(rowIndex, columnIndex-1).value] = barDict2[worksheet.cell(rowIndex, columnIndex-1).value] + 1
            #print(worksheet.cell(rowIndex, columnIndex).value)
        else:
            barDict2[worksheet.cell(rowIndex, columnIndex-1).value] = 1
            
        totalTix = totalTix + 1
            
    rowIndex = rowIndex + 1
    
print(barDict2)
condensed = barNameCondensor(barDict2)
print(condensed)
print(totalTix)
keyList, valueList = toList(condensed)

y_pos = np.arange(len(keyList))

plt.barh(y_pos, valueList, align='center', alpha=0.5)
plt.yticks(y_pos, keyList)
plt.xlabel('Tickets')
plt.title('Tickets given in IC bars past 5 years') #still need to use get date fct. and take 2 months off to display dates

plt.show()
'''
def combiningNamesAgain(barName):
    index = 0
    keysToDelete = []
    for key, value in barDict2.items():
        if barName in key:
            index +=  value
            keysToDelete.append(key)
    for i in keysToDelete:
        del barDict2[i]
    return index 

#google address and do it that way
summitVal = combiningNamesAgain('10 S CLINTON ST')

dcVal = combiningNamesAgain('124 S DUBUQUE ST')

martinisVal = combiningNamesAgain('127 E COLLEGE ST') + combiningNamesAgain('127E COLLEGE ST')

unionVal = combiningNamesAgain('121 E COLLEGE ST') + combiningNamesAgain('121 E COLLEGE') + combiningNamesAgain('125 S DUBUQUE ST')

edenVal = combiningNamesAgain('12 S DUBUQUE ST')

fieldValue = combiningNamesAgain("FIELD")

airlinerVal = combiningNamesAgain("AIRLINER")

spocoVal = combiningNamesAgain("SPORT")

bojamesVal = combiningNamesAgain("BO") + combiningNamesAgain("118 E WASHINGT")


barDictionary["FIELDHOUSE"] = fieldValue
barDictionary["SUMMIT"] = summitVal
barDictionary["AIRLINER"] = airlinerVal
barDictionary["SPOCO"] = spocoVal
barDictionary["UNION"] = unionVal
barDictionary["BO JAMES"] = bojamesVal
barDictionary["EDEN"] = edenVal
barDictionary["MARTINIS"] = martinisVal
barDictionary["DC'S"] = dcVal
'''

