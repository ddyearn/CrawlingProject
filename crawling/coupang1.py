from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException #element 요소 있는지 확인하고, 없으면 예외 처리해주는 용도
from openpyxl import Workbook
import time

wb = Workbook()                                       
ws = wb.create_sheet('식품')                         
wb.remove_sheet(wb['Sheet'])   #기본 default sheet 지우기
ws.append(['이름', '가격', '배송기한', '상세페이지'])
i = 1
while True:
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
    options.add_argument('user-agent=' + UserAgent)    #https://www.whatismybrowser.com/detect/what-is-my-user-agent/에서 본인 UserAgent 복사,붙여넣기

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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

    id_input = driver.find_element(By.XPATH, '//*[@id="login-email-input"]')
    id_input.send_keys('put id here')

    pw_input = driver.find_element(By.XPATH, '//*[@id="login-password-input"]')
    pw_input.send_keys('put pwd here')

    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[5]/button').click()

    driver.get(url='https://www.coupang.com/np/categories/194276?page=' + str(i))
    time.sleep(5)

    try:
        product = driver.find_element(By.ID, 'productList')
        lis = product.find_elements(By.CLASS_NAME, 'baby-product')
        print('*' * 50 + ' ' + str(i) + 'Page Start!' + ' ' + '*' * 50)

        for li in lis:
            try:
                product = li.find_element(By.CLASS_NAME, 'name').text
                price = li.find_element(By.CLASS_NAME, 'price-value').text
                delivery = li.find_element(By.CLASS_NAME, 'delivery').text
                url = li.find_element(By.CLASS_NAME, 'baby-product-link').get_attribute('href')

                print('Product:' + product)
                print('Price:' + price)
                print('Delivery:' + delivery)
                print('URL:' + url)

                ws.append([product, price, delivery, url])
            except Exception:
                pass

        print('*' * 50 + ' ' + str(i) + 'Page End!' + ' ' + '*' * 50)
        time.sleep(5)
        i += 1
        driver.quit()

    except NoSuchElementException: #Page에 해당 카테고리 제품이 없을 경우
        wb.save('./Coupang1_Product_Grocery_All.xlsx')
        wb.close()
        exit(0)
