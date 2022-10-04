from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from lib.product_details import ProductDetailSearch
from lib.make_sub_csv import SaveColorCSVOfProduct


def ProductListSearch(driver, url, category_list):
    # driver = webdriver.Chrome("C:\Dev\chromedriver_win32\chromedriver.exe")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    # driver.implicitly_wait(2)

    pre_url = ""
    cur_url = url

    # 페지이 끝까지 돌기
    while pre_url != cur_url:
        product_lists = driver.find_elements(By.CSS_SELECTOR, "#listBody > li")
        # 제품목록에 있는 제품들 하나씩 접근
        for product in product_lists:
            # 한제품당 모든 컬러별 썸네일담을 list
            thumbnail_urls_of_product = []

            color_of_product = product.find_elements(
                By.CSS_SELECTOR, "div >.color_more_wrap > a")
            # 제품의 컬러별 썸네일 이미지 2개씩 담기
            for color in color_of_product:
                # 해당 물품의 컬러 클릭
                color.send_keys(Keys.ENTER)
                time.sleep(0.1)
                # 물건 컬러에 썸네일 2개를 긁어오기
                thumbnails_of_color = []
                product_thumbnail = product.find_elements(
                    By.CSS_SELECTOR, "div > a.item_info1 > span.item_img > img")
                thumbnails_of_color.append(
                    product_thumbnail[0].get_attribute('src'))
                thumbnails_of_color.append(
                    product_thumbnail[1].get_attribute('src'))

                thumbnail_urls_of_product.append(thumbnails_of_color)

                # color.click()

            product_brand_name = product.find_element(
                By.CLASS_NAME, "brand").text
            # 해당 제품의 상세정보 긁으러 가자~
            product_url = product.find_element(
                By.CSS_SELECTOR, "div > a").get_attribute('href')

            driver.switch_to.window(driver.window_handles[2])
            driver.get(product_url)
            time.sleep(0.1)
            try:
                ProductDetailSearch(
                    driver, product_brand_name, category_list, thumbnail_urls_of_product)
            except:
                print("상품디테일정보 긁어오기에서 실패했어요 ㅠㅠ")
            driver.switch_to.window(driver.window_handles[1])

            
        # 다음버튼 클릭
        pre_url = cur_url
        driver.find_element(
            By.CSS_SELECTOR, "#bodyWrap > div.adaptive_wrap > div.paging > a.next").click()

        time.sleep(0.2)
        cur_url = driver.current_url
    driver.switch_to.window(driver.window_handles[0])
