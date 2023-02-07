from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://signinssl.gmarket.co.kr/login/login?url=https://www.gmarket.co.kr/')

user_id = driver.find_element(By.ID, 'id')
user_id.send_keys('skdus3373')
user_pw = driver.find_element(By.ID, 'pwd')
user_pw.send_keys('zmfhffld12')

driver.find_element(By.CLASS_NAME, 'btn-login').click()
