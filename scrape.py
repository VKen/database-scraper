# Sample thingy
def get_url_text(url):
    #gets the source of a URL in xml tree format
    url_hash = hashlib.sha1(url).hexdigest()
    #load from disk if it exists, if not fetch and store and disk
    try:
        #raise IOError()
        f = codecs.open("%s.txt" % url_hash, 'r', encoding="latin-1")
        x = f.read()
    except IOError:
        printc("WTF!", 1)
        resp = urllib2.urlopen(url).read()
        f = open("%s.txt" % url_hash, 'w')
        f.write(resp)
        x = resp

    return fromstring(unicode(x))


#########################################################
#Start of the test scripts
#########################################################
from pyquery import PyQuery as pq
import urllib2
import lxml
import hashlib
import os
import csv
from time import ctime as now
from time import time
from datetime import timedelta as td
from unicodedata import normalize as un

def writelog(entry,filename='log'):
    f = open(filename,'a')
    f.write(now()+" > ")
    f.write(entry)
    f.write('\n')
    f.close()

def mobylistcheck():
    url = "http://www.mobygames.com/browse/games/list-games/"
    y = pq(url)
    number = y(".mobHeader .mobHeaderItems").text()
    print "Number of games : " + number[-6:-1]

def initmobylist(list=30657):
    """Initialize moby list"""
    global num
    num = range(0,list+1,25)
    print "Tracking "+str(list)+" games in moby database"
    print "Last page starts with : " + str(num[-1])
'''
d = pq("http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/")
test = [x.attrib["href"] for x in d("#mof_object_list tbody a")]

for x in num:
    y = pq("http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/")
    scrap.append(y)
    print "done batch "+str(x)'''

####
#### Grab moby URLs of individual Games
####
def scrapepage():
    """Populate scrap list with URLs of individual games"""
    print ("Populating moby game list...")
    global scrap
    scrap = []
    # linecount = 0
    for x in num:
        url = "http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            x=f.read()
            y = pq(x)
            grab = [z.attrib["href"] for z in y("#mof_object_list tbody a")] 
            for line in grab:
                if line not in scrap:
                    if "/game/" in line:
                        scrap.append(line)
                        # print ("added "+str(line))
                        # linecount += 1
        except IOError:
            print ("scraping new html of "+str(x))
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+str(x))
    print ("Finished populating moby game list")

#######
# update moby game browser cache
#######

def updatemobycache():
    """update moby gamebrowser listing"""
    writelog("starting moby gamebrowser listing update")
    start = time()
    count = 0
    errcount = 0
    updateerr=[]
    for x in num:
        try:
            url = "http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/"
            url_hash = hashlib.sha1(url).hexdigest()
            print ("removing "+url)
            os.remove("cache/%s.txt" % url_hash)
            count += 1
            print ("removed "+url)
        except:
            errcount += 1
            updateerr.append(url)
        try:
            webscrape(url)
        except urllib2.URLError, (err):
            print ("URL error(%s)" % (err))
            print ("Retrying...")
            webscrape(url)
        except:
            raise
    if errcount:
        print ("Errors: "+str(errcount))
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Complete mobygame browser listing update in " + elapse)
    print "Time elapsed " + elapse

##########
#scrape moby individial game pages
##########

def scrapepage1():
    """scrape individual game page"""
    writelog("starting moby individual game page scrape")
    start = time()
    #count=0
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            # x=f.read()
            # y = pq(x)
            # print (str(count)+" | "+x)
            #count += 1
        except IOError:
            print ("scraping new html of "+url)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+str(x))
            #count += 1
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed individual game page scrape in " + elapse)
    print "Time elapsed " + elapse
######
#scrape credits page
######

def scrapepage2():
    """scrape credit page"""
    writelog("starting moby game credit page scrape")
    start = time()
    # count = 0
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)+"/credits"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            # x=f.read()
            # y = pq(x)
            # print (str(count)+" | "+x+"/credits")
            # count += 1
        except IOError:
            print ("scraping new html of "+url)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+url)
            # count += 1
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, credit scrape process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed credit scrape in " + elapse)
    print "Time elapsed " + elapse

######
#scrape moby platform credits page
######

def scrapepage3():
    """scrape moby platform credits page"""
    writelog("starting platform credit page scrape")
    start = time()
    # count = 0
    for x in credplatform:
        url = "http://www.mobygames.com"+str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            # x=f.read()
            # y = pq(x)
            # print (str(count)+" | "+x+"/credits")
            # count += 1
        except IOError:
            print ("scraping new html of "+url)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+url)
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, platform credit scrape process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
            # count += 1
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed platform credit scrape in " + elapse)
    print "Time elapsed " + elapse

######
# Credit check sub
######
def credsubcheck(list):
    
    global suberr
    global suberr2
    global subweird
    global subcredinplace
    global subcredplatform
    global subcredredirect

    suberr = []
    suberr2 = []
    subweird = []
    subcredinplace = []
    subcredplatform = []
    subcredredirect = []
    total = len(list)
    print ("total: " + str(total))
    creditcount = 0
    creditinplacecount = 0
    creditplatformcount = 0
    nocreditcount = 0
    other = 0
    for x in list:
        url = "http://www.mobygames.com" + str(x)
        #print ("checking "+ url)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            y = pq(f.read())
            f.close()
            z = y(".rightPanelMain p").text()   # Check for main content
        except:
            print url
            pass
        try:
            if "The following" in z:    # Check for platform list
                cd = y(".rightPanelMain ul li a")
                for each in cd:
                    cred = each.attrib["href"]
                    subcredplatform.append(cred)
                    creditplatformcount += 1
                subcredredirect.append(url)
                creditcount += 1
            elif "There are no credits" in z:   # Check for no-credits
                nocreditcount += 1
            else:
                try:
                    z1 = y(".rightPanelMain table").attr("summary") # Check for in place credits
                    if "List of Credits" in z1:
                        subcredinplace.append(url)
                        creditinplacecount += 1
                    else:
                        subweird.append(url)
                        other += 1
                except:
                    suberr2.append(url)
        except:
            suberr.append(url)
        #print ("done "+ url)
    print ("Credits: "+ str(creditcount))
    print ("Credits in platform: "+ str(creditplatformcount))
    print ("Credits in place " + str(creditinplacecount))
    print ("No Credits: "+ str(nocreditcount))
    print ("Others :" + str(other))
    print ("Errors " + str(len(suberr)))
    print ("Error2s " + str(len(suberr2)))


######
#scrape mobyrank page
######

def scrapepage4():
    """scrape mobyrank page"""
    writelog("starting moby rank page scrape")
    start = time()
    # count = 0
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)+"/mobyrank"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            # x=f.read()
            # y = pq(x)
            # print (str(count)+" | "+x+"/credits")
            # count += 1
            f.close()
        except IOError:
            print ("scraping new html of "+url)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+url)
            # count += 1
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed mobyrank page scrape in " + elapse)
    print "Time elapsed " + elapse

######
# Check for credits availability
######
def creditcheck():
    global err
    global err2
    global weird
    global credinplace
    global credplatform
    err = []
    err2 = []
    weird = []
    credinplace = []
    credplatform = []
    total = len(scrap)
    print ("total: " + str(total))
    creditcount = 0
    creditinplacecount = 0
    creditplatformcount = 0
    nocreditcount = 0
    other = 0
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)+"/credits"
        #print ("checking "+ url)
        url_hash = hashlib.sha1(url).hexdigest()
        f = open("cache/%s.txt" % url_hash, 'r')
        y = pq(f.read())
        z = y(".rightPanelMain p").text()   # Check for main content
        try:
            if "The following" in z:    # Check for platform list
                cd = y(".rightPanelMain ul li a")
                for each in cd:
                    cred = each.attrib["href"]
                    credplatform.append(cred)
                    creditplatformcount += 1
                creditcount += 1
            elif "There are no credits" in z:   # Check for no-credits
                nocreditcount += 1
            else:
                try:
                    z1 = y(".rightPanelMain table").attr("summary") # Check for in place credits
                    if "List of Credits" in z1:
                        credinplace.append(url)
                        creditinplacecount += 1
                    else:
                        weird.append(url)
                        other += 1
                except:
                    err2.append(url)
        except:
            err.append(url)
        #print ("done "+ url)
    f.close()
    print ("Credits: "+ str(creditcount))
    print ("Credits in platform: "+ str(creditplatformcount))
    print ("Credits in place " + str(creditinplacecount))
    print ("No Credits: "+ str(nocreditcount))
    print ("Others :" + str(other))
    print ("Errors " + str(len(err)))
    print ("Error2s " + str(len(err2)))

######
# Scrape moby credits sub page ordering by developer
######

def scrapepage5(list):
    """scrape moby credits sub page ordering by developer"""
    writelog("starting mob game credit sub page scrape")
    start = time()
    for x in list:
        url = x
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            x=f.read()
            print ("extracting "+url)
            y = pq(x)
            gametitle = y("#gameTitle a").text().encode("utf-8")
            gameplatform = y("#gamePlatform").text().encode("utf-8")
            core = y("#coreGameRelease a")  # Basic Information block
            gamepublisher = core[0].text_content().encode("utf-8")
            gamedeveloper = core[1].text_content().encode("utf-8")
            gamerelease = core[2].text_content().encode("utf-8")
            core2 = y("#coreGameGenre a")
            core2num = len(core2)   # Begin dealing with variable info block
            gamemisc = []
            for x in range (0,core2num):
                if x == 0:
                    gamegenre = core2[0].text_content().encode("utf-8")
                elif x == 1:
                    gameperspective = core2[1].text_content().encode("utf-8")
                else:
                    misc = core2[x].text_content().encode("utf-8")
                    gamemisc.append(misc)
            if len(gamemisc) == 0:
                gamemisc = "Nil"
            mobyrank = y(".scoreBoxBig").text()
            mobyscore = y(".scoreBoxMed").text()
            main = y(".rightPanelMain tr") #Get the main info
            num = len(main) #get the number of table rows
            for x in range(0,num):  #begin ripping the table contents apart
                stuff = main[x].attrib
                if not stuff: # check for header row
                    affiliation = main[x].text_content()
                else:
                    position = main[x][0].text_content().encode("utf-8")
                    memnum = len(main[x][1])
                    if memnum == 0:
                        #print ("memnum = "+str(memnum))
                        member = main[x][1].text_content().encode("utf-8")
                        c.writerow([member]+[position]+[affiliation]+[gametitle]+[gameplatform]+[gamepublisher]+[gamedeveloper]+[gamerelease]+[gamegenre]+[gameperspective]+[gamemisc]+[mobyrank]+[mobyscore])
                    else:
                        for z in range(0,memnum):
                            #print("else memnum = "+str(z))
                            member = main[x][1][z].text_content().encode("utf-8")
                            c.writerow([member]+[position]+[affilation]+[gametitle]+[gameplatform]+[gamepublisher]+[gamedeveloper]+[gamerelease]+[mobyrank]+[mobyscore]+[gamegenre]+[gameperspective]+[gamemisc])
            print ("done "+url)
            #break
        except IOError:
            print ("scraping new html of "+str(x))
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+str(x))
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed moby credit sub page scrape in " + elapse)
    print "Time elapsed " + elapse
        #break
         


#thinking about it....
####
# to dig studio/contribution affiliation
####
'''for i in range(0,num):
    stuff = x[i].attrib
    if not stuff:
        print (x[i].text_content())
        affiliation = x[i].text_content()
    else:
        print (x[i][0].text_content()+" "+x[i][1].text_content()+" "+affiliation)'''

######
# scrape moby release info page
######

def scrapepage6():
    """scrape moby release info page"""
    writelog("starting moby release info page scrape")
    start = time()
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)+"/release-info"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            #x=f.read()
            #y = pq(x)
        except IOError:
            print ("scraping new html of "+url)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+url+" info")
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed release info page scrape in " + elapse)
    print "Time elapsed " + elapse

######
# scrape moby techinfo page
######

def scrapepage7():
    """scrape moby tech info page"""
    writelog("starting moby tech info page scrape")
    start = time()
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)+"/techinfo"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            #x=f.read()
            #y = pq(x)
        except IOError:
            print ("scraping new html of "+url)
            while True:  # Unlimited tries to pull data
                try:
                    resp = urllib2.urlopen(url).read()
                    f = open("cache/%s.txt" % url_hash, 'w')
                    f.write(resp)
                    break
                except urllib2.URLError, (err):
                    print ("URL error(%s)" % (err))
                    writelog(str(err) + "| Error, retrying...")
                    print ("Retrying...")
                    pass
                except:
                    pass
            print ("done "+url)
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed tech info page scrape in " + elapse)
    print "Time elapsed " + elapse

######
# scrape business model
######
def bizmodelcheck():
    """check tech info page for business model"""
    writelog("starting capturing of business model data test")
    start = time()

    global bizmodel
    bizmodel = []
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)+"/techinfo"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
        except:
            raise
        x=f.read()
        y=pq(x)
        main = y(".rightPanelMain table").text()

        # check for business model in table
        if "Business Model" in strip_accents(main):
            bizmodel.append(url)
    print ("Completed process")
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed checking of tech info business model in " + elapse)
    print "Time elapsed " + elapse


######
# scrape business model detail
######
def bizmoddetgrab():
    """grab business model"""
    writelog("starting grab of business model detail test")
    start = time()
    print "Running business model detail grab"
    global bizdet
    bizdet = []
    for xurl in bizmodel:
        url = xurl
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
        except:
            raise
        check = 0 #debug check
        x=f.read()
        y=pq(x)
        table = y(".rightPanelMain table")
        num = len(table)*2
        for x in range(2,num+1,2): # Check table details
            str2 = ".rightPanelMain > table.techInfo:nth-child({0}) > tr > td:nth-child(1)".format(x)
            column1 = strip_accents(y(str2).text())
            if "Business Model" in column1:
                #grab platform model
                str1 = ".rightPanelMain > table.techInfo:nth-child({0}) thead".format(x)
                platform = strip_accents(y(str1).text())
                #print platform

                #grab game name
                gamename = strip_accents(y("#gameTitle a").text()) # get gamename
                #print gamename

                # getting release date
                listing = [strip_accents(z.text_content()) for z in y("#coreGameRelease > div")]

                # getting indexes and corresponding items
                try:
                    indexrel = listing.index("Released")
                    releasedate = listing[indexrel+1]
                except:
                    releasedate = 'nil'
                #print releasedate

                # get column1 rows in a table
                str3 = ".rightPanelMain > table.techInfo:nth-child({0}) > tr > td:nth-child(1)".format(x)
                rows = y(str3)
                rownum = len(rows)
                rowlisting = []
                for row in rows:
                    rowlisting.append(strip_accents(row.text_content()))
                targetrownum = rowlisting.index("Business Model")
                # get target row in column 2
                str4 = ".rightPanelMain > table.techInfo:nth-child({0}) > tr > td:nth-child(2)".format(x)
                column2rows = y(str4)
                model = strip_accents(column2rows[targetrownum].text_content())
                # print model
                # print url
                bizdet.append([gamename,platform,releasedate,model,url])
                check += 1
                # print "Found"
        if check == 0:
            print url + " nothing?"
    print ("Completed process")
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed grab of business model detail test in " + elapse)
    print "Time elapsed " + elapse
#####
# mobyrank individual platform scrap
#####


def scrapepage8(list):
    """scrape mobyrank individual platform page"""
    print ("starting mobyrank individual platform scrape")
    writelog("starting mobyrank individual platform scrape test")
    start = time()
    for x in list:
        url = "http://www.mobygames.com"+str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            #x=f.read()
            #y = pq(x)
        except IOError:
            print ("scraping new html of "+url)
            while True:  # Unlimited tries to pull data
                try:
                    resp = urllib2.urlopen(url).read()
                    f = open("cache/%s.txt" % url_hash, 'w')
                    f.write(resp)
                    break
                except urllib2.URLError, (err):
                    print ("URL error(%s)" % (err))
                    writelog(str(err) + "| Error, retrying...")
                    print ("Retrying...")
                    pass
                except KeyboardInterrupt:
                    raise
            print ("done "+url)
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog("Error, process stopped after: "+ elapse)
            print "Error Time elapsed: " + elapse
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed mobyrank individual platform scrape test in " + elapse)
    print "Time elapsed " + elapse


########
# Grab parts of the moby list
########
def scrapelist():

    # linecount = 0
    for x in num:
        url = "http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            x=f.read()
            y = pq(x)
            for stuff in y("#mof_object_list tbody td"):
                grab1.append(stuff.text_content())
        except IOError:
            print "scraping new html of "+str(x)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print "done "+str(x)
############## Grab to types #####################

def initgamelist():
    global gamename
    global gameyear
    global gampublisher
    global gamegenre
    global gameplatform
    gamename = []
    gameyear = []
    gamepublisher = []
    gamegenre = []
    gameplatform = []

def grabtype():
    """grab field types from gamebrowser list"""
    for x in num:
        url = "http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            x=f.read()
            y = pq(x)
            for stuff in y("#mof_object_list tbody td"):
                grab1.append(stuff.text_content())
        except IOError:
            print "end"

    objcnt = 0

    for stuff in grab1:
        if int(objcnt)%5 == 0: # gamename
            gamename.append(stuff)
        elif int(objcnt)%5 == 1: # gameyear
            gameyear.append(stuff)
        elif int(objcnt)%5 == 2: # gamepublisher
            gamepublisher.append(stuff)
        elif int(objcnt)%5 == 3: # gamegenre
            gamegenre.append(stuff)
        elif int(objcnt)%5 == 4: # gameplatform
            gameplatform.append(stuff)
        objcnt += 1


###########
# grab individual game details: Publisher, Developer, Release Date, Platform
###########

def gamedetgrab(list):
    """grab individual game details: Publisher, Developer, Release Date, Platform"""
    global deterr
    global det8
    global det6
    global det6nopub
    global det6nodev
    global det6norel
    global det6noplat
    global det4

    deterr = []
    det8 = []
    det6 =[]
    det6nopub = []
    det6nodev = []
    det6norel = []
    det6noplat = []
    det4 = []
    det4nopub = []
    det4nodev = []
    det4norel = []
    det4noplat = []
    

    print ("grabing game details from list")
    writelog("starting game detail grab test")
    start = time()
    print ("No. of items in list: " + str(len(list)))
    for x in list:
        url = "http://www.mobygames.com"+str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            detpanel = y('.rightPanel #coreGameRelease div')
            if len(detpanel) is 8:
                det8.append(url)
            elif len(detpanel) is 6:
                det6.append(url)
                det6list = [strip_accents(x.text_content()) for x in detpanel]
                if "Published by" not in det6list:
                    det6nopub.append(url)
                elif "Developed by" not in det6list:
                    det6nodev.append(url)
                elif "Released" not in det6list:
                    det6norel.append(url)
                elif "Platforms" not in det6list:
                    if "Platform" not in det6list:
                        det6noplat.append(url)
            elif len(detpanel) is 4:
                det4.append(url)
                det4list = [strip_accents(x.text_content()) for x in detpanel]
                if "Published by" not in det4list:
                    det4nopub.append(url)
                elif "Developed by" not in det4list:
                    det4nodev.append(url)
                elif "Released" not in det4list:
                    det4norel.append(url)
                elif "Platforms" not in det4list:
                    if "Platform" not in det4list:
                        det4noplat.append(url)
            else:
                print (url)
                deterr.append(url)
        except:
            print (x)
            raise
    print "8 fields: " + str(len(det8))
    print "6 fields: " + str(len(det6))
    print "---- No Publisher: " + str(len(det6nopub))
    print "---- No Developer: " + str(len(det6nodev))
    print "---- No Release date: " + str(len(det6norel))
    print "---- No Platforms: " + str(len(det6noplat))
    print "4 fields: " + str(len(det4))
    print "---- No Publisher: " + str(len(det4nopub))
    print "---- No Developer: " + str(len(det4nodev))
    print "---- No Release date: " + str(len(det4norel))
    print "---- No Platforms: " + str(len(det4noplat))
    print "Errors: " + str(len(deterr))
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed game detail grab test in " + elapse)
    print "Time elapsed " + elapse
    
    
def gamedetgrab2(list):
    """grab individual game details: Publisher, Developer, Release Date, Platform"""
    print ("grabing game details from list...")
    writelog("starting game detail grab test 2")
    start = time()
    global gamenameandplatform
    gamenameandplatform = []
    for x in list:
        url = "http://www.mobygames.com"+str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            gamename = strip_accents(y('#gameTitle').text())
            detpanel = y('.rightPanel #coreGameRelease div')
            detlist = [strip_accents(x.text_content()) for x in detpanel]
            gamerelease = strip_accents(detlist[-3])
            gamereleaseyear = yeargrab(gamerelease)
            platformlist = detlist[-1].split(',')
            for x in platformlist:
                gameplatform = x.strip()
                gamenameandplatform.append([gamename,gameplatform,gamerelease])
        except:
            raise
    print "listing: " + str(len(gamenameandplatform))
    print ('Done grab test 2')
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed game detail grab test 2 in " + elapse)
    print "Time elapsed " + elapse


