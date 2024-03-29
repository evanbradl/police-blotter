import urllib.request
import ssl
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import xlrd
from xlwt import Workbook    
from datetime import datetime
from datetime import timedelta
import json
from urllib.parse import quote_plus
from urllib.request import urlopen
import gmaps
import requests
from bs4 import BeautifulSoup
import os




#functions returns data from police blotter in df form
def getDfFromBlotter(url="http://www.iowa-city.org/IcgovApps/Police/ArrestBlotter"):
        
    page = requests.get(url)
    sp = BeautifulSoup(page.content, 'lxml')
    tb = sp.find_all('table')[0] 
    df = pd.read_html(str(tb),encoding='utf-8', header=0)[0]
    df['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in tb.find_all('a')]
    return df


#returns birthdate of offender and officer that made arrest from police blotter, stored in href link from main police blotter page
def getBirthDateandOfficer(href):
    url = "https://www.iowa-city.org" + href
    page = requests.get(url)
    sp = BeautifulSoup(page.content, 'lxml')
    tb = sp.find(class_='inline')
    fieldList = []
    valueList = []
    for link in tb.find_all('dt'):
        fieldList.append(link.text)
    for link in tb.find_all('dd'):
        valueList.append(link.text)
    indexDOB = fieldList.index('DOB')
    birthDate = datetime.strptime(valueList[indexDOB], "%m/%d/%Y")
    
    indexOfficer = fieldList.index('Officer')
    officer = str(valueList[indexOfficer])
    return(birthDate, officer)
 



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

    barDict["FIELDHOUSE BAR"] = fieldValue
    barDict["SUMMIT"] = summitVal
    barDict["AIRLINER"] = airlinerVal
    barDict["SPOCO"] = spocoVal
    barDict["UNION BAR"] = unionVal
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

#function takes in barDict (key = barName value = num of tickets) and returns 2 lists to be graphed in ascending order
def toList(barDict):
    keyList = []
    valueList = []
    toDelete = []
    
    #otherCount = 0 #counter for items that didn't fall into other bar name category
    correctionVal = 0 # counter for where to start list after unecessary vals are removed
    #correctionKey = 0
    for key, value in barDict.items():
        if len(key) < 11: #doesn't include items where address didn't correlate with bar name
     #    keyList.append(key)
         valueList.append(value)
        #elif len(key) > 10:
         #   otherCount += 1
    #keyList.append("DNE/ OTHER")
    #valueList.append(otherCount) #adding other count value to be graphed
    valueList.sort(reverse = True)
    keyList = sorted(barDict, key=barDict.get, reverse=True)
    for item in keyList:
        if len(item) > 10:
            toDelete.append(item)
    for item in toDelete:
        keyList.remove(item)
    for x in valueList:
        if x < 1:
            correctionVal += 1
    correctionVal = len(valueList) - correctionVal
    keyList = keyList[:correctionVal]
    valueList = valueList[:correctionVal] #removes keys and vals where val was 0
    Sum = 0
    for item in valueList:
        Sum += item
    print("total charges: ",Sum)
    
    return keyList, valueList

  
def largestDateinDoc():
    #document included dates to may 6th 2019 on start
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')
    
    rowIndexSearch = 2
    largestDate = datetime.strptime('5/6/2019', "%m/%d/%Y")
    #print(largestDate)
    while(not(worksheet.cell(rowIndexSearch, 0).value == 1)):
        currentDate = (datetime(*xlrd.xldate_as_tuple(worksheet.cell(rowIndexSearch, 0).value, workbook.datemode)))
        #print(worksheet.cell(rowIndex, 0))
        if(currentDate > largestDate):
            largestDate = currentDate
            
        rowIndexSearch += 1
    return largestDate
#updates excel doc with items pulled from police blotter website
def updateExcel():
    
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')

    
    #new workbook is created
    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet1')
    
    rowIndex = 0
    
    while(not(worksheet.cell(rowIndex, 0).value == 1)):
        date = worksheet.cell(rowIndex, 0).value
        sheet1.write(rowIndex, 0, date) 
        
        name = worksheet.cell(rowIndex, 1).value
        sheet1.write(rowIndex, 1, name) 
        
        dob = worksheet.cell(rowIndex, 2).value
        sheet1.write(rowIndex, 2, dob)
        
        location = worksheet.cell(rowIndex, 3).value
        sheet1.write(rowIndex, 3, location)
        
        charge = worksheet.cell(rowIndex, 4).value
        sheet1.write(rowIndex, 4, charge)
        
        officer = worksheet.cell(rowIndex, 5).value
        sheet1.write(rowIndex, 5, officer)
        
        
        lat = worksheet.cell(rowIndex, 6).value
        long = worksheet.cell(rowIndex, 7).value
        sheet1.write(rowIndex, 6, lat)
        sheet1.write(rowIndex, 7, long)
        
   
        rowIndex += 1

    
    df = getDfFromBlotter()

    #df['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in words.find_all('a')]

    #print(df)
    largestDate = largestDateinDoc()

    length = len(df.loc[:,'Charges'])
    j = 0
    
    while(j < length):
        currentDate = datetime.strptime((df.loc[j,'Offense Date']),"%m/%d/%Y %I:%M:%S %p")
        if currentDate > largestDate:
            dateToWrite = excel_date(currentDate)
            sheet1.write(rowIndex, 0, dateToWrite)
            
            offenderName = df.loc[j,'Name']
            sheet1.write(rowIndex, 1, offenderName)
            
            location = df.loc[j,'Location']
            sheet1.write(rowIndex, 3, location)
            
            charge = df.loc[j,'Charges']
            sheet1.write(rowIndex, 4, charge)
            
            #print(str(df.loc[j,'href']))
            birthdate, officer = getBirthDateandOfficer(str(df.loc[j,'href']))
            #print(type(df.loc[j,'href']))

            excelBirthdate = excel_date(birthdate)
            sheet1.write(rowIndex, 2, excelBirthdate)
            sheet1.write(rowIndex, 5, officer)
            
            print(location, ' ', rowIndex )
            if type(location) == str:
                lat, long = geocodeBusinessName(location + ' iowa city')
                sheet1.write(rowIndex, 6, lat)
                sheet1.write(rowIndex, 7, long)
            else:
                sheet1.write(rowIndex, 6, 0)
                sheet1.write(rowIndex, 7, 0)
            
            rowIndex += 1
            
            
        j = j + 1
    sheet1.write(rowIndex, 0 , 1)
    
    largestDate = largestDateinDoc()
    
    print("Document has been updated from",largestDate, "from web")
    os.remove('barproject.xls')
    wb.save('barproject.xls')
        
    #datetime.strptime((df.loc[j,'Offense Date']),"%m/%d/%Y %H:%M:%S %p")

def excel_date(date1):
    temp = datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

#function returns dictionary from barproject.xls in form key = bar name, value = count of tickets
def barDictFromExcel():
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')

    barDict2 = {}
    rowIndex = 2
    columnIndex = 4
    totalTix = 0
    while(not(worksheet.cell(rowIndex, 0).value == 1)):
        charge = worksheet.cell(rowIndex, columnIndex).value
        if 'UNDER 21 IN BAR AFTER 10 PM' in charge or 'In a Bar After 10 pm While Underage' in charge:
            #print(datetime(*xlrd.xldate_as_tuple(worksheet.cell(rowIndex, 0).value, workbook.datemode)))
            if worksheet.cell(rowIndex, columnIndex-1).value in barDict2:
                barDict2[worksheet.cell(rowIndex, columnIndex-1).value] = barDict2[worksheet.cell(rowIndex, columnIndex-1).value] + 1
            #print(worksheet.cell(rowIndex, columnIndex).value)
            else:
                barDict2[worksheet.cell(rowIndex, columnIndex-1).value] = 1
            
            totalTix = totalTix + 1
            
        rowIndex = rowIndex + 1
    
    condensed = barNameCondensor(barDict2)
    return condensed

    
def graphTicketsGivenByOfficer(startDate='jan 1 2014',endDate='jun 28 2050'):
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')
    
    keyList = []
    valueList = []

    beginDate = datetime.strptime(startDate, '%b %d %Y')
    finalDate = datetime.strptime(endDate, '%b %d %Y')
    
    rowIndex = 2
    columnIndex = 4
        
    
    while(not(worksheet.cell(rowIndex, 0).value == 1)):
        charge = worksheet.cell(rowIndex, columnIndex).value
        if 'UNDER 21 IN BAR AFTER 10 PM' in charge or 'In a Bar After 10 pm While Underage' in charge:
            currentDate = (datetime(*xlrd.xldate_as_tuple(worksheet.cell(rowIndex, 0).value, workbook.datemode)))

            if (currentDate >= beginDate and currentDate <= finalDate):
                officer = charge = worksheet.cell(rowIndex, 5).value
                officer = officer.upper()
                if officer in keyList:
                    index = keyList.index(officer)
                    valueList[index] = valueList[index] + 1
                else:
                    keyList.append(officer)
                    valueList.append(1)
        rowIndex += 1
    del valueList[0]
    del keyList[0]

    y_pos = np.arange(len(keyList))

    plt.barh(y_pos, valueList, align='center', alpha=0.5)
    plt.yticks(y_pos, keyList)
    plt.xlabel('Tickets (data only available after 5/6/2019)')
    finalDate = datetime.strptime(endDate, '%b %d %Y')
    largestDate = largestDateinDoc()
    if(largestDate < finalDate):
        finalDate = largestDate
    endDate = finalDate.strftime("%m/%d/%Y")
    earliestPossible = datetime.strptime(startDate, '%b %d %Y')
    start = datetime.strptime('may 6 2019', '%b %d %Y')
    if(start < earliestPossible):
        start = earliestPossible
    startDate = start.strftime("%m/%d/%Y")
    plt.title('Tickets given in IC bars ' + startDate + ' to ' + endDate) #still need to use get date fct. and take 2 months off to display dates

    plt.show()

def graphUnderageByDayWeek(startDate='jan 1 2014',endDate='jun 28 2050'):
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')
    index = 0
    keyList = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    valueList = []
    beginDate = datetime.strptime(startDate, '%b %d %Y')
    finalDate = datetime.strptime(endDate, '%b %d %Y')
    
    for items in keyList:
        Sum = 0
        rowIndex = 2
        columnIndex = 4
        while(not(worksheet.cell(rowIndex, 0).value == 1)):
            currentDate = (datetime(*xlrd.xldate_as_tuple(worksheet.cell(rowIndex, 0).value, workbook.datemode)))
            if currentDate >= beginDate and currentDate <= finalDate and currentDate.weekday() == index:
                charge = worksheet.cell(rowIndex, columnIndex).value
                if 'UNDER 21 IN BAR AFTER 10 PM' in charge or 'In a Bar After 10 pm While Underage' in charge:
                    Sum += 1
            rowIndex += 1
        valueList.append(Sum)
        index += 1
    keyList.reverse()
    valueList.reverse()
    
    y_pos = np.arange(len(keyList))

    plt.barh(y_pos, valueList, align='center', alpha=0.5)
    plt.yticks(y_pos, keyList)
    plt.xlabel('Tickets'+ ' (days break at midnight so data is skewed)')
    enddatetime = datetime.strptime(endDate, '%b %d %Y')
    largestDate = largestDateinDoc()
    if(largestDate < enddatetime):
        enddatetime = largestDate
    endDate = enddatetime.strftime("%m/%d/%Y")
    earliestPossible = datetime.strptime(startDate, '%b %d %Y')
    start = datetime.strptime('jan 1 2014', '%b %d %Y')
    if(start < earliestPossible):
        start = earliestPossible
    startDate = start.strftime("%m/%d/%Y")
    plt.title('Tickets given in IC bars ' + startDate + ' to ' + endDate ) #still need to use get date fct. and take 2 months off to display dates

    plt.show()
    
def graphUnderageTimeIntervals(startDate='jan 1 2014',endDate='jun 28 2050'):
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')
    keyList = []
    valueList = []
    counter = 0
    
    startDatetime = datetime.strptime(startDate, '%b %d %Y')
    endDatetime = datetime.strptime(endDate, '%b %d %Y')
    
    startTime = datetime.strptime('10:00 pm', '%I:%M %p')
    barClose = datetime.strptime('2:00 am', '%I:%M %p')
    while startTime.time() != barClose.time():
        lowerIntervalString = startTime.strftime("%I:%M:%S %p")
        beginTime = startTime
        startTime = startTime + timedelta(minutes = 15)
        endTime = startTime
        higherIntervalString = startTime.strftime("%I:%M:%S %p")
        intervalString = lowerIntervalString + '-'+ higherIntervalString
        
        keyList.append(intervalString)
        
        rowIndex = 2
        columnIndex = 4
        
        currentCount = 0
        while(not(worksheet.cell(rowIndex, 0).value == 1)):
            charge = worksheet.cell(rowIndex, columnIndex).value
            if 'UNDER 21 IN BAR AFTER 10 PM' in charge or 'In a Bar After 10 pm While Underage' in charge:
                currentDate = (datetime(*xlrd.xldate_as_tuple(worksheet.cell(rowIndex, 0).value, workbook.datemode)))
                if(beginTime.time() > endTime.time()):
                    if (currentDate.time() >= beginTime.time() or currentDate.time() < endTime.time()) and (currentDate >= startDatetime and currentDate <= endDatetime):
                        currentCount += 1
                else:
                    if (currentDate.time() >= beginTime.time() and currentDate.time() < endTime.time()) and (currentDate >= startDatetime and currentDate <= endDatetime):
                        currentCount += 1
        
            rowIndex = rowIndex + 1
        valueList.append(currentCount)
        counter += 1
    

    
    keyList.reverse()
    valueList.reverse()
    
    y_pos = np.arange(len(keyList))

    plt.barh(y_pos, valueList, align='center', alpha=0.5)
    plt.yticks(y_pos, keyList)
    plt.xlabel('Tickets')
    enddatetime = datetime.strptime(endDate, '%b %d %Y')
    largestDate = largestDateinDoc()
    if(largestDate < enddatetime):
        enddatetime = largestDate
    endDate = enddatetime.strftime("%m/%d/%Y")
    earliestPossible = datetime.strptime(startDate, '%b %d %Y')
    start = datetime.strptime('jan 1 2014', '%b %d %Y')
    if(start < earliestPossible):
        start = earliestPossible
    startDate = start.strftime("%m/%d/%Y")
    plt.title('Tickets given in IC bars ' + startDate + ' to ' + endDate) #still need to use get date fct. and take 2 months off to display dates

    plt.show()
    
#creates dictionary of bar based on times and dates entered in string for ex. (10:05 PM, 1:00 AM, jun 5 2016, jul 6 2017) this is 10:05pm to midnight. 
def createDictFromDateandTime(startDate,endDate,begin,end):
    beginTime = datetime.strptime(begin, '%I:%M %p')
    endTime = datetime.strptime(end, '%I:%M %p')
    
    beginDate = datetime.strptime(startDate, '%b %d %Y')
    endDate = datetime.strptime(endDate, '%b %d %Y')
    
    if(beginDate > endDate):
        print("Begin date was after end date")

    elif(beginDate < datetime.strptime("jan 1 2014", '%b %d %Y')):
        print("data only goes exists after 2014")

    barDictionary = {}
    
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')

    rowIndex = 2
    columnIndex = 4
    
    while(not(worksheet.cell(rowIndex, 0).value == 1)):
        charge = worksheet.cell(rowIndex, columnIndex).value
        if 'UNDER 21 IN BAR AFTER 10 PM' in charge or 'In a Bar After 10 pm While Underage' in charge:
            currentDate = (datetime(*xlrd.xldate_as_tuple(worksheet.cell(rowIndex, 0).value, workbook.datemode)))
            
            if(beginTime.time() > endTime.time()):
                if (currentDate.time() >= beginTime.time() or currentDate.time() < endTime.time()) and (currentDate >= beginDate and currentDate <= endDate):
                    if worksheet.cell(rowIndex, columnIndex-1).value in barDictionary:
                        barDictionary[worksheet.cell(rowIndex, columnIndex-1).value] = barDictionary[worksheet.cell(rowIndex, columnIndex-1).value] + 1
                
                    else:
                        barDictionary[worksheet.cell(rowIndex, columnIndex-1).value] = 1
               # print(currentTime)
            else:
                if (currentDate.time() >= beginTime.time() and currentDate.time() < endTime.time()) and (currentDate >= beginDate and currentDate <= endDate):
                    if worksheet.cell(rowIndex, columnIndex-1).value in barDictionary:
                        barDictionary[worksheet.cell(rowIndex, columnIndex-1).value] = barDictionary[worksheet.cell(rowIndex, columnIndex-1).value] + 1
                
                    else:
                        barDictionary[worksheet.cell(rowIndex, columnIndex-1).value] = 1
                else:
                   print("time not included: ",currentDate.time())
                                      
        rowIndex = rowIndex + 1
    
    return barDictionary
    


    

def graphDataFromDateandTime(startDate='jan 1 2014',endDate='jun 28 2050',begin='10:00 pm', end='3:00 am'):
    barDictionary = createDictFromDateandTime(startDate, endDate, begin, end)
    condensedDict = barNameCondensor(barDictionary)
    
    keyList, valueList = toList(condensedDict)
    
    y_pos = np.arange(len(keyList))

    plt.barh(y_pos, valueList, align='center', alpha=0.5)
    plt.yticks(y_pos, keyList)
    plt.xlabel('Tickets')
    enddatetime = datetime.strptime(endDate, '%b %d %Y')
    largestDate = largestDateinDoc()
    if(largestDate < enddatetime):
        enddatetime = largestDate
    endDate = enddatetime.strftime("%m/%d/%Y")
    earliestPossible = datetime.strptime(startDate, '%b %d %Y')
    start = datetime.strptime('jan 1 2014', '%b %d %Y')
    if(start < earliestPossible):
        start = earliestPossible
    startDate = start.strftime("%m/%d/%Y")
    plt.title('Tickets given in IC bars ' + startDate + ' to ' + endDate + ' from ' + begin + ' to ' + end) #still need to use get date fct. and take 2 months off to display dates

    plt.show()

def geocodeAddress(addressString):
   urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
   geoURL = urlbase + quote_plus(addressString)
   geoURL = geoURL + "&key=" + 'API key'

   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   
   stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
      return (0.0, 0.0) # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
   loc = jsonResult['results'][0]['geometry']['location']
   return float(loc['lat']),float(loc['lng'])

def geocodeBusinessName(nameString):
   urlbase = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
   #https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=union%20bar&inputtype=textquery&fields=photos,formatted_address,name,opening_hours,rating&locationbias=circle:20@41.6611,-88.4698&key=AIzaSyBXqIG1nWHyk3Se73pC2p5ElF9KhHmqB7Y
   formattedName = quote_plus(nameString)
   fields = "&fields=formatted_address"
   key = "&key=" + 'API key'
   inputType = "&inputtype=textquery"
   iowaCityBias = "&locationbias=circle:10000@41.6611,-91.5302"
   url = urlbase + formattedName + inputType + fields + iowaCityBias + key

   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   
   stringResultFromGoogle = urlopen(url, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      return (0.0, 0.0) # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
   loc = jsonResult['candidates'][0]['formatted_address']
   #print (loc)
   return geocodeAddress(loc)#(float(loc['lat']),float(loc['lng']))



def createHeatMap(locations):
    fig = gmaps.figure()
    fig.add_layer(gmaps.heatmap_layer(locations))
    fig
        

    
def createHeatMapAll():
    gmaps.configure(api_key = "API key")
    locations = listOfLatLong()
    createHeatMap(locations)
    
 
def createGraphs(startDate='jan 1 2014',endDate='jun 28 2050'):
    graphDataFromDateandTime(startDate,endDate)
    graphUnderageTimeIntervals(startDate,endDate)
    graphUnderageByDayWeek(startDate,endDate)
    graphTicketsGivenByOfficer(startDate, endDate)
    
    


def listOfLatLong():
    workbook = xlrd.open_workbook('barproject.xls')
    worksheet = workbook.sheet_by_name('Sheet1')
    latLong = []

    rowIndex = 2
    while(not(worksheet.cell(rowIndex, 0).value == 1)):
        lat = worksheet.cell(rowIndex, 6).value
        long = worksheet.cell(rowIndex, 7).value
        if (lat > 41.62 and lat < 41.68) and (long > -91.56 and long < -91.5):
            
            if not(lat == 0):
                together = (lat, long)
                latLong.append(together)
          
            
        rowIndex += 1
    #print(largeLat, " ", smallLat, " ", largeLong, " ", smallLong)
    return latLong


#!!! FOLLOWING FUNCTIONS ARE FOR GRAPHING LATEST 2 MONTHS OF POLICE ACTIVITY, NO EXCEL DOC IS NEEDED

    
    
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

#puts data from web blotter into bar graph and prints to console
def graphWebData():
    
    barDictionary = createUnderageDictWeb()
    condensedDict = barNameCondensor(barDictionary)

    #print(condensedDict)
    
    keyList, valueList = toList(condensedDict)

    y_pos = np.arange(len(keyList))

    plt.barh(y_pos, valueList, align='center', alpha=0.5)
    plt.yticks(y_pos, keyList)
    plt.xlabel('Tickets')
    plt.title('Tickets given in IC bars past 2 months') #still need to use get date fct. and take 2 months off to display dates

    plt.show()