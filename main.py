from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
from lib.prod_list import ProductListSearch


def app():
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])  # usb warning mesage 안나오게
    options.add_argument("--headless")  # 브라우저 뜨지 않고 실행
    options.add_argument('window-size=1400,1226')
    options.add_argument("--no-sandbox")  # Bypass OS security model
    # overcome limited resource problems
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        "C:\Dev\chromedriver_win32\chromedriver.exe", options=options)

    home_url = "http://www.thehandsome.com/ko"
    driver.get(home_url)
    driver.implicitly_wait(3)

    # 카테고리별 새창 하나 더 띄우기
    driver.execute_script("window.open()")
    # 상품detail 볼 새창 하나 더 띄우기
    driver.execute_script("window.open()")

    # l_category_name = "여성"
    # l_category_name = "남성"
    l_category_name = "잡화"
    # category l,m,s 수집
    # m_categorys = driver.find_elements(
    # By.CSS_SELECTOR, "#cate_m_main > li:nth-child(2) > div > div > ul> li")#여자
    # m_categorys = driver.find_elements(
    #     By.CSS_SELECTOR, "#cate_m_main > li:nth-child(3) > div > div > ul> li")  # 남자
    m_categorys = driver.find_elements(
        By.CSS_SELECTOR, "#cate_m_main > li:nth-child(4) > div > div > ul> li")  # 잡화
    for i in range(1, len(m_categorys)):
        m_category_name = m_categorys[i].find_element(
            By.TAG_NAME, 'a').get_attribute('innerHTML')
        s_categorys = driver.find_elements(
            By.CSS_SELECTOR, f"#cate_m_main > li:nth-child(4) > div > div > ul > li:nth-child({i+1}) > ul > li")
        for s_category in s_categorys:
            s_category_name = s_category.find_element(
                By.CSS_SELECTOR, 'li > a').get_attribute('innerText')

            get_url = s_category.find_element(
                By.TAG_NAME, 'a').get_attribute('href')

            next_url = home_url+get_url

            category_list = [
                l_category_name,
                m_category_name,
                s_category_name
            ]
            print('지금은' + category_list[0]+'/' +
                  category_list[1] + '/'+category_list[2] + '진행중~')
            # 목록 도는 함수 호출
            try:
                ProductListSearch(driver, next_url, category_list)
            except:
                print("목록 접근에서 실패했어요 ㅠㅠ")

    driver.close()


if __name__ == '__main__':
    app()