def gamedetgrab3(list):
    """grab individual game details: Publisher, Developer, Release Date, Platform + genre and other craps"""
    print ("grabing game genre from list...")
    writelog("starting game genre grab test")
    start = time()
    global gamegenres
    global gamegenrelisting
    gamegenres = []
    gamegenrelisting = []

    global genrecollation
    genrecollation = []

    #count = 0

    for x in list:
        #count += 1
        url = "http://www.mobygames.com"+str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            f.close()
        except:
            raise
        gamename = strip_accents(y('#gameTitle').text())
        detpanel = y('.rightPanel #coreGameRelease div')
        detlist = [strip_accents(x.text_content()) for x in detpanel]
        gamerelease = strip_accents(detlist[-3])
        gamereleaseyear = yeargrab(gamerelease)
        gamegenre = []

        # General Genre Classification
        c1 = 'Nil' # Action
        c2 = 'Nil' # Adventure
        c3 = 'Nil' # Educational
        c4 = 'Nil' # Racing / Driving
        c5 = 'Nil' # Role-Playing (RPG)
        c6 = 'Nil' # Simulation
        c7 = 'Nil' # Sports
        c8 = 'Nil' # Strategy

        genrelist = (y("#coreGameGenre div div"))
        if len(genrelist): # Check for genre existence
            listing = []
            for x in genrelist:
                listing.append(strip_accents(x.text_content()))
                gamegenrelisting.append(strip_accents(x.text_content()))
            try:
                genrepos = listing.index('Genre')
                genreclasses = genrelist[genrepos+1]
                for x in genreclasses:
                    gamegenre.append(strip_accents(x.text_content()))
                    gamegenre.sort()
                    for x in gamegenre:
                        if 'Action' in x:
                            c1 = 'Action'
                        elif 'Adventure' in x:
                            c2 = 'Adventure'
                        elif 'Educational' in x:
                            c3 = 'Educational'
                        elif 'Racing' in x:
                            c4 = 'Racing / Driving'
                        elif 'RPG' in x:
                            c5 = 'Role-Playing (RPG)'
                        elif 'Simulation' in x:
                            c6 = 'Simulation'
                        elif 'Sports' in x:
                            c7 = 'Sports'
                        elif 'Strategy' in x:
                            c8 = 'Strategy'
                        genrecollation.append(x)
            except ValueError:
                pass
            except:
                raise
                    
        platformlist = detlist[-1].split(',')
        for x in platformlist:
            gameplatform = x.strip()
            gamegenrelist = [c1, c2, c3, c4, c5, c6, c7, c8]
            gamegenres.append([gamename,gameplatform,gamerelease,gamereleaseyear]+gamegenrelist)
        #if count >= 100:
            #break

    print ('Done game genre grab test')
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed game genre grab test in " + elapse)
    print "Time elapsed " + elapse

######
# grab game developers *Error
######

def gamedevgrab(list):
    """grab individual game developers"""
    print ("grabing game dev from list...")
    writelog("starting game dev grab test...")
    start = time()
    global devlist
    devlist = []
    platcount = 0
    platcount2 = 0
    for x in list:
        url = str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            f.close()
        except:
            raise
        gamename = strip_accents(y('#gameTitle').text())
        detpanel = y('.rightPanel #coreGameRelease div')
        detlist = [strip_accents(x.text_content()) for x in detpanel]
        gamerelease = strip_accents(detlist[-3])
        platformlist = strip_accents(y('#gamePlatform').text())
        if not platformlist:
            platformlist = detlist[-1]
            platcount +=1
        if 'Combined View' in platformlist:
            platformlist = platformlist[0:-16]
            platcount2 +=1
        main = y(".rightPanelMain tr") #Get the main info
        num = len(main) #get the number of table rows
        for x in range(0,num):  #begin ripping the table contents apart
            stuff = main[x].attrib
            if not stuff: # check for header row
                affiliation = strip_accents(main[x].text_content())
            else:
                position = strip_accents(main[x][0].text_content())
                memnum = len(main[x][1])
                if memnum == 0:
                    #print ("memnum = "+str(memnum))
                    member = strip_accents(main[x][1].text_content())
                    devlist.append([member,position,affiliation,gamename,platformlist,gamerelease])
                else:
                    for z in range(0,memnum):
                        #print("else memnum = "+str(z))
                        member = strip_accents(main[x][1][z].text_content())
                        devlist.append([member,position,affiliation,gamename,platformlist,gamerelease])
        #break

    print ('Done grab dev test')
    print ('No Platform: '+str(platcount))
    print ('No Platform + other platform: ' + str(platcount2))
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed game dev grab test in " + elapse)
    print "Time elapsed " + elapse

######
# mobycheck
######
def mobyrankcheck(list,optionnum = 1):
    """moby rank checking for multi or single platform"""
    print ("Running mobyrank check...")
    writelog("moby rank check...")
    start = time()
    global mobysingle
    global mobymulti
    global mobyplat
    global mobyweird
    global mobyerr
    
    mobysingle = []
    mobymulti = []
    mobyplat = []
    mobyweird = []
    mobyerr = []

    multicount = 0

    for x in list:
        if optionnum == 1:
            url = "http://www.mobygames.com"+str(x)+"/mobyrank"
        if optionnum == 2:
            url = str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            f.close()
        except:
            print (url)
            raise
        check = y('#coreGameRank .pct100')
        if check: # Check existence of multi-platform
            count = 0
            for x in y("#coreGameRank .pct100 tbody .left"): # check exact number of platforms
                if len(x.text_content()) > 0:
                    count += 1
            mobymulti.append([url,count])
            multicount += count
            corelist = y("#coreGameRelease div a") # check for links
            num = len(corelist)
            count2 = 0
            for x in range(0,num):
                link = corelist[x].attrib["href"]
                if "/mobyrank" in link: # check for platform urls
                    mobyplat.append("http://www.mobygames.com"+link)
                    count2 += 1
                else:
                    pass
            if count != count2:
                mobyweird.append(url)
        elif len(y("#coreGameRank div b")) == 2: # check for bolded headers of MobyRank and MobyScore
            mobysingle.append(url)
        else:
            mobyerr.append(url)
    print ("Done mobyrank check.") 
    print ("Multiple platforms: " +str(len(mobymulti)))
    print ("----platforms"+str(len(mobyplat))+" | count = "+str(multicount))
    print ("Single platform: " + str(len(mobysingle)))
    print ("Error: " +  str(len(mobyerr)))
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed moby rank check in " + elapse)
    print "Time elapsed " + elapse

######
# Mobyrank press and review availability check
######

