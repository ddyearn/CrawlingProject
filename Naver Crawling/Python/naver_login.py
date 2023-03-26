from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pandas import DataFrame
import time
import pyperclip


# 행사 리스트 : 상품명/판매할인가/할인율/링크
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('lang=ko_KR')

# infobar-chrome is being controlled by automated test software 제거 
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

user_id = 'bestsy777'
user_pw = 'muze2005;'

# 1. 네이버 이동
driver.get('http://naver.com')

# 2. 로그인 버튼 클릭
elem = driver.find_element(By.CLASS_NAME,'link_login')
elem.click()

''' headless 모드에서는 pyperclip 사용 불가
# 3. id 복사 붙여넣기
elem_id = driver.find_element(By.ID,'id')
elem_id.click()
pyperclip.copy(user_id)
elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 4. pw 복사 붙여넣기
elem_pw = driver.find_element(By.ID,'pw')
elem_pw.click()
pyperclip.copy(user_pw)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)
'''

# 자바스크립트로 입력
driver.execute_script(
    f"document.querySelector('input[id=\"id\"]').setAttribute('value', '{user_id}')"
)
time.sleep(1)
driver.execute_script(
    f"document.querySelector('input[id=\"pw\"]').setAttribute('value', '{user_pw}')"
)

# 5. 로그인 버튼 클릭
driver.find_element(By.ID,'log.login').click()

time.sleep(2)
# driver.find_element(By.CSS_SELECTOR, '#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix > li:nth-child(5) > a').click()
time.sleep(2)

# 6. html 정보 출력
f = open("naver_shopping.html", "w")
f.write(driver.page_source)
f.close()

# 7. 브라우저 종료
# browser.close() # 현재 탭만 종료
driver.quit() # 전체 브라우저 종료
