# *******************************************************************
# * Created by Cameron McCloskey (2019)                             *
# * Hosted at https://github.com/alexandzors/g-ee                   *
# * Created for Grafana - Experts Exchange Facebook group           *
# * G-EE URL: https://www.facebook.com/groups/grafanaexchange/      *
# * Author's URL: https://www.facebook.com/darkhat.me               *
# *******************************************************************

from selenium import webdriver
from bs4 import BeautifulSoup
import html5lib
import time
import requests
from influxdb import InfluxDBClient
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
LOGGER.setLevel(logging.INFO)

logging.info('*********************BEGIN SCRAPING PROCESS.*********************')
logging.info('Setting config.ini as source config.')
# Read configuration file
mylines = []
with open('config.ini', 'rt') as myfile:
    for myline in myfile:
        mylines.append(myline)

logging.info('Setting config.ini lines as individual variables.')
ATT_Username = (mylines[0])
ATT_Password = (mylines[1])
ATT_Account_Number = (mylines[2])
InfluxDB_IP_Address = (mylines[3])
InfluxDB_Port_Number = (mylines[4])
Database_Name = (mylines[5])
Authenticate = (mylines[6])
InfluxDB_Username = (mylines[7])
InfluxDB_Password = (mylines[8])
Chromedriver_Location = (mylines[9])
Chromedriver_State_Headless = (mylines[10])

logging.info('Reading config.ini variables.')
Chromedriver_State_Headless = Chromedriver_State_Headless.replace('Run Chromedriver in headless mode?: ', '')
Chromedriver_State_Headless = Chromedriver_State_Headless.replace('\n', '')
Chromedriver_State_Headless = Chromedriver_State_Headless.replace('\t', '')
Authenticate = Authenticate.replace('Authenticate With Influx?: ', '')
Authenticate = Authenticate.replace('\n', '')
Authenticate = Authenticate.replace('\t', '')
ATT_Username = ATT_Username.replace('AT&T Username = ', '')
ATT_Username = ATT_Username.replace('\n', '')
ATT_Username = ATT_Username.replace('\t', '')
ATT_Password = ATT_Password.replace('AT&T Password = ', '')
ATT_Password = ATT_Password.replace('\n', '')
ATT_Password = ATT_Password.replace('\t', '')
ATT_Account_Number = ATT_Account_Number.replace('AT&T Account Number = ', '')
ATT_Account_Number = ATT_Account_Number.replace('\n', '')
ATT_Account_Number = ATT_Account_Number.replace('\t', '')
InfluxDB_IP_Address = InfluxDB_IP_Address.replace('InfluxDB Host IP Address: ', '')
InfluxDB_IP_Address = InfluxDB_IP_Address.replace('\n', '')
InfluxDB_IP_Address = InfluxDB_IP_Address.replace('\t', '')
InfluxDB_Port_Number = InfluxDB_Port_Number.replace('InfluxDB Host Port: ', '')
InfluxDB_Port_Number = InfluxDB_Port_Number.replace('\n', '')
InfluxDB_Port_Number = InfluxDB_Port_Number.replace('\t', '')
Database_Name = Database_Name.replace('Database Name: ', '')
Database_Name = Database_Name.replace('\n', '')
Database_Name = Database_Name.replace('\t', '')
Chromedriver_Location = Chromedriver_Location.replace('Chromedriver location: ', '')
Chromedriver_Location = Chromedriver_Location.replace('\n', '')
Chromedriver_Location = Chromedriver_Location.replace('\t', '')
Chromedriver_Location = ('"' + Chromedriver_Location + '"')
print("Chromedriver location: " + Chromedriver_Location)
print("Chrome state headless?: " + Chromedriver_State_Headless)

logging.info('Checking if InfluxDB authentication is required.')
# Check if InfluxDB authentication is required
if Authenticate == "true":
    InfluxDB_Username = InfluxDB_Username.replace('InfluxDB Username: ', '')
    InfluxDB_Username = InfluxDB_Username.replace('\n', '')
    InfluxDB_Username = InfluxDB_Username.replace('\t', '')
    InfluxDB_Password = InfluxDB_Password.replace('InfluxDB Password: ', '')
    InfluxDB_Password = InfluxDB_Password.replace('\n', '')
    InfluxDB_Password = InfluxDB_Password.replace('\t', '')
    print("This server REQUIRES authentication.")
elif Authenticate == "false":
    InfluxDB_Username = ''
    InfluxDB_Password = ''
    print("This server DOES NOT require authentication.")

logging.info('Declaring webdriver options.')
# Declare webdriver options
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
# Check if Chromedriver is configured to run in Headless mode or not
if Chromedriver_State_Headless == "true":
    options.add_argument("--headless")
    print("Chromedriver configured to run in headless mode")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options, executable_path=[Chromedriver_Location])
print("Webdriver options declared")
print("Chromedriver configured for headless operation?" + Chromedriver_State_Headless)
print(driver)

logging.info("VARIABLES: " + "username: " + ATT_Username + ", password redacted, " + "AT&T account number: " + ATT_Account_Number + ","
    " Influx host IP: " + InfluxDB_IP_Address + ", Influx port number: " + InfluxDB_Port_Number + ", using database: "
    + Database_Name + ", InfluxDB username: " + InfluxDB_Username + ", password redacted" + ", authentication? " +
    Authenticate + ", Chromedriver location: " + Chromedriver_Location)

# Print config file variables
print("InfluxDB I.P. address: " + InfluxDB_IP_Address)
print("InfluxDB port: " + InfluxDB_Port_Number)
print("Database name: " + Database_Name)
print("InfluxDB password redacted for security")
print("Using authentication? " + Authenticate)
print("Chromedriver located: " + Chromedriver_Location)