def mbrprcheck(list):
    """moby rank checking for existence of press or scores"""
    print ("Running mobyrank detailed check test...")
    writelog("moby rank check...")
    start = time()

    global mbrcomplete
    global mbrpress
    global mbscore
    global mbrempty

    mbrcomplete = []
    mbrpress = []
    mbscore = []
    mbrempty = []
    for x in list:
        url = str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            f.close()
        except:
            print (url)
            raise
        press = 0
        score = 0
        if len(y(".rightPanelMain .m5 + p")): # Check for press existence
            p = y(".rightPanelMain .m5 + p")[0].text_content()
            if 'no rankings' in p:
                press = 0
            if 'no reviews' in p:
                press = 1
        if 'MobyRanks are listed' in strip_accents(y(".rightPanelMain").text()[15:42]):
            press = 1

        if y(".m5 + div.floatholder table"): # Check for user score table existence
            score = 1

        if not press and not score: # Tally results
            mbrempty.append(url)
        elif not score:
            mbrpress.append(url)
        elif not press:
            mbscore.append(url)
        elif press and score:
            mbrcomplete.append(url)
    print ("Empty: " + str(len(mbrempty)))
    print ("Press only:" + str(len(mbrpress)))
    print ("Score only: " + str(len(mbscore)))
    print ("Both: " + str(len(mbrcomplete)))
    print ("completed moby rank detailed check")
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed moby rank detailed check test in " + elapse)
    print "Time elapsed " + elapse
 

######
# Grab moby rank details
######

def gamemobyrankgrab(listinput,option):
    """grab moby ranking. options: 'c'=complete, 'p'=press only, 's'=score only.""" 
    print ("grabing mobyrank details from list...")
    writelog("starting mobyrank detail grab test...")
    start = time()
    global mobyranklist
    mobyranklist = []
    # debug break
    total = float(len(listinput))
    percent = float(0)
    count = float(0)
    newpercent = float(0)
    for x in listinput:
        url = str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            f.close()
        except:
            raise
        # initialize data fields
        gamename = 'Nil'
        platform = 'Nil'
        publisher = 'Nil'
        developer = 'Nil'
        releasedate = 'Nil'
        mobyrank = 'Nil'
        mobyscore = 'Nil'
        mobyscorevoter = 'Nil'
        mobyscorefinal = []
        press = []

        # Start of grabbing operations
        gamename = strip_accents(y("#gameTitle").text())
        platform = strip_accents(y("#gamePlatform").text())

        # Grab publisher developer, and release date
        listing = [strip_accents(x.text_content()) for x in y("#coreGameRelease > div")]
        # getting indexes and corresponding items
        try:
            indexpub = listing.index("Published by")       
            publisher = listing[indexpub+1]
        except:
            pass
        try:
            indexdev = listing.index("Developed by")
            developer = listing[indexdev+1]
        except:
            pass
        try:
            indexrel = listing.index("Released")
            releasedate = listing[indexrel+1]
        except:
            pass   

        # Grab mobyrank
        mobyrank = strip_accents(y("#coreGameRank .fr.scoreBoxBig").text())

        # Grab moby score from the overall box
        mobyscore = strip_accents(y("#coreGameScore > div.fr").text())

        # apply to combine and press-only list
        if option in "cp":
            # grab full list of press
            presslist = y(".mobyrank.scoresource")
            articlesnum = len (presslist)
            pressentry = []

            for x in range(articlesnum):
                pressscore = strip_accents(y(".mobyrank.scoresource .fl")[x].text_content())
                presssource = strip_accents(y(".mobyrank.scoresource .source")[x].text_content())
                try:
                    presslink = y(".mobyrank.scoresource .url a")[x].attrib["href"]
                except:
                    presslink = 'Nil'
                pressnormalize = [pressscore,presssource,presslink]
                for x in pressnormalize:
                    press.append(x)
        # apply to combined and only-score list
        if option in "cs":
            # Grab voters number for moby score
            footer = y(".m5 + div.floatholder table.reviewList tfoot .left").text()
            mobyscorevoter = strip_accents(voters(footer))

            # Grab score category
            mobyscorecat = []
            mobyscorecatscore = []
            mobyscorecombined = []
            try:
                table = y(".m5 + div.floatholder table.reviewList tbody tr td.left")
                num = len(table)
                for x in range(0,num,2):
                    mobyscorecat.append(strip_accents(table[x].text_content()))

            # Grab score category score
                scoretable = y(".m5 + div.floatholder table.reviewList tbody tr td.center")
                for x in range(num/2):
                    mobyscorecatscore.append(strip_accents(scoretable[x].text_content()))
            except:
                raise

            # Combine mobyscore cat and score
            zipped = zip(mobyscorecat,mobyscorecatscore)
            for x in zipped:
                z = list(x)
                mobyscorecombined.append(" : ".join(z))

            # Combine mobyscorecombined list
            mobyscorefinal.append(" | ".join(mobyscorecombined))
        # compile mobyranklist
        mobyranklist.append([gamename,platform,publisher,developer,releasedate,mobyrank,mobyscore,mobyscorevoter,mobyscorefinal]+press)
        # debug break
        count += 1
        newpercent = count / total * 100
        new = "%.1f" % newpercent
        if new > percent:
            percent = new
            print (str(new)+" complete...")
        
        
        #   break
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed moby rank detail grab test in " + elapse)
    print "Time elapsed " + elapse

######
# Mobyscore grab
######

