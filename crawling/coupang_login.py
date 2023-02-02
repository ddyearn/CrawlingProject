from selenium import webdriver
from fake_useragent import UserAgent
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
user_ag = UserAgent().random
options.add_argument('user-agent=%s'%user_ag)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("prefs", {"prfile.managed_default_content_setting.images": 2})
driver = webdriver.Chrome('chromedriver.exe', options=options)

# 크롤링 방지 설정을 undefined로 변경
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
})

url = 'https://login.coupang.com/login/login.pang'
driver.get(url=url)
time.sleep(2)

id_input = driver.find_element_by_xpath('//*[@id="login-email-input"]')
id_input.send_keys('skdus3373@naver.com')

pw_input = driver.find_element_by_xpath('//*[@id="login-password-input"]')
pw_input.send_keys('zmfhffld12')

driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[5]/button').click()
