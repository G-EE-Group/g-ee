from selenium import webdriver
from bs4 import BeautifulSoup
import html5lib
import time
import requests

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
options.add_argument('--disable-gpu')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=r'C:\chromedriver.exe')

# **************************************************************
# Extract username, password and account number from config.ini*
# **************************************************************

mylines = []
with open ('config.ini', 'rt') as myfile:
    for myline in myfile:
        mylines.append(myline)

ATT_Username = (mylines[0])
ATT_Password = (mylines[1])
ATT_Account_Number = (mylines[2])

ATT_Username = ATT_Username.replace('AT&T Username = ', '')
ATT_Username = ATT_Username.replace('\n', '')
ATT_Username = ATT_Username.replace('\t', '')
ATT_Password = ATT_Password.replace('AT&T Password = ', '')
ATT_Password = ATT_Password.replace('\n', '')
ATT_Password = ATT_Password.replace('\t', '')
ATT_Account_Number = ATT_Account_Number.replace('AT&T Account Number = ', '')
ATT_Account_Number = ATT_Account_Number.replace('\n', '')
ATT_Account_Number = ATT_Account_Number.replace('\t', '')

# **********************************************
# Open AT&T web page and begin extracting data *
# **********************************************

driver.implicitly_wait(10)
driver.get("https://www.att.com/my/")

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
time.sleep(10)
elementAttDueDate= driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/p[2]/span")
attDueDate = elementAttDueDate.text
attDueDate = attDueDate.replace('Pay by ', '')
print(attDueDate)
driver.get("https://www.att.com/olam/passthroughAction.myworld?actionType=UsageLanding&selectedBan=" + ATT_Account_Number)
print("navigated to bill page")
time.sleep(10)
innerHTML = driver.execute_script("return document.body.innerHTML")
time.sleep(3)
driver.find_element_by_xpath("//*[@id='divShortcut']/div[1]").click()
time.sleep(3)
driver.find_element_by_xpath("//*[@id='RecentUnbilled']/div[2]/a").click()

soup = BeautifulSoup(innerHTML, 'html.parser')
time.sleep(1)
elementAttAmountDue= driver.find_element_by_xpath("//*[@id='content']/div[3]/div[1]/div[2]/span")
elementAttBandwidthUsed= driver.find_element_by_xpath("//*[@id='countlargenumbers']/span/strong")
attAmountDue = elementAttAmountDue.text
attBandwidthUsed = elementAttBandwidthUsed.text

attAmountDue = attAmountDue.replace('$', '')

print(attAmountDue)
print(attBandwidthUsed)
print(attDueDate)

line1 = ("# DML\\n")
line2 = ("\n")
line3 = ("# CONTEXT-DATABASE: telegraf")
line4 = ("\n")
line5 = ("\n")
line6 = ("dataUsage,host=att value=" + attBandwidthUsed)
line7 = ("\n")
line8 = ("ATT_Due,host=att value=" + attAmountDue)
line9 = ("ATT_Due_Date,host=att value=" + '"' + attDueDate + '"')

f1 = open('att_data_used.txt', 'w')
f2 = open('att_amount_due.txt', 'w')
f3 = open('att_due_date.txt', 'w')

f1.writelines([line1, line2, line3, line4, line5, line6, line7])
f2.writelines([line1, line2, line3, line4, line5, line8, line7])
f3.writelines([line1, line2, line3, line4, line5, line9, line7])

print("successfully output")

driver.quit()
