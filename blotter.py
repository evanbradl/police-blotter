import urllib.request
import ssl
import pandas as pd
#import io
from zipfile import ZipFile
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import xlrd

workbook = xlrd.open_workbook('barproject.xls')
worksheet = workbook.sheet_by_name('Sheet1')

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

words = getWebPage()
dfs = pd.read_html(words)
df = dfs[0]
#print(df)
length = len(df.loc[:,'Charges'])
#print(df.loc[:,'Charges'])
#print(length)
j = 0
count = 0
barDictionary = {}
while(j < length):
    #print(df.loc[j,'Charges'])
    #print(df.loc[j,'Name'])
    if "In a Bar After 10 pm While Underage" in df.loc[j,'Charges']:
        count = count + 1
        #print(df.loc[j,'Charges'] + " " + df.loc[j,'Name']+ " " + df.loc[j,'Location'])
        if df.loc[j,'Location'] in barDictionary:
            barDictionary[df.loc[j,'Location']] = barDictionary[df.loc[j,'Location']] + 1
        else:
            barDictionary[df.loc[j,'Location']] = 1
        #print()
    j = j + 1


def combiningNames(barName):
    index = 0
    keysToDelete = []
    for key, value in barDictionary.items():
        if barName in key:
            index +=  value
            keysToDelete.append(key)
    for i in keysToDelete:
        del barDictionary[i]
    return index 
    

edenVal = combiningNames("EDEN")

martinisVal = combiningNames("MARTINI")

fieldValue = combiningNames("FIELD")

summitVal = combiningNames("SUMMIT") + combiningNames("10 S CLINTON")

airlinerVal = combiningNames("AIRLINER")

spocoVal = combiningNames("SPORT")

unionVal = combiningNames("UNION")

bojamesVal = combiningNames("BO") + combiningNames("118 E WASHINGT")


barDictionary["FIELDHOUSE"] = fieldValue
barDictionary["SUMMIT"] = summitVal
barDictionary["AIRLINER"] = airlinerVal
barDictionary["SPOCO"] = spocoVal
barDictionary["UNION"] = unionVal
barDictionary["BO JAMES"] = bojamesVal
barDictionary["EDEN"] = edenVal
barDictionary["MARTINIS"] = martinisVal

#for item in keysToDelete:
 #   del barDictionary[item]
  #  print(item)

print(barDictionary)

keyList = []
valueList = []
for key, value in barDictionary.items():
    keyList.append(key)
    valueList.append(value)






y_pos = np.arange(len(keyList))

plt.barh(y_pos, valueList, align='center', alpha=0.5)
plt.yticks(y_pos, keyList)
plt.xlabel('Hits')
plt.title('Tickets given in IC bars past 2 months')

plt.show()

barDict2 = {}
rowIndex = 2
columnIndex = 4
totalTix = 0
while(not(worksheet.cell(rowIndex, 0).value == 1)):
    if(worksheet.cell(rowIndex, columnIndex).value == 'UNDER 21 IN BAR AFTER 10 PM'):
        if worksheet.cell(rowIndex, columnIndex-1).value in barDict2:
            barDict2[worksheet.cell(rowIndex, columnIndex-1).value] = barDict2[worksheet.cell(rowIndex, columnIndex-1).value] + 1
            print(worksheet.cell(rowIndex, columnIndex).value)
        else:
            barDict2[worksheet.cell(rowIndex, columnIndex-1).value] = 1
            
        totalTix = totalTix + 1
            
    rowIndex = rowIndex + 1
    
print(barDict2)
print(totalTix)
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


#print(dfs[0])
#print(words)
#print(type(words))
#from BeautifulSoup import BeautifulSoup, Comment
#pd.read_html('http://www.iowa-city.org/IcgovApps/Police/ArrestBlotter)', header=0)[1]