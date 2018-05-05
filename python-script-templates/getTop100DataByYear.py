"""
Created on Tue Mar 11 13:11:08 2014
@author: stav.davis
"""

import mechanize, re, xlsxwriter

def getDomestic(filmHTML): #extracting the domestic total from specific film's url
    if "Domestic Total" in filmHTML:
        splitPage = filmHTML.split('Domestic Total', 1)
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
searchYearInt = 1990
while searchYearInt <= 2017:    
    searchYear = str(searchYearInt)
    #################################################
    #Creating the exported Excel file: (this has to be done here, so that if it crashes it happens now):
    fileName = searchYear + "territoryBObalanceByYear.xlsx"
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet(searchYear)
    #################################################
    
    # Defining the "Browser":
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False) #will get error 403 if this is true - server thinks we are robot
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    # User-Agent (this is cheating, ok?) - identifying ourselves as using Firefox
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    titleList = []
    domesticTotalList = []
    foreignTotalList = []
    territoryList = ["FOREIGN TOTAL","Argentina","Australia","Austria","Belgium","Bolivia","Brazil","Bulgaria","Chile","China",\
                    "Colombia","Croatia","Czech Republic","Denmark","East Africa","Ecuador","Egypt","Finland",\
                    "France","Germany","Greece","Hong Kong","Hungary","Iceland","India","Indonesia","Israel",\
                    "Italy","Japan","Lebanon","Malaysia","Mexico","Netherlands","New Zealand","Nigeria",\
                    "Norway","Peru","Philippines","Poland","Portugal","Russia - CIS","Serbia & Montenegro",\
                    "Singapore","Slovakia","Slovenia","South Africa (Entire Region)","South Korea","Spain",
                    "Sweden","Thailand","Turkey","Ukraine","United Arab Emirates","United Kingdom","Uruguay",\
                    "Venezuela"]
    
    #getting the list of 100 most successful films (domestically) of 2013:
    openBOMojo = br.open('http://www.boxofficemojo.com')
    clickLink = br.click_link(text="Yearly")
    br.open(clickLink)
    clickLink = br.click_link(text=searchYear)
    br.open(clickLink)
    searchList = []
    foreignGrossesDict = []
    titleList = []
    startAtRank = 0 #zero is rank 1...
    counter1 = 1
    for item in br.links():
        if (("/movies/?id=" in item.url) and ("#1 Movie" not in item.text)): #including the "?id=" eliminates the last entry: "/movies/?ref=ft", as well as just "/movies/ "
            searchList.append(item)
    
    for link in searchList[startAtRank:]: #this should be a list of 100 film titles
        clickMovieLink = br.click_link(link)
        br.open(clickMovieLink)
        filmContent = br.response().read()
        domesticTotal = getDomestic(filmContent)
        titleList.append(link.text)
        domesticTotalList.append(domesticTotal)
        #Finding foreign totals (requires "clicking" on the "foreign" tab, if it exists:
        br.find_link(text="Foreign")
        clickForeignLink = br.click_link(text="Foreign")
        br.open(clickForeignLink)
        foreignContent = br.response().read()
        foreignGrosses = getForeign(foreignContent, territoryList) #this is a dictionary of grosses - one for each territory
        foreignGrossesDict.append(foreignGrosses)
        foreignTotalList.append(foreignGrosses["FOREIGN TOTAL"]) #this is just a list of the non-US totals
        print "Done with title #" + str(counter1) + " - " + link.text
        counter1 += 1
        ### Back
        br.back() # Goes back to the film's main page
        br.back() # Go back to the yearly list page to get the next movie on the list
    
    for i in range(len(searchList[startAtRank:])):
        print "Title #" + str(i+1) + ": " + titleList[i] + " - Domestic Total: $" + str(domesticTotalList[i]) \
              + "; Foreign Total: $" + str(foreignTotalList[i])
    
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
    for i in range(len(territoryList)):
        worksheet.write(i+5, 0, territoryList[i], vertTitleFormat)#Creating the territory column
    worksheet.write(5, 0, territoryList[0], boldBlueBG) #re-enter Foreign Total title, with its different formatting
    #Horizontal Excel titles:
    for j in range(len(titleList)):
        worksheet.write(1, j+1, titleList[j], horizTitleFormat) #Creating the film titles row; format: wrapped, centered, light green
    #Data for Excel:
    ##for x in range(len(filmDatesList)): #entering the release dates row
    ##    worksheet.write(2, x+1, filmDatesList[x], centerBorderFormat)
    ##for y in range(len(filmBudgetsList)): #entering the budgets row
    ##    worksheet.write(3, y+1, filmBudgetsList[y], centerBorderFormat)
    for z in range(len(domesticTotalList)): #entering the domestic grosses row
        worksheet.write(4, z+1, domesticTotalList[z], boldCenterBlueFormat)
    for k in range(len(titleList)): #entering the territory grosses for each film
        for m in range(len(territoryList)): #length should be ~56?
            worksheet.write(m+5, k+1, foreignGrossesDict[k][territoryList[m]], centerBorderFormat)#territoryList[m] is the name of the key to the dict; filmForeignList is a list of dicts: territoeyList[IndexByFilmName][keyByTerritory]-->territoy value
    for p in range(len(titleList)): #re-enter the FOREIGN TOTAL line, with its different formatting
        worksheet.write(5, p+1, foreignGrossesDict[p][territoryList[0]], boldCenterBlueFormat)
    #Adding the table's title:
    worksheet.merge_range(0, 1, 0, len(titleList), searchYear + " Top 100 Films (by Domestic Gross)", topTitleFormat)#Adding the top title
    workbook.close()
    searchYearInt += 1
