from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from pandas import DataFrame
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("http://corners.gmarket.co.kr/Bestsellers")
time.sleep(10)

titleList = []
itemList = []
priceList = []
urlList = []

lists = driver.find_elements(By.CLASS_NAME, 'best-list')[0]
lis = lists.find_elements(By.TAG_NAME, 'li')

for li in lis:
    title = li.find_element(By.TAG_NAME, 'p').text
    item = li.find_element(By.CLASS_NAME, 'itemname').text
    price = li.find_element(By.CLASS_NAME, 's-price').text
    url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

    titleList.append(title)
    itemList.append(item)
    priceList.append(price)
    urlList.append(url)

dic = {'title' : titleList, 'item' : itemList, 'price' : priceList, 'url' : urlList}
Gmarket_Bestseller_df = pd.DataFrame(dic)
Gmarket_Bestseller_df.to_csv('./Gmarket_Bestseller.xlsx')
driver.quit()
