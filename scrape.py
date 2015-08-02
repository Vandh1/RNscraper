
# November 2014
#
# Start Date Scraper - scraper.py
#
# Scrapes the Rail Nation web forum for posts about server start dates
# Uses urllib to fetch the website, and beautifulsoup to parse
# Stores start dates in a sqlite3 database
#
# Used as a cronjob to automate the fetching of the start dates for use in a web page
#

from bs4 import BeautifulSoup
import re
from datetime import datetime, date, time
import urllib.request
import sqlite3

currentDate = datetime.now();

#Announcements URL
forumURL = 'http://forum.rail-nation.com/forumdisplay.php?f=510';

#Logging options
logging = True;
logfile = '/var/log/scraper.log';

if logging:
    log = open(logfile, 'a+')

serverStarts = {};

startsMetadata = {}; #'Interrail West' -> [Royal, 21, November, 2014, 01, 14]

monthsPT = {
    'Janeiro': 1,
    'Fevereiro': 2,
    'Março': 3,
    'Abril': 4,
    'Maio': 5,
    'Junho': 6,
    'Julho': 7,
    'Agosto': 8,
    'Setembro': 9,
    'Outubro': 10,
    'Novembro': 11,
    'Dezembro': 12
};

monthsEN = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
};

def convertDate(serverDate):
    year = serverDate.year;
    month = serverDate.month;
    day = serverDate.day;
    hour = -1;
    minutes = -1;
    try:
        hour = serverDate.hour;
        minutes = serverDate.minute;
    except AttributeError:
        pass;
    
    if day < 10: 
        day = "0"+str(day);
    else:
        day = str(day);

    if month < 10:
        month = "0"+str(month);
    else:
        month = str(month);

    if hour != -1 and hour < 10:
        hour = "0"+str(hour);
    else:
        if hour != -1:
            hour = str(hour);

    if minutes != -1 and minutes < 10:
        minutes = "0"+str(minutes);
    else:
        if minutes != -1:
            minutes = str(minutes);

    year = str(year);

    if hour != -1 and minutes != -1: 
        sqliteDate = year+"-"+month+"-"+day+" "+hour+":"+minutes;
    else:
        sqliteDate = year+"-"+month+"-"+day;
    return sqliteDate;



def writeToDB():
    conn = sqlite3.connect('/home/pedro/RNScraper/serverStarts.db');
    c = conn.cursor();
    c.execute('''CREATE TABLE IF NOT EXISTS starts (server TEXT PRIMARY KEY, startDate DATE, poster TEXT, announcementDate DATETIME)''');

    for server in serverStarts:
        startPostData = startsMetadata[server];
        serverDate = serverStarts[server];
        startDate = convertDate(serverDate);
        #print(startDate);
        announcementDate = startPostData[1];
        query = "SELECT * FROM starts WHERE server = ?";
        c.execute(query, (server,));
        row = c.fetchone();
        if row == None:
            c.execute("INSERT INTO starts VALUES (?,?,?,?)", (server,startDate,startPostData[0],announcementDate));
        else:
            dbDate = row[1];
            regexp = re.compile(r'([0-9]+)-([0-9]+)-([0-9]+)');
            match = regexp.search(dbDate);
            (year, month, day) = match.group(1,2,3);
            dbDate = date(int(year),int(month),int(day));
            if dbDate < serverDate:
                c.execute("UPDATE starts SET startDate = ?, poster = ?, announcementDate = ? WHERE server = ?",(serverDate, startPostData[0], announcementDate, server));
                if logging:
                    log.write(currentDate.strftime("%Y-%m-%d %H:%M:%S")+" Updated start time for "+server+" "+str(serverDate)+"\n");
            else:
                if logging:
                    log.write(currentDate.strftime("%Y-%m-%d %H:%M:%S")+" DB date is "+str(dbDate)+", server date is "+str(serverDate)+". DB already has the latest start date, nothing to do for "+server+".\n");
    conn.commit();
    conn.close();

def getServerStartDate(threadNumber):
    baseURL = "http://forum.rail-nation.com/printthread.php?t=";
    threadURL = baseURL+threadNumber;
    f = urllib.request.urlopen(threadURL);
    html = f.read();
    soup = BeautifulSoup(html);
    text = "";
    for tag in soup.find_all('div', class_="content"): #there is only one tag called blockquote in the printable version. If the vBulletin guys change their code around, this will be broken
        text = tag.blockquote.text;
        break;
    if text=="":
        raise Exception("Could not scrape the post text");
    else:
        regexp = re.compile(r'dia ([0-9]+) de ([Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro]+)');
        match = regexp.search(text);
        (startDay, startMonth) = (match.group(1),match.group(2));
        year = -1;
        if monthsPT[startMonth] <= currentDate.month:
            year = currentDate.year;
        else:
            year = currentDate.year-1;
        startDate = date(year, monthsPT[startMonth], int(startDay));

        return startDate; 
        
def getThreadNumber(link):
    regexp = re.compile(r'showthread.php\?t=([0-9]+)&s=[0-9a-z]');
    match = regexp.search(link);
    return match.group(1);


def findServerNameInTitle(title):
    regexp = re.compile("^Reinício do ([0-9A-Za-z\t .]+)");
    result=regexp.search(title);
    return result;

def getPostData(string):
    regexp_date = re.compile(r"^Started by ([0-9A-Za-z]+) on ([0-9]+). ([January|February|March|April|May|June|July|August|September|October|November|December]+) ([0-9]+) ([0-9]+):([0-9]+)");
    regexp_today = re.compile(r"^Started by ([0-9A-Za-z]+) on ([Yesterday|Today]+) ([0-9]+):([0-9]+)");

    
    match = regexp_date.search(string);

    if match != None:
    
        poster = match.group(1);
        day = match.group(2);
        month = match.group(3);
        year = match.group(4);
        hours = match.group(5);
        minutes = match.group(6);
    else:
        match = regexp_today.search(string);
        day = 0; #placeholder until we calculate it
        poster = match.group(1);
        dayString = match.group(2);
        hours = match.group(3);
        minutes = match.group(4);


        if dayString == "Yesterday": #a hora manhosa do forum esta 2h adiantada quando a lingua e en (default com wget), mas nao deve influenciar. se houver shenanigans na logica de verificar se um post e novo verificar isso!
            day = currentDate.day - 1;
        else:
            day = currentDate.day;
        month = currentDate.month;
        year = currentDate.year;

    return (poster,day,month,year,hours,minutes);


def main():
    f = urllib.request.urlopen(forumURL);
    html = f.read();
    
    soup = BeautifulSoup(html);

    for tag in soup.find_all('div', class_="inner"):
        match = findServerNameInTitle(tag.h3.a.string);
        
        if match != None:
            serverName = match.group(1);
            if serverName in serverStarts: #server was already found before, this is a restart for an earlier round, skip this thread
                continue;
            for datetag in tag.find_all('div', class_="author"):
                (poster,day,month,year,hours,minutes) = getPostData(datetag.span.a['title']);
               
                try: #if the posting date is in "yesterday"/"today" format, value will be numeric
                    month = int(month);
                except ValueError: #otherwise it will be a string ie "December"
                    month = monthsEN[month];
                announcementDate = datetime(int(year), month,int(day),int(hours),int(minutes));
                startsMetadata[serverName] = [poster,convertDate(announcementDate)];
                threadNumber = getThreadNumber(tag.h3.a['href']);
                startDate = getServerStartDate(threadNumber);
                serverStarts[serverName] = startDate;

        
    writeToDB();

    if logging:
        log.close();
    
    
if  __name__ =='__main__':main()





