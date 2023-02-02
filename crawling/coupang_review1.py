from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook
import pandas as pd
import time
import math

url = "https://www.coupang.com/vp/products/29528864?vendorItemId=3222696681&sourceType=SDP_ALSO_VIEWED&rmdId=e4655b075bca4d43a084d2fc95cb46d8&eventLabel=recommendation_widget_pc_sdp_001&platform=web&rmdABTestInfo=9266:C,10242:C,8534:A,8088:A,8091:A,9437:A&rmdValue=p1421463742:vt-1.0.0:p29528864&isAddedCart="

options = webdriver.ChromeOptions()
options.add_argument('--headless')
UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)   
time.sleep(5)

driver.find_element(By.CSS_SELECTOR, '.count').click()
time.sleep(5)

data_list = []
review_total = driver.find_element(By.CSS_SELECTOR, '.sdp-review__average__total-star__info-count').text
review_total = review_total.replace(",", "")
print(review_total)

review_per_page = 5
total_page = int(review_total) / review_per_page

total_page = math.ceil(total_page)
print(total_page)

product = driver.find_element(By.CSS_SELECTOR, '.prod-buy-header__title').text
print(product)

def get_page_data():
    users = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__info__user__name.js_reviewUserProfileImage')

    ratings = driver.find_elements(By.CSS_SELECTOR, '.sdp-review__article__list__info__product-info__star-orange.js_reviewArticleRatingValue')
        
    if len(users) == len(ratings):            
        for index in range(len(users)):
            data = {}
            data['username'] = users[index].text
            data['rating'] = int(ratings[index].get_attribute('data-rating'))
            print(data)
            data_list.append(data)

get_page_data() 
for page in range(1, total_page):
    try:
        print(str(page) + " page 수집 끝")

        button_index = page % 10 + 2

        driver.find_element(By.XPATH, '//*[@id="btfTab"]/ul[2]/li[2]/div/div[5]/section[4]/div[3]/button[' + str(button_index) +']').click()
        time.sleep(5)

        if(page % 10 == 0):
            driver.find_element(By.XPATH, '//*[@id="btfTab"]/ul[2]/li[2]/div/div[5]/section[4]/div[3]/button[12]').click()
            time.sleep(5)

        get_page_data()
    except:
        print("수집 에러")

print(str(page) + " page 수집 끝")
print("수집 종료")
    
driver.quit()
df = pd.DataFrame(data_list)
print(df)

# 엑셀로 저장
df.to_excel("./Coupang_Review.xlsx")
