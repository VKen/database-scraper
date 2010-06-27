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
    global scrap
    num = range(0,list+1,25)
    print "Tracking "+str(list)+" games in moby database"
    print "Last page starts with : " + str(num[-1])
    scrap = []
'''
d = pq("http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/")
test = [x.attrib["href"] for x in d("#mof_object_list tbody a")]

for x in num:
    y = pq("http://www.mobygames.com/browse/games/offset,"+str(x)+"/so,0a/list-games/")
    scrap.append(y)
    print "done batch "+str(x)
'''

####
#### Grab moby URLs of individual Games
####
def scrapepage():
    """Populate scrap list with URLs of individual games"""
    print ("Populating moby game list...")
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
# Credit check
######
def credsubcheck(list):
    
    global suberr
    global suberr2
    global subweird
    global subcredinplace
    global subcredplatform

    suberr = []
    suberr2 = []
    subweird = []
    subcredinplace = []
    subcredplatform = []
    total = len(list)
    print ("total: " + str(total))
    creditcount = 0
    creditinplacecount = 0
    creditplatformcount = 0
    nocreditcount = 0
    other = 0
    for x in list:
        url = "http://www.mobygames.com"+str(x)
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
                    subcredplatform.append(cred)
                    creditplatformcount += 1
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
        f.close()
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

def scrapepage5():
    """scrape moby credits sub page ordering by developer"""
    writelog("starting mob game credit sub page scrape")
    start = time()
    for x in pc:
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
                stuff = x[i].attrib
                if not stuff: # check for header row
                    affiliation = x[i].text_content()
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
'''
for i in range(0,num):
    stuff = x[i].attrib
    if stuff == {}:
        print (x[i].text_content())
        affiliation = x[i].text_content()
    else:
        print (x[i][0].text_content()+" "+x[i][1].text_content()+" "+affiliation)
'''

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
    for x in scrap:
        url = "http://www.mobygames.com"+str(x)+"/techinfo"
        url_hash = hashlib.sha1(url).hexdigest()
        try:
            f=open("cache/%s.txt" % url_hash, 'r')
            #x=f.read()
            #y = pq(x)
        except IOError:
            print ("scraping new html of "+str(x))
            resp = urllib2.urlopen(url).read()
            f = open("cache/%s.txt" % url_hash, 'w')
            f.write(resp)
            print ("done "+str(x)+" techinfo")


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
    
##Test##
"""
for stuff in y("#mof_object_list tbody td"):
    if int(objcnt)%5 == 0:
        print stuff.text_content()
    objcnt += 1
"""
######################
# Unicode and CSV
######################
"""
import unicodedata

for x in gamename:
    if x is unicode:
        c.writerow(unicodedata.normalize('NKFD',x).encode('ascii','ignore'))
    else:
        c.writerow(x)
"""
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
    print x
"""
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

def htmlcheck(urllist):
    exec "badhtml = []"
    good = 0
    bad = 0
    print ("Total: " + str(len(credplatform)))
    for x in urllist:
        url = "http://www.mobygames.com"+str(x)
        #print ("checking "+ url)
        url_hash = hashlib.sha1(url).hexdigest()
        f = open("cache/%s.txt" % url_hash, 'r')
        y = pq(f.read())
        if "</body>" in y.html():
            good += 1
        else:
            badhtml.append(url)
            bad += 1
    print ("Good: " + str(good))
    print ("Bad: " + str(bad))


######
# re-scrape bad html
######

def rescrape():
    for url in badhtml:
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
        except:
            raise

def webscrape(url):
    print ("scraping new html of "+url)
    url_hash = hashlib.sha1(url).hexdigest()
    resp = urllib2.urlopen(url).read()
    f = open("cache/%s.txt" % url_hash, 'w')
    f.write(resp)
    print ("done "+url)