logging.info('Navigating to AT&T website.')
# Log into and scrape the AT&T website
driver.implicitly_wait(10)
driver.get("https://www.att.com/my/")
print("Navigated to https://www.att.com/my/")


logging.info('Waiting for page to load.')
print("Waiting for page to load.")
time.sleep(10)
username = driver.find_element_by_id("userName")
logging.info('Page loaded.')
print("Page loaded.")
logging.info('Username located.')
print("Username located")
password = driver.find_element_by_id("password")
logging.info('Password located.')
print("Password located")
username.send_keys(ATT_Username)
logging.info('Username entered.')
print("Username entered")
time.sleep(1)
password.send_keys(ATT_Password)
logging.info('Password entered.')
print("Password entered")
time.sleep(1)
driver.find_element_by_id("loginButton-lgwgLoginButton").click()
logging.info('Login button clicked.')
print("Login button clicked")
print("Waiting for page to load.")
time.sleep(10)
elementAttDueDate= driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/p[2]/span")
attDueDate = elementAttDueDate.text
attDueDate = attDueDate.replace('Pay by ', '')
logging.info("Due date extracted from web page: " + attDueDate)
print("Due date extracted from web page: " + attDueDate)
driver.get("https://www.att.com/olam/passthroughAction.myworld?actionType=UsageLanding&selectedBan=" + ATT_Account_Number)
logging.info('Navigated to bill page.')
print("navigating to bill page")
logging.info('Waiting for page to load.')
print("Waiting for page to load.")
time.sleep(10)
innerHTML = driver.execute_script("return document.body.innerHTML")
logging.info('Extracted HTML body.')
print("Extracted HTML body.")
time.sleep(3)
driver.find_element_by_xpath("//*[@id='divShortcut']/div[1]").click()
logging.info('Clicked Date Select drop down menu.')
print("Clicked Date Select drop down menu.")
time.sleep(3)
driver.find_element_by_xpath("//*[@id='RecentUnbilled']/div[2]/a").click()
logging.info('Clicked "To present" in Date Selection dropdown menu.')
print("Clicked 'To present' in Date Selection dropdown menu.")

print("Formatting variables for Influx.")
logging.info('Formatting variables for Influx.')
soup = BeautifulSoup(innerHTML, 'html.parser')
time.sleep(1)
elementAttAmountDue= driver.find_element_by_xpath("//*[@id='content']/div[3]/div[1]/div[2]/span")
elementAttBandwidthUsed= driver.find_element_by_xpath("//*[@id='countlargenumbers']/span/strong")
attAmountDue = elementAttAmountDue.text
attBandwidthUsed = elementAttBandwidthUsed.text

attAmountDue = attAmountDue.replace('$', '')

logging.info("METRICS EXTRACTED: ""Amount due: $" + attAmountDue + ", Data quota used: " + attBandwidthUsed + " Gb, Due date: " + attDueDate)
print("Amount due: " + attAmountDue)
print("Data quota used: " + attBandwidthUsed)
print("Due date: " + attDueDate)

# Uncomment these lines if you want an InfluxDB import text file generated for each variable.
# line1 = ("# DML\\n")
# line2 = ("\n")
# line3 = ("# CONTEXT-DATABASE: telegraf")
# line4 = ("\n")
# line5 = ("\n")
# line6 = ("dataUsage,host=att value=" + attBandwidthUsed)
# line7 = ("\n")
# line8 = ("ATT_Due,host=att value=" + attAmountDue)
# line9 = ("ATT_Due_Date,host=att value=" + '"' + attDueDate + '"')
# f1 = open('att_data_used.txt', 'w')
# f2 = open('att_amount_due.txt', 'w')
# f3 = open('att_due_date.txt', 'w')
# f1.writelines([line1, line2, line3, line4, line5, line6, line7])
# f2.writelines([line1, line2, line3, line4, line5, line8, line7])
# f3.writelines([line1, line2, line3, line4, line5, line9, line7])

logging.info('Converting strings to integers.')
print("Converting strings to integers.")

attAmountDue = attAmountDue[:attAmountDue.index('.')]
attAmountDue = int(attAmountDue)

attBandwidthUsed = attBandwidthUsed[:attBandwidthUsed.index('.')]
attBandwidthUsed = int(attBandwidthUsed)

logging.info('Configuring JSON output.')
print("Configuring JSON output")
# Configure JSON output for InfluxDB
json_body_1 = [
    {
        "measurement": "ATT_Amount_Due",
        "tags": {
            "host": "AT&T"
        },
        "fields": {
            "value": attAmountDue
        }
    }
]
json_body_2 = [
    {
        "measurement": "ATT_Bandwidth_Used",
        "tags": {
            "host": "AT&T"
        },
        "fields": {
            "value": attBandwidthUsed
        }
    }
]
json_body_3 = [
    {
        "measurement": "ATT_Date_Due",
        "tags": {
            "host": "AT&T"
        },
        "fields": {
            "value": attDueDate
        }
    }
]

# Post metrics to InfluxDB API
logging.info('Connecting to InfluxDB API.')
print("Connecting to InfluxDB API")
client = InfluxDBClient(InfluxDB_IP_Address, InfluxDB_Port_Number, InfluxDB_Username, InfluxDB_Password, Database_Name)
logging.info('Sending JSON metrics')
print('Sending JSON metrics')
client.write_points(json_body_1)
client.write_points(json_body_2)
client.write_points(json_body_3)
result = client.query('select value from ATT_Bandwidth_Used;')

logging.info('InfluxAPI request sent and accepted.')
print("InfluxAPI request sent and accepted.")
logging.info('Job complete.')
print("Job complete.")

driver.quit()
logging.info('Job quit.')
