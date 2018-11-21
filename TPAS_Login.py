from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup as soup
import requests, re, time, csv, os
import CREDENTIALS
import pandas as pd
#Add comment
def site_login(UN, Pass):
        driver = webdriver.Chrome(executable_path= CREDENTIALS.LOCATION + 'chromedriver.exe')
        driver.get ('https://studio2.innovid.com/analytics/campaigns.php')
        driver.maximize_window()
        driver.find_element_by_id('username').send_keys(UN)
        driver.find_element_by_id ('user_pass').send_keys(Pass)
        driver.find_element_by_id('signin-button').click()
        time.sleep(5)
        driver.get('https://studio2.innovid.com/analytics/campaigns.php?dateRange=fromToFilter&fromDate=2018/10/1&toDate=2018/10/31')
        scrollPage(driver)
        crawler(driver)
        
def scrollPage(D):
        last_height = D.execute_script("return document.body.scrollHeight")
        while True:
                D.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #Wait to load page
                time.sleep(5)
                #Calculate new scroll height and compare with last scroll height
                new_height = D.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                        break
                last_height = new_height
                
def crawler(D):
    xml=soup(D.page_source, 'lxml')
    for tr in xml.findAll(True, {'class':re.compile("^(odd|even)$")}):
        result = cleaner(tr)
        if str(result[0]) == '.':
                collect.append(result[1:])
        else:
                collect.append(result)

def cleaner(str1):
        out = str1.text.strip()
        out = out.replace("'", '')
        out = out.replace(',', '')
        out = out.replace(' ','')
        out = out.replace('\n',' ')
        out = out.split()
        return out

def SaveToCSV(C,L):
        DF = pd.DataFrame(C)
        DF.to_csv(L + 'output.csv', index=False, header=False)

#############################################################################################
#LOCATION = os.path.dirname(os.path.abspath(__file__)) 
LOCATION = CREDENTIALS.LOCATION
collect = [['Campaign','First Tracked','Last Tracked','Impressions','CTR','Awareness','Engagement','Completion','Client']]

UN = CREDENTIALS.UN
PASS = CREDENTIALS.PASS
site_login(UN, PASS)
SaveToCSV(collect, LOCATION)