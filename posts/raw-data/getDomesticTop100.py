"""
Created on Tue Mar 11 13:11:08 2014; updated for python 3.6 on Apr 6, 2018
@author: stav.davis
"""

import mechanicalsoup, re, xlsxwriter

def getDomestic(filmHTML): #extracting the domestic total from specific film's url
    filmHTMLstr = str(filmHTML)
    if "Domestic Total Gross:" in filmHTMLstr:
        splitPage = filmHTMLstr.split('Domestic Total Gross:', 1)
        splitPage = splitPage[1].split('$', 1) #cut the list at the first '$' after "Domestic Total"
        splitPage = splitPage[1].split('</b></font>') #cut again after the number we need
        #print("Domestic gross: $" + splitPage[0])
        return BOstr2int(splitPage[0]) #the new [0] is what's after the first break and before the second.
    else:
        #print("Domestic total gross: N/A.")
        return "N/A"

def getForeign(filmHTML, territoryList):
    foreignDict = {}
    if "Foreign</a></li>" in filmHTML: #see if the "foreign" tab is even there
        for territoryName in territoryList:
            if (">" + territoryName + "<") in filmHTML:
                splitPage = filmHTML.split(territoryName + "<", 1)
                splitPage = splitPage[1].split('<b>', 1) #cut the list at the first bolded '$' after territory name
                splitPage = splitPage[1].split('</b></font>') #cut again after the number we need
                if (splitPage[0] == 'N/A') or (splitPage[0] == 'n/a'): #if it's a string ("N/A") - no need for BOstr2int
                    foreignDict[territoryName] = (splitPage[0])#the new [0] is what's between the two breaks - goes into the dict, with the specific territory as the key.
                else:#if it's a number (not "N/A") - we do need BOstr2int
                    foreignDict[territoryName] = BOstr2int(splitPage[0])#the new [0] is what's between the two breaks - goes into the dict, with the specific territory as the key.
            else:
                foreignDict[territoryName] = "N/A"
        #print("Foreign total gross: $" + str(foreignDict["FOREIGN TOTAL"]) + "; Breakdown by territory in exported Excel file.")
    else:
        for territoryName in territoryList:
            foreignDict[territoryName] = "N/A"
        #print("Foreign total gross: N/A. No territory breakdown exported to Excel file.")
    return foreignDict #the new [0] is what's after the first break and before the second.

def BOstr2int(BOstr): #converting the "$jj,jjj,jjj" strings from BOMojo to integers
    if BOstr == 'N/A':
        return BOstr
    else:
        BOstr2 = BOstr.replace(',', '')
        BOstr3 = BOstr2.replace('$', '')
        BOstr4 = BOstr3.replace(' (Estimate)' or ' (estimate)', '')
        return int(BOstr4)

def BOMSearchDropWord(string):#drop words with "'()" from BOMojo (eg: "We're the millers" and "The Great Gatsby (2013)"
    newString = ' '.join(word for word in string.split() if not any((char=="'" or char=="(" or char==".") for char in word))
    return newString

#################################################
searchYearInt = 2012
while searchYearInt <= 2012:    
    searchYear = str(searchYearInt)
    #################################################
    #Creating the exported Excel file: (this has to be done here, so that if it crashes it happens now):
    fileName = searchYear + "territoryBObalanceByYear.xlsx"
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet(searchYear)
    #################################################
    
    # Defining the "Browser":
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://www.boxofficemojo.com")
    browser.follow_link("yearly")
    browser.follow_link(searchYear)
    
    searchList = []  
    listOfLinks = browser.links(url_regex="/movies/")  
    for i in range(100):
        searchList.append(listOfLinks[i+1])

    titleList = []
    domesticTotalList = []
    startAtRank = 0 #zero is rank 1...
    counter1 = 1;
    for j in range(5): #this should be a list of 100 film titles
        print("Starting title #" + str(counter1) + " - " + searchList[j].text)
        print("Going to url: http://www.boxofficemojo.com" + searchList[j].attrs['href'])
        browser.open("http://www.boxofficemojo.com" + searchList[j].attrs['href'])
        filmContent = browser.get_current_page()
        domesticTotal = getDomestic(filmContent)
        print("Domestic total: " + str(domesticTotal))
        titleList.append(searchList[j].text)
        domesticTotalList.append(domesticTotal)
        print("Done with title #" + str(counter1) + " - " + searchList[j].text)
        print("***")
        counter1 += 1
        browser.open("http://www.boxofficemojo.com")
        browser.follow_link("yearly")
        browser.follow_link(searchYear)
        # browser.back() # Go back to the yearly list page to get the next movie on the list

    # #Print a status report:
    # for k in range(len(searchList[startAtRank:])-95):   #change this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #     print(k)
    #     print("Title #" + str(k+1) + ": " + titleList[k] + " - Domestic Total: $" + str(domesticTotalList[k]))
    
    #######################
    #Back to the Excel sheet that was initialized at the top of the previous block:
    #Creating formatting elements:
    centerText = workbook.add_format({'align': 'center'}) #Centered text
    centerLightBlueBG = workbook.add_format({'align': 'center', 'bg_color':'#CCFFCC','num_format':'$#,##0'})#Centered, '$#,##0', lightBlue background (for Domestic row)
    horizTitleFormat = workbook.add_format({'text_wrap':'1','align': 'center', 'bg_color':'#FFCCCC', 'border':'1'})#Horiontal titles: Wrapped, centered, border, light pink BG
    vertTitleFormat = workbook.add_format({'bg_color':'#CCFF99', 'border':'1'})#Vertical titles: light green BG, border
    centerBorderFormat = workbook.add_format({'align': 'center', 'border':'1','num_format':'$#,##0'})#Centered, border, (for territory data cells)
    topTitleFormat = workbook.add_format({'bold': 1, 'border': 1, 'align': 'center', 'bg_color': '#FF9966'})# Darker pink, center, border, bold - for the title of the whole table (top merged cell)
    boldCenterBlueFormat = workbook.add_format({'bold': 1, 'border': 1, 'align': 'center', 'bg_color':'#CCFFCC','num_format':'$#,##0'})#Bold, center, border, blue, '$#,##0'
    boldBlueBG = workbook.add_format({'bold': 1, 'border': 1,'bg_color': '#CCFFCC','num_format':'$#,##0'})#Bold, border (no center), light green BG (for Domestic Gross and Foreign Total vertical titles)
    
    worksheet.set_column('A:A', 25) #make the first column wider
    worksheet.set_column('B:QQ', 20) #make next columns wider
    
    #Vertical Excel titles:
    worksheet.write(2, 0, "Release Date", vertTitleFormat)
    worksheet.write(3, 0, "Production Budget", vertTitleFormat)
    worksheet.write(4, 0, "Domestic Gross", boldBlueBG)
    #Horizontal Excel titles:
    for j in range(len(titleList)):
        worksheet.write(1, j+1, titleList[j], horizTitleFormat) #Creating the film titles row; format: wrapped, centered, light green
    #Data for Excel:
    for z in range(len(domesticTotalList)): #entering the domestic grosses row
        worksheet.write(4, z+1, domesticTotalList[z], boldCenterBlueFormat)
    #Adding the table's title:
    worksheet.merge_range(0, 1, 0, len(titleList), searchYear + " Top 100 Films (by Domestic Gross)", topTitleFormat)#Adding the top title
    workbook.close()
    searchYearInt += 1
