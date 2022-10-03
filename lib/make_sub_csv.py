import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time


def SaveDetailOfProduct(product_id,
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
                        manufacturer_ym):
    with open(f'out/product_table.csv', 'a') as f:
        wr = csv.writer(f, lineterminator='\n')
        row = []
        row.append(product_id)
        row.append(product_brand_name)
        row.append(category_list[0])
        row.append(category_list[1])
        row.append(category_list[2])
        row.append(product_name)
        row.append(price)
        row.append(product_detail)
        row.append(fit_info)
        # 여기서는 상품정보제공 고시 내용들
        row.append(item)
        row.append(Material)
        row.append(color)
        row.append(size)
        row.append(country)
        row.append(manufacturer)
        row.append(manufacturer_ym)
        wr.writerow(row)


def SaveColorCSVOfProduct(driver, product_id, thumbnail_urls_of_product, size_li):
    color_li = driver.find_elements(
        By.XPATH, "//*[@id=\"color_size\"]/ul/li[1]/div/ul/li")

    # 미리 색상코드, 컬러이름, url을 다 긁은 후에 제품이미지들을 긁자
    color_codes = []
    color_names = []
    color_urls = []
    image_of_colors = []
    for l in color_li:
        # color code
        color_code = l.get_attribute("id")
        color_codes.append(color_code)
        # color 이름
        color_names.append(l.find_element(
            By.XPATH, f"//*[@id=\"{color_code}\"]/input").get_attribute("value"))
        # color의 url
        color_url = l.find_element(
            By.XPATH, f"//*[@id=\"{color_code}\"]/a").get_attribute("style")
        color_url = re.findall('"([^\']*)"', color_url)[0]
        color_urls.append(color_url)

    for color_code in color_codes:
        time.sleep(0.1)
        driver.find_element(
            By.XPATH, f"//*[@id=\"{color_code}\"]/a").send_keys(Keys.ENTER)
        time.sleep(1)

        product_imgs_of_color = driver.find_elements(
            By.CSS_SELECTOR, "#imageDiv > ul > li")
        images_of_color = []
        for idx, li_of_imageDiv in enumerate(product_imgs_of_color):
            if idx > 6:
                break
            images_of_color.append(li_of_imageDiv.find_element(
                By.TAG_NAME, "img").get_attribute("src"))
        image_of_colors.append(images_of_color)

        # size_table 저장하자
        SaveStockCSVOfProduct(product_id, color_code, size_li)

    with open(f'out/color_table.csv', 'a') as f:
        wr = csv.writer(f, lineterminator='\n')
        for i in range(len(color_codes)):
            row = []
            row.append(product_id)
            row.append(color_codes[i])
            row.append(color_names[i])
            row.append(color_urls[i])
            row = row+thumbnail_urls_of_product[i]
            row = row+image_of_colors[i]
            # 총 최대 13개 column 저장
            wr.writerow(row)


def SaveStockCSVOfProduct(product_id, color_code, size_li):
    with open(f'out/size_table.csv', 'a') as f:
        wr = csv.writer(f, lineterminator='\n')
        for size in size_li:
            row = []
            row.append(product_id)
            row.append(color_code)
            row.append(size)
            wr.writerow(row)