def gamemobyscoregrab(listinput,option):
    """grab moby score. options: 'c'=complete, 'p'=press only, 's'=score only.""" 
    print ("grabing mobyscore details from list...")
    writelog("starting mobyscore detail grab test...")
    start = time()
    global mobyscorelist
    mobyscorelist = []
    global scorecat
    scorecat = []

    # debug break
    total = float(len(listinput))
    percent = float(0)
    count = float(0)
    newpercent = float(0)
    for x in listinput:
        url = str(x)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            x = f.read()
            y = pq(x)
            f.close()
        except:
            raise
        # initialize data fields
        gamename = 'Nil'
        platform = 'Nil'
        publisher = 'Nil'
        developer = 'Nil'
        releasedate = 'Nil'
        releaseyear = 'Nil'
        mobyrank = 'Nil'
        mobyscore = 'Nil'
        mobyscorevoter = 'Nil'
        mobyscorefinal = []
        press = []

        # scorelisting classification
        c1 = 'Nil' # AI
        c2 = 'Nil' # Acting
        c3 = 'Nil' # Effectiveness
        c4 = 'Nil' # Gameplay
        c5 = 'Nil' # Graphics
        c6 = 'Nil' # Personal Slant
        c7 = 'Nil' # Sound / Music
        c8 = 'Nil' # Story / Presentation
        c9 = 'Nil' # Text Parser

        # Start of grabbing operations
        gamename = strip_accents(y("#gameTitle").text())
        platform = strip_accents(y("#gamePlatform").text())

        # Grab publisher developer, and release date
        listing = [strip_accents(x.text_content()) for x in y("#coreGameRelease > div")]
        # getting indexes and corresponding items
        try:
            indexpub = listing.index("Published by")       
            publisher = listing[indexpub+1]
        except:
            pass
        try:
            indexdev = listing.index("Developed by")
            developer = listing[indexdev+1]
        except:
            pass
        try:
            indexrel = listing.index("Released")
            releasedate = listing[indexrel+1]
            try:
                releaseyear = yeargrab(releasedate)
            except:
                pass
        except:
            pass   

        # Grab mobyrank
        #mobyrank = strip_accents(y("#coreGameRank .fr.scoreBoxBig").text())

        # Grab moby score from the overall box
        mobyscore = strip_accents(y("#coreGameScore > div.fr").text())

        # apply to combined and only-score list
        if option in "cs":
            # Grab voters number for moby score
            footer = y(".m5 + div.floatholder table.reviewList tfoot .left").text()
            mobyscorevoter = strip_accents(voters(footer))

            # Grab score category
            mobyscorecat = []
            mobyscorecatscore = []
            mobyscorecombined = []
            try:
                table = y(".m5 + div.floatholder table.reviewList tbody tr td.left")
                num = len(table)
                for x in range(0,num,2):
                    mobyscorecat.append(strip_accents(table[x].text_content()))
                    scorecat.append(strip_accents(table[x].text_content()))

            # Grab score category score
                scoretable = y(".m5 + div.floatholder table.reviewList tbody tr td.center")
                for x in range(num/2):
                    mobyscorecatscore.append(strip_accents(scoretable[x].text_content()))
            except:
                raise

            # Combine mobyscore cat and score
            zipped = zip(mobyscorecat,mobyscorecatscore)
            for x in zipped:
                z = list(x)
                if 'AI' in z[0]:
                    c1 = str(z[1])
                elif 'Acting' in z[0]:
                    c2 = str(z[1])
                elif 'Effect' in z[0]:
                    c3 = str(z[1])
                elif 'Gameplay' in z[0]:
                    c4 = str(z[1])
                elif 'Graphics' in z[0]:
                    c5 = str(z[1])
                elif 'Personal' in z[0]:
                    c6 = str(z[1])
                elif 'Sound' in z[0]:
                    c7 = str(z[1])
                elif 'Story' in z[0]:
                    c8 = str(z[1])
                elif 'Text' in z[0]:
                    c9 = str(z[1])
                #for a in z:
                    #mobyscorecombined.append(a)

            # Combine mobyscorecombined list
            #for x in mobyscorecombined:
                #mobyscorefinal.append(x)
        mobycats = [c1,c2,c3,c4,c5,c6,c7,c8,c9]
        # compile mobyranklist
        mobyscorelist.append([gamename,platform,publisher,developer,releasedate,releaseyear,mobyscore,mobyscorevoter]+mobycats)
        # debug break
        count += 1
        newpercent = float(count) / total * 100
        new = "%.1f" % newpercent
        if float(new) > float(percent):
            percent = new
            print (str(new)+" complete...")
        
        
        #   break
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed moby score detail grab test in " + elapse)
    print "Time elapsed " + elapse

######
# Truncate list function
######

def truncatelist(list,truncatelength=100):
    """chop to size"""
    print ("truncating list test...")
    writelog("starting truncate test...")
    start = time()
    xcount = 0
    ycount = 0
    cut = truncatelength
    for x in list:
        ycount = 0
        for y in x:
            if len(y) > cut:
                list[xcount][ycount] = y[0:cut]
            ycount += 1
        xcount += 1
    print ('Done truncate test')
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed truncate test in " + elapse)
    print "Time elapsed " + elapse


######
# CSV Exporter
######

def exportcsv(list,filenamestr='test',rowlimitnum=65000):
    """export list to csv. default to 65k rows for MS excel 2003 compatibility"""
    writelog("starting csv export to %s.csv" % filenamestr)
    start = time()
    rowcount = 0
    rowlimit = rowlimitnum
    filecount = 0
    for x in list:
        if rowcount > rowlimit:
            filecount += 1
            rowcount = 0
        filename = str(filenamestr) + str(filecount)
        f = open('export/%s.csv' % filename,'a')
        c = csv.writer(f)
        c.writerow(x)
        rowcount += 1
    f.close()
    print ("finish export")
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed csv export in " + elapse)
    print "Time elapsed " + elapse

##Test##
"""
for stuff in y("#mof_object_list tbody td"):
    if int(objcnt)%5 == 0:
        print stuff.text_content()
    objcnt += 1"""


######################
# Unicode and CSV
######################
"""
import unicodedata

for x in gamename:
    if x is unicode:
        c.writerow(unicodedata.normalize('NKFD',x).encode('ascii','ignore'))
    else:
        c.writerow(x)"""
def strip_accents(string):
  import unicodedata
  return unicodedata.normalize('NFKD', unicode(string)).encode('ASCII', 'ignore')

"""
import csv
c = csv.writer(open("gamedata.csv","w"))

numcount = 0

for x in gamename:
    c.writerow([x.encode('utf-8')]+[gameyear[numcount]]+[gamepublisher[numcount].encode('utf-8')]+[gamegenre[numcount]]+[gameplatform[numcount].encode('utf-8')])
    numcount += 1
    print x"""
def targetcsvfile(filename):
    f = open(filename,"w")
    global c
    c = csv.writer(f)

######
# scrape EA Games
######

def initealist():
    global grab2
    grab2 = []

def scrapeeagames():
    for x in num:
        url = "http://www.ea.com/games/gamePaging?sort=newest&i=1&s=641&c=25664497"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            x=f.read()
            y = pq(x)
            for stuff in y(""):
                grab2.append(stuff.text_content())
        except IOError:
            print "scraping new html of "+str(x)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print "done "+str(x)

######
# Scrape XBox links
######
def initxboxlist():
    global grab3
    global xboxlist
    grab3 = []
    xboxlist = []

def scrapexboxgames():
    url = "http://www.xbox.com/en-US/games/catalog.aspx?st=&g=0&r=0&sd=0&p=1&c=1675"
    url_hash = hashlib.sha1(url).hexdigest()
    try:
        f=open("cache/%s.txt" % url_hash, 'r')
        x=f.read()
        y = pq(x)
        grab3 = [stuff.attrib["href"] for stuff in y(".XbcPcResult .XbcRelative h4 a")]
    except IOError:
        print "scraping new html of "+str(url)
        resp = urllib2.urlopen(url).read()
        f = open("cache/%s.txt" % url_hash, 'w')
        f.write(resp)
        print "done "+str(url)

######
# Scrape XBox individual pages
######


def scrapepagexboxpage():    # Note: 2 sites cannot hit, halo3 versions
    for x in grab3:
        url = x
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            x=f.read()
            y = pq(x)
            name = y(".XbcWpProductInfo h6").text().encode('ascii','ignore')
            anchor = [x.text_content() for x in y(".XbcWpProductInfo p a")]
            developer = anchor[0].encode('ascii','ignore')
            publisher = anchor[1].encode('ascii','ignore')
            genre = anchor[2].encode('ascii','ignore')
            anchor2 = [x.text_content() for x in y(".XbcWpProductInfo p")]
            releasedate = anchor2[3][14:].encode('ascii','ignore')
            platform = anchor2[4][9:].encode('ascii','ignore')
            xboxlist.append([name,anchor,developer,publisher,genre,releasedate,platform])
        except IOError:
            print "scraping new html of "+str(url)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print "done "+str(url)

