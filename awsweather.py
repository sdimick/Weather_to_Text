import urllib2
from bs4 import BeautifulSoup
import smtplib

html = urllib2.urlopen('http://forecast.weather.gov/MapClick.php?lat=47.6152&lon=-122.3199&lg=english&&FcstType=digital')
soup = BeautifulSoup(html, 'html.parser')

table = soup.find_all("table")[7]

data = []

rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)
    
hours = []
temps = []
precips = []

for row in data:
    l = len(row)
    if row[0] == u'Hour (PST)':
        for i in row[1:l]:
            hours.append(i)

for row in data:
    l = len(row)
    if row[0] == u'Temperature (\xb0F)':
        for i in row[1:l]:
            temps.append(i)

for row in data:
    l = len(row)
    if row[0] == u'Precipitation Potential (%)':
        for i in row[1:l]:
            precips.append(i)

forecast = "HR TEMP PRECIP"
for i in range(24):
    forecast = forecast + "\n" + hours[i] + "     " + temps[i]  + "      " + precips[i] + "%"

fromaddr = "sdimickpythonweather@gmail.com"
toaddr = "9072527976@mms.att.net"

msg = "From: " + fromaddr + "\r\nTo: " + toaddr + "\r\n\r\n" + forecast

server = smtplib.SMTP( "email-smtp.us-west-2.amazonaws.com", 587 )
server.starttls()
server.login( 'AKIAJY4V7AALHCS7T5BA', 'AmrD4aqq10S91N2IWJHlWe7nV6jN4oyrEHopLYQIOtG9' )
server.sendmail( fromaddr, toaddr, msg )

exit()

            

