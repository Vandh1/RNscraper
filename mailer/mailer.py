import sqlite3
from datetime import datetime
from datetime import timedelta
from datetime import date
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

#startsDatabase = "/home/pedro/RNScraper/serverStarts.db"
#emailFile = "/home/pedro/RNScraper/mailer/sendto"
#emailDatabase = "/home/pedro/RNScraper/mailer/mailer.db"

dbConnections = {
    'starts': '/home/pedro/RNScraper/serverStarts.db',
    'emails': '/home/pedro/RNScraper/mailer/mailer.db'
}

starts = {} 
emails = []

#Logging options
logging = True;
logfile = '/var/log/scraper.log';

if logging:
    log = open(logfile, 'a+')

def getEndgameStartsToday():
    endgameServers = []
    for key in starts:
#        currentDate = date(2015,9,9);
        currentDate = datetime.now()
        start = starts[key].split(sep="-")
        start = date(int(start[0]),int(start[1]),int(start[2]))#.strftime('%Y-%m-%d')
        endgame = start + timedelta(days=84)
        endgame = endgame.strftime('%Y-%m-%d')
        currentDate = currentDate.strftime('%Y-%m-%d')
        print(currentDate)
        print(endgame)
        if currentDate == endgame:
            log.write(currentDate+" Mailer: Endgame for "+key+" starts today - sending mail\n");
            print("Dates are the same - server "+key+" added");
            endgameServers.append(key)
        else:
            print("Dates are different");
    if endgameServers == []:
        log.write(currentDate+" Mailer: No endgame starts today, postmaster is on holiday\n");
    return endgameServers

def dbFetch():
    
    for db in dbConnections:
        conn = sqlite3.connect(dbConnections[db])
        c = conn.cursor()
        
        if db == 'starts':
            c.execute('''CREATE TABLE IF NOT EXISTS starts (server TEXT PRIMARY KEY, startDate DATE, poster TEXT, announcementDate DATETIME)''');
            query = "SELECT * FROM starts"
            for row in c.execute(query):
                start = row[1]
                starts[row[0]] = start
        else:
            c.execute('''CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, isEnabled INTEGER)''');
            query = "SELECT * FROM emails"
            for row in c.execute(query):
                if row[3] == 1: #if sending to this email is not disabled
                    emails.append(row[2]) # id | name | email | isEnabled (bool int flag)
                else:
                    print("Email with id "+str(row[0])+" is disabled, skipping...")
        conn.close()
    
def sendmail(endgameServers):
        
    for server in endgameServers:
        for email in emails:
            print("Sending e-mail to "+email)
                
            msg = MIMEText("Hello,\n\nThe endgame for server "+server+" starts today.\n\nCheers,\nPimpzmaizcatz Technology Services")
            msg["From"] = "no-reply@pieinthesky.xyz"
            msg["To"] = email
            msg["Subject"] = server+" endgame starts today"
            p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
            p.communicate(bytes(msg.as_string(), 'UTF-8'))
    
def main():
    dbFetch()
    endgameServers = getEndgameStartsToday()
    sendmail(endgameServers)
        
if  __name__ =='__main__':main()