######
# scrape games for windows
######
def startgamesforwindowslist(page=9):
    numwin= range(1,page)
    grab4 = []

def scrapepagewindows():
    for x in numwin:
        url = "http://www.microsoft.com/games/en-us/Games/Pages/catalog"+str(x)+".aspx"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            x=f.read()
            y = pq(x)
            for stuff in y(""):
                grab4.append(stuff.text_content())
        except IOError:
            print "scraping new html of "+str(url)
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print "done "+str(url)


######
# Gamespot
######

def initgamespotlist():
    global gslist
    gslist = []
    gamebrowserurl = "http://www.gamespot.com/games.html?type=games&mode=all&sort=title&dlx_type=all&sortdir=desc&official=all"
    sitepage = Webpage(gamebrowserurl)
    lastpage = sitepage.pq_text('ul.pages>li.last a')[0]
    print ("Last page is "+str(lastpage))
    for x in range(int(lastpage)):
        url = "http://www.gamespot.com/games.html?type=games&mode=all&sort=title&dlx_type=all&sortdir=desc&official=all&page="+str(x)
        gslist.append(url)

def scrapegspage(listing):
    writelog('Starting Gamespot Scraping and individual game link grab')
    start = time()
    global gsindlist
    global bin404
    bin404 = []
    gsindlist = []
    for x in listing:
        try:
            page = Webpage(x)
            page.pq.make_links_absolute('http://www.gamespot.com')
        except KeyboardInterrupt:
            raise
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog('error occurred')
            raise
        for x in page.pq_links('table tbody tr th a'):
            url = str(x[1])
            gsindlist.append(url)
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed gamespot individual game page link grab in " + elapse)
    print "Time elapsed " + elapse

def gsindvpage(listing):
    writelog("Starting Gamespot individual game page grab")
    start = time()
    global gstechinfo
    global gscritic
    global gserr1
    global gserr2
    global bin404
    gstechinfo = []
    gscritic = []
    gserr1 = []
    gserr2 = []
    bin404 = []
    for x in listing:
        try:
            page = Webpage(x)
            if page:
                page.pq.make_links_absolute('http://www.gamespot.com')
        except KeyboardInterrupt:
            raise
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog('error occurred')
            raise
        if not page:
            bin404.append(x)
            pass
        try:
            techurl = page.pq_links('.techinfo a')[0][1]
            gstechinfo.append(techurl)
        except IndexError:
            try:
                techurl = page.pq_links('div.body div.product div.specs>a.details_link')[0][1]
                gstechinfo.append(techurl)
            except:
                gserr1.append(x)
                pass
        except TypeError:
            gserr2.append(x)
            pass
        try:
            criticurl = page.pq_links('.review_scores .critic_score .wrap span.more a')[0][1]
            if criticurl:
                if 'http' not in criticurl:
                    break                
            gscritic.append(criticurl)
        except IndexError:
            pass
        except TypeError:
            gserr2.append(x)
        except:
            raise
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed gamespot individual game page grab in " + elapse)
    print "Time elapsed " + elapse
    

def gsindvtech(listing=''):
    writelog("Starting Gamespot individual game tech page grab")
    start = time()
    listing = set(gstechinfo)
    global bin404
    bin404 = []
    global multidate
    multidate = []
    global gsincomplete
    gsincomplete = []
    global gsdevlist
    gsdevlist = []
    global gstechinfodata
    gstechinfodata = []
    global info
    info = []
    # start cycle
    for x in listing:
        try:
            page = Webpage(x)
            if page:
                page.pq.make_links_absolute('http://www.gamespot.com')
        except KeyboardInterrupt:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog('keyboard interrupt after ' + elapse)
            raise
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog('error occurred')
            print 'some error in grabbing page'
            raise

        if not page:
            pass
        else:
            ## Grab primary information
            title = strip_accents(page.pq_text('.product_title')[0])
            platform = page.pq('.nav a.on')
            if not platform:
                platform = ''
            else:
                platform = strip_accents(platform[0].text_content())
            
            ## main tech info box
            main = page.pq('#main #tech_info div.body div.module div.body dl.game_info').eq(0)
    
            if len(main('dd')) > 7:
                print 'main is longer'
                raise
    
            maindict = {} # initiate dictionary to deal with info
    
            for y in range(len(main('dd'))): # grab information
                maindict[strip_accents(main('dt').eq(y).text())] = strip_accents(main('dd').eq(y).text())
            keys = maindict.keys()
    
            # assign information
            publisher = ''
            if 'Publisher:' in keys:
                publisher = maindict['Publisher:']
    
            developer = ''
            if 'Developer:' in keys:
                developer = maindict['Developer:']
    
            genre = ''
            if 'Genre:' in keys:
                genre = maindict['Genre:']
    
            releasedate = ''
            regionrelease = ''
            gameyear = ''
            if 'Release Date:' in keys:
                releasedate = maindict['Release Date:']
                if '(more)' in releasedate:
                    releasedate = releasedate[:-7]
                    morelink = page.pq('a').filter(lambda i: pq(this).text() == '(more)').attr('href')
                    multidate.append([title,platform,x,morelink])
                if '(' in releasedate:
                    dnum = releasedate.index('(')
                    regionrelease = releasedate[dnum+1:-1]
                    releasedate = releasedate[:dnum]
                if releasedate:
                    if not 'ancel' in releasedate and not 'TBA' in releasedate and not 'n/a' in releasedate and not releasedate: # exclude canceled, TBA, n/a, and empty
                        gameyear = yeargrab(releasedate)
    
            esrb = ''
            if 'ESRB:' in keys:
                esrb = maindict['ESRB:']
    
            esrbdetail = ''
            if 'ESRB Descriptors:' in keys:
                esrbdetail = maindict['ESRB Descriptors:']
        
            copyprotection = ''
            if 'Copy Protection:' in keys:
                copyprotection = maindict['Copy Protection:']
    
            # start Game Information modules section grab
            infomod = page.pq('#tech_info .body .module')
            
            # check Gameinfo availability
            if infomod.filter(lambda i:'Game Information' in pq(this).text())('.body').text():
                info.append(x)
            # check Technical Support availability
            #if infomod.filter(lambda i:'Technical Support' in pq(this).text())('.body').text():
            #    pass
            # check Official Site availability
            #if infomod.filter(lambda i:'Official Site' in pq(this).text())('.body').text():
            #    pass
    
            gstechinfodata.append([title,platform,developer,genre,releasedate,gameyear,regionrelease,esrb,esrbdetail,copyprotection])
    
            # check Credits availability
            if infomod.filter(lambda i:'Credits' in pq(this).text())('.body').text():
                tabledata = infomod.filter(lambda i:'Credits' in pq(this).text())('div.body table tr')
                length = len(tabledata)
                record = []
                for z in range(length):
                    designation = strip_accents(tabledata.eq(z)('th').text())
                    devname = strip_accents(tabledata.eq(z)('td').text())
                    record.append([devname,designation])
                for a in record:
                    gsdevlist.append(a + [title] + [platform] + [developer] + [releasedate] + [gameyear])
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Completed gamespot individual game tech page grab in " + elapse)
    print "Time elapsed " + elapse

