#I have this script run every morning at 5:05am to text me the 18 hour weather
#forecast for my zip code in Seattle.

#I scheduled it with crontab on a mac like this
#5 5 * * * python path/to/the/file/weathertotext.py

#For this script to work you need to install selenium, the chromedriver, and beautiful
#soup.
import smtplib
from selenium import webdriver
from bs4 import BeautifulSoup
import time

#Use selenium and the chromedriver to go to navigate to the hourly forecast online
#then import the html source as your soup for Beautiful Soup
driver = webdriver.Chrome('/Users/mvdimick/Documents/Seth/PythonDev/chromedriver/chromedriver')
driver.get("https://weather.weatherbug.com/forecasts/hourly/seattle-wa-98122")
driver.refresh()
html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')

#empty lists
hours = []
temps = []
newtemps = []
precip = []

#Use Beautiful soup to scrape the html for our weather info and store it in our lists
for element in soup('span', {'class' : 'hour'}):
    hours.append(str(element.contents[0]))

for element in soup('div', {'class' : 'temp'}):
    temps.append(element.contents[0])

for x in temps:
    newtemps.append(str(x.replace(u'\xa0', ' ').encode('utf-8')))

for element in soup('div', {'class' : 'precip'}):
    precip.append(str(''.join(element.find('span'))))


#From our lists of data, create strings that will be sent as text messages
forecast = "HOUR TEMP PRECIP"
for i in range(6):
    forecast = forecast + "\n" + " " + hours[i] + "   " + newtemps[i]  + "   " + precip[i]

forecast2 = "HOUR TEMP PRECIP"
for i in range(6, 12):
    forecast2 = forecast2 + "\n" + " " + hours[i] + "   " + newtemps[i]  + "   " + precip[i]


#Then log into an email account to send the text messages to a phone
#All phones are connected to an email with the following types of extensions:
#@vtext.com for Verizon
#@mms.att.net for AT&T

#I also put some sleep time between texts to make sure they come in the correct order
server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( '[youreamil]@gmail.com', '[yourpassword]' )
server.sendmail( 'Weather', '5555555555@mms.att.net', forecast ) #use your number
time.sleep(2)
server.sendmail( 'Weather', '5555555555@mms.att.net', forecast2 )

exit()
