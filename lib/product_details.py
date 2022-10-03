from selenium import webdriver
from selenium.webdriver.common.by import By

import re
import time

from lib.make_sub_csv import SaveColorCSVOfProduct, SaveDetailOfProduct


def ProductDetailSearch(driver,  product_brand_name, category_list, thumbnail_urls_of_product):
    # driver = webdriver.Chrome("C:\Dev\chromedriver_win32\chromedriver.exe")

    # driver.implicitly_wait(2)

    product_name = driver.find_element(
        By.CSS_SELECTOR, "#contentDiv > div.info > div:nth-child(1) > h4 > span").get_attribute("innerText")
    price = driver.find_element(By.ID, "productPrice").get_attribute("value")
    product_detail = driver.find_element(
        By.CSS_SELECTOR, "#contentDiv > div.info > div:nth-child(1) > div.prod-detail-con-box > div.round-style > p").get_attribute("innerText")
    fit_info = ""
    try:
        fit_info = driver.find_element(
            By.CSS_SELECTOR, "#contentDiv > div.info > div:nth-child(1) > div.prod-detail-con-box > div.fit-info > p").get_attribute("innerText")
    except:
        print(product_name+"는 피팅정보가 없네요")

    # size_li = driver.find_elements(
    #     By.CSS_SELECTOR, "#color_size > ul > li:nth-child(2) > span.txt > ul > li")

    product_id = ""
    item = ""
    Material = ""
    color = ""
    size = ""
    country = ""
    manufacturer = ""
    manufacturer_ym = ""

    dt_tags = driver.find_elements(By.CSS_SELECTOR, ".toggle_type1 > dt")

    # 상품정보제공고시 위치가 매번달라서 위치 번호를 알아내고 상품정보제공고시에 있는 정보들 뺴오자
    for idx, dt_tag in enumerate(dt_tags):
        if dt_tag.find_element(By.CSS_SELECTOR, "dt > a").text == "상품정보제공고시":
            prod_info = driver.find_element(
                By.XPATH, f"//*[@id=\"contentDiv\"]/div[1]/dl/dd[{idx+1}]").get_attribute("innerText")
            prod_info = prod_info.splitlines()

            for info in prod_info:
                row = info.strip().split(":")
                if row[0].strip() == '상품품번':
                    product_id = row[1].strip()
                elif row[0].strip() == '품목':
                    item = row[1].strip()
                elif row[0].strip() == '소재':
                    Material = row[1].strip()
                elif row[0].strip() == '색상':
                    color = row[1].strip()
                elif row[0].strip() == '사이즈':
                    size = row[1].strip()
                elif row[0].strip() == '제조국':
                    country = row[1].strip()
                elif row[0].strip() == '제조사':
                    manufacturer = row[1].strip()
                elif row[0].strip() == '제조연월':
                    manufacturer_ym = row[1].strip()

    # size_li = []
    # sizes = driver.find_elements(
    #     By.CSS_SELECTOR, "#color_size > ul > li:nth-child(2) > span.txt > ul > li")
    # for s in sizes:
    #     size_li.append(s.find_element(By.CSS_SELECTOR,
    #                    "li > a").get_attribute("innerText"))
    size_li = []
    for s in size.split(','):
        size_li.append(s.strip())
    try:
        SaveColorCSVOfProduct(
            driver,
            product_id,
            thumbnail_urls_of_product,
            size_li
        )
    except:
        print('컬러에서 오류네')

    SaveDetailOfProduct(
        product_id,
        product_brand_name,
        category_list,
        product_name,
        price,
        product_detail,
        fit_info,
        # 여기서는 상품정보제공 고시 내용들
        item,
        Material,
        color,
        size,
        country,
        manufacturer,
        manufacturer_ym
    )
