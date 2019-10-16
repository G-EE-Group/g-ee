from selenium import webdriver
from bs4 import BeautifulSoup
import html5lib
import time
import requests

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
options.add_argument('--disable-gpu')
#options.add_argument('--headless')
# ***********************************************
# Be sure to add the path to your chromedriver: *
# ***********************************************
driver = webdriver.Chrome(options=options, executable_path=r'C:\chromedriver.exe')

driver.implicitly_wait(10)

driver.get("https://www.att.com/my/")
print("Navigated to https://www.att.com/my/")
time.sleep(1)

time.sleep(10)
username = driver.find_element_by_id("userName")
print("username located")
time.sleep(1)
password = driver.find_element_by_id("password")
print("password located")
# ***********************************************
# Add your AT&T Username/Email address here:    *
# ***********************************************
username.send_keys("USERNAME")
print("username entered")
time.sleep(1)
# ***********************************************
# Add your AT&T password here:                  *
# ***********************************************
password.send_keys("PASSWORD")
print("password entered")
time.sleep(1)
driver.find_element_by_id("loginButton-lgwgLoginButton").click()
print("Login button clicked")
time.sleep(20)
elementAttDueDate = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/p[2]/span")
print("Located Due Date field")
time.sleep(1)
attDueDate = elementAttDueDate.text
attDueDate = attDueDate.replace('Pay by ', '')
# ************************************************************
# Add your AT&T account number at the end of the line below: *
# ************************************************************
driver.get("https://www.att.com/olam/passthroughAction.myworld?actionType=UsageLanding&selectedBan=ATTACCOUNTNUMBER")
print("navigated to bill page")
time.sleep(10)
innerHTML = driver.execute_script("return document.body.innerHTML")
time.sleep(3)
time.sleep(3)
driver.find_element_by_xpath("//*[@id='divShortcut']/div[1]").click()
time.sleep(3)
driver.find_element_by_xpath("//*[@id='RecentUnbilled']/div[2]/a").click()

soup = BeautifulSoup(innerHTML, 'html.parser')
time.sleep(1)
elementAttAmountDue = driver.find_element_by_xpath("//*[@id='content']/div[3]/div[1]/div[2]/span")
print("Located Amount Due field")
time.sleep(1)
elementAttBandwidthUsed = driver.find_element_by_xpath("//*[@id='countlargenumbers']/span/strong")
print("Located Bandwidth Quota field")
time.sleep(1)
attAmountDue = elementAttAmountDue.text
attBandwidthUsed = elementAttBandwidthUsed.text

attAmountDue = attAmountDue.replace('$', '')

print("Amount due: " + attAmountDue)
print("Bandwidth used: " + attBandwidthUsed + " Gb")
print("Due date: " + attDueDate)

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