######
# Scrape gamespot critic page
######
def gsindvcritic(listing=''):
    writelog("Starting Gamespot individual game critic page grab")
    start = time()
    listing = set(gscritic)
    global bin404
    bin404 = []
    for x in listing:
        try:
            page = Webpage(x)
            if page:
                page.pq.make_links_absolute('http://www.gamespot.com')
            else:
                bin404.append(x)
                pass
        except KeyboardInterrupt:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog('keyboard interrupt after ' + elapse)
            raise
        except:
            end = time()
            elapse = str(td(seconds = end - start))
            writelog('error occurred')
            raise
    elapse = str(td(seconds = end - start))
    writelog("Completed gamespot individual game critic page grab in " + elapse)
    print "Time elapsed " + elapse
#################### Miscellaneous ####################


######
# retry script
######

def scraperun(func):
    """Run a loop with URLError recovery. Input function name without the () call"""
    try:
        func()
    except urllib2.URLError, (err):
        print ("URL error(%s)" % (err))
        writelog(str(err) + "| Error, retrying...")
        print ("Retrying...")
        scraperun(func)
    except:
        writelog("Error, process stopped")
        raise
    
###
# Delete Cache
###

def deletecache(list,urlstr=''):
    """delete cached data. Input form (list,[urlstr])"""
    for x in list:
        count = 0
        try:
            url = "http://www.mobygames.com"+str(x)+str(urlstr)
            url_hash = hashlib.sha1(url).hexdigest()
            os.remove("cache/%s.txt" % url_hash)
            count += 1
            print ("removed "+url)
        except OSError:
            pass


######
# Check for complete html
######

def htmlcheck(urllist,urlstr=''):
    print "Checking html completeness"
    writelog ("Running html check for completeness.")
    start = time()
    global badhtml
    badhtml = []
    good = 0
    bad = 0
    print ("Total: " + str(len(urllist)))
    for x in urllist:
        url = str(x)
        #print ("checking "+ url)
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f = open("cache/%s.txt" % url_hash, 'r')
            y = pq(f.read())
            if "</body>" in y.html():
                good += 1
            else:
                badhtml.append(url)
                bad += 1
        except KeyboardInterrupt:
            raise
        except:
            pass
    end = time()
    elapse = str(td(seconds = end - start))
    writelog("Finised html check in: "+ elapse)
    print ("Good: " + str(good))
    print ("Bad: " + str(bad))
    print ("Finished check in" + elapse)

######
# re-scrape bad html
######

def rescrape(list,urlstr=''):
    for x in list:
        url = x
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            f.close()
        except IOError:
            while True:  # Unlimited tries to pull data
                try:
                    resp = urllib2.urlopen(url).read()
                    f = open("cache/%s.txt" % url_hash, 'w')
                    f.write(resp)
                    break
                except urllib2.URLError, (err):
                    print ("URL error(%s)" % (err))
                    writelog(str(err) + "| Error, retrying...")
                    print ("Retrying...")
                    pass
                except:
                    pass
            print "done "+str(url)
        except:
            raise

def webscrape(url):
    print ("scraping new html of "+url)
    url_hash = hashlib.sha1(url).hexdigest()
    resp = urllib2.urlopen(url).read()
    f = open("cache/%s.txt" % url_hash, 'w')
    f.write(resp)
    print ("done "+url)

######
# get cached name of url
######

def cachename(url):
    url_hash = hashlib.sha1(url).hexdigest()
    return ("%s.txt" % url_hash)

######
# get moby score voters number
######

def voters(footer_row):
    x = footer_row
    y = x[19:] # chop the front part of the string
    if 'votes' in y:
        return y[:-7]
    elif 'vote' in y:
        return y[:-6]
    else:
        raise IOError

######
# grab year
######

def yeargrab(strinput):
    year = strinput[-2:]
    if int(year)<15:
        yr = '20'+year
    if int(year)>40:
        yr = '19'+year
    return str(yr)
 


######
# Webpage class
######

class Webpage(object):
    def __init__(self, url, cache=True, retries=20):
        #constructor, takes a webpage
        self.url = url
        self.cache = cache
        self.retries = retries
        self.tries = 0
        self.pq = None

        print(url)
        self.url_hash = hashlib.sha1(url).hexdigest()

        #load from disk if it exists, if not fetch and store and disk
        if self.cache:
            try:
                f = open("cache/%s.txt" % self.url_hash)
                tmp = f.read()
            except IOError:
                tmp = self._get_url()
        else:
            tmp = self._get_url()

        #check if tmp contains anything
        if tmp:
            self.pq = pq(tmp)
        else:
            self.pq = None

    def _get_url(self):
        while True:
            try:
                if self.tries==self.retries:
                    return None
                resp = urllib2.urlopen(self.url).read()
                if self.cache:
                    f = open("cache/%s.txt" % self.url_hash, 'w')
                    f.write(resp)
                return resp
            except KeyboardInterrupt:
                raise
            except urllib2.HTTPError,e:
                if self.tries >= 3 and e.code == 404:
                    return None
                else:
                    self.tries += 1
                    pass
            except:
                self.tries += 1
                pass

    def pq_text(self, sel):
        #returns a list of text content
        return [x.text_content() for x in self.pq(sel)]

    def pq_links(self, sel):
        #returns a list of tuples of link text then link href
        return [(x.text_content(), x.attrib["href"]) for x in self.pq(sel)]

    def __nonzero__(self):
        #test if the webpage exists
        return self.pq!=None


######
# Greenpool parallel scrapint test
######

def parallelscrape(urllist,poolsize=50,retries=20,overwrite=False):
    import eventlet
    from eventlet.green import urllib2
    def fetch(url):
        tries = 0
        while True:
            try:
                print ('grabing ' + url)
                body = urllib2.urlopen(url).read()
                print ('grabbed' + url)
                return url, body
            except KeyboardInterrupt:
                raise
            except urllib2.HTTPError,e:
                if tries >= retries:
                    print ('failed '+url)
                    return None
                    tries += 1
                else:
                    tries += 1
                    pass

    if overwrite == True:
        urllist2 = urllist
    else:
        urllist2 = []
        print ('start check')
        for item in urllist:
            try:
                url_hash = hashlib.sha1(item).hexdigest()
                f = open('cache/%s.txt' % url_hash, 'r')
                f.close()
            except IOError:
                urllist2.append(item)
        print ('finished check')

    print ('Start scraping')
    pool = eventlet.GreenPool(poolsize)
    for url, body in pool.imap(fetch,urllist2):
        print ('writing cache')
        url_hash = hashlib.sha1(url).hexdigest()
        f = open('cache/%s.txt' % url_hash, 'w')
        f.write(body)
        print ('cached '+url)

