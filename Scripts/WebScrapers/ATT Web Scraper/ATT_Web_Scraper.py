from selenium import webdriver
from bs4 import BeautifulSoup
import html5lib
import time
import requests
from influxdb import InfluxDBClient

# Declare webdriver options
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
options.add_argument('--disable-gpu')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=r'C:\chromedriver.exe')
print("Webdriver options declared")

# Read configuration file
mylines = []
with open ('config.ini', 'rt') as myfile:
    for myline in myfile:
        mylines.append(myline)

ATT_Username = (mylines[0])
ATT_Password = (mylines[1])
ATT_Account_Number = (mylines[2])
InfluxDB_IP_Address = (mylines[3])
InfluxDB_Port_Number = (mylines[4])
Database_Name = (mylines[5])
Authenticate = (mylines[6])
InfluxDB_Username = (mylines[7])
InfluxDB_Password = (mylines[8])

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

# Print config file variables
print("AT&T username: " + ATT_Username)
print("AT&T password redacted for security")
print("AT&T account number: " + ATT_Account_Number)
print("InfluxDB I.P. address: " + InfluxDB_IP_Address)
print("InfluxDB port: " + InfluxDB_Port_Number)
print("Database name: " + Database_Name)
print("InfluxDB username: " + InfluxDB_Username)
print("InfluxDB password redacted for security")
print("Using authentication? " + Authenticate)

# Log into and scrape the AT&T website
driver.implicitly_wait(10)
driver.get("https://www.att.com/my/")
print("Navigated to https://www.att.com/my/")

print("Waiting for page to load.")
time.sleep(10)
username = driver.find_element_by_id("userName")
print("username located")
password = driver.find_element_by_id("password")
print("password located")
username.send_keys(ATT_Username)
print("username entered")
time.sleep(1)
password.send_keys(ATT_Password)
print("password entered")
time.sleep(1)
driver.find_element_by_id("loginButton-lgwgLoginButton").click()
print("Login button clicked")
print("Waiting for page to load.")
time.sleep(10)
elementAttDueDate= driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/p[2]/span")
attDueDate = elementAttDueDate.text
attDueDate = attDueDate.replace('Pay by ', '')
print("Due date extracted from web page: " + attDueDate)
driver.get("https://www.att.com/olam/passthroughAction.myworld?actionType=UsageLanding&selectedBan=" + ATT_Account_Number)
print("navigating to bill page")
print("Waiting for page to load.")
time.sleep(10)
innerHTML = driver.execute_script("return document.body.innerHTML")
print("Extracted HTML body.")
time.sleep(3)
driver.find_element_by_xpath("//*[@id='divShortcut']/div[1]").click()
print("Clicked Date Select drop down menu.")
time.sleep(3)
driver.find_element_by_xpath("//*[@id='RecentUnbilled']/div[2]/a").click()
print("Clicked 'To present' in Date Selection dropdown menu.")

print("Formatting variables for Influx.")
soup = BeautifulSoup(innerHTML, 'html.parser')
time.sleep(1)
elementAttAmountDue= driver.find_element_by_xpath("//*[@id='content']/div[3]/div[1]/div[2]/span")
elementAttBandwidthUsed= driver.find_element_by_xpath("//*[@id='countlargenumbers']/span/strong")
attAmountDue = elementAttAmountDue.text
attBandwidthUsed = elementAttBandwidthUsed.text

attAmountDue = attAmountDue.replace('$', '')

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

print("Converting strings to integers.")

attAmountDue = attAmountDue[:attAmountDue.index('.')]
attAmountDue = int(attAmountDue)

attBandwidthUsed = attBandwidthUsed[:attBandwidthUsed.index('.')]
attBandwidthUsed = int(attBandwidthUsed)

print("Configuring JSON output")
# Configure JSON output for InfluxDB
json_body = [
    {
        "measurement": "ATT_Due_3",
        "tags": {
            "host": "AT&T"
        },
        "fields": {
            "value": attAmountDue
        },
        "measurement": "ATT_Due_Date_3",
        "tags": {
            "host": "AT&T"
        },
        "fields": {
            "value": attDueDate
        },
        "measurement": "ATT_Data_Usage_3",
        "tags": {
            "host": "AT&T"
        },
        "fields": {
            "value": attBandwidthUsed
        }
    }
]

# Post metrics to InfluxDB API
print("Connecting to InfluxDB API")
client = InfluxDBClient(InfluxDB_IP_Address, InfluxDB_Port_Number, InfluxDB_Username, InfluxDB_Password, Database_Name)
client.write_points(json_body)
result = client.query('select value from cpu_load_short;')

print("InfluxAPI request sent and accepted.")
print("Job complete.")

driver.quit()
