from flask import Flask
from discord_webhook import DiscordWebhook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def main():
    dates = []
    ## Code for Finding the Minimum Price for the Last 30 Days
    def SortMinimum():
        minimum = dates[0]
        for x in range(len(dates)):
            if dates[x+1]:
                if int(dates[x+1]) < int(dates[x]):
                    minimum = dates[x+1]
        return minimum
    ##Fetching 30 Cheapest Days of Cheapest Flight Prices
    for x in range(30):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        browser = webdriver.Chrome(PATH)
        browser.get('https://airlinezprice.netlify.app/')
        To= browser.find_element(By.ID,'box1')
        From= browser.find_element(By.ID,"box2")
        Departure_Date= browser.find_element(By.ID,"box3")
        Results_Count= browser.find_element(By.ID,"box4")
        To.send_keys("SEA")
        From.send_keys("LAX")
        Departure_Date.send_keys((datetime.strptime((datetime.now().strftime('%m-%d-%Y')),'%m-%d-%Y') + timedelta(days= x)).strftime('%m-%d-%Y'))
        Results_Count.send_keys("1")
        Results_Count.send_keys(Keys.RETURN)
        time.sleep(3)
        cheapest = browser.find_element(By.ID, "0")
        dates.append(cheapest)
    Minimum = SortMinimum()
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1009303429715333182/CjTAkOgzUb6p9llA85rVAW1UFQTrtvvdLgTXgzyTxLYadiBH_atvu2zglEWwozooNaNr', content= f'The cheapest price for the next 30 days is: {Minimum}')
    response = webhook.execute()    
    return "Done"
