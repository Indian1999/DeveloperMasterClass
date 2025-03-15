from selenium import webdriver
from selenium.webdriver.common.by import By
import math
import json
import os

def remove_non_digit(string: str) -> int:
    """Removes every non digit character from the string, and returns an integer."""
    new_string = ""
    for char in string:
        if char.isdigit():
            new_string += char
    if new_string == "":
        return 0
    return int(new_string)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

driver.get("https://bazarosonline.hu/alex-store-hu/")

#"ty-mainbox-title__right"
num_of_products = driver.find_element(By.CSS_SELECTOR, "span.ty-mainbox-title__right").text
num_of_products = remove_non_digit(num_of_products)
num_of_pages = math.ceil(num_of_products / 50)

num_of_pages = 2 # felülírom, hogy ne 1 órág fésülgesse az oldalakat
products = []

for page_num in range(1, num_of_pages + 1):
    print(f"Scanning page no. {page_num}...")
    driver.get(f"https://bazarosonline.hu/alex-store-hu/?page={page_num}")
    
    results = driver.find_elements(By.CSS_SELECTOR, "div.ut2-gl__item")
    
    for result in results:
        try:
            product = {}
            product["title"] = result.find_element(By.CSS_SELECTOR, "a.product-title").text
            product["price"] = remove_non_digit(result.find_element(By.CSS_SELECTOR, "span.ty-price-num").text)
            product["currency"] = "HUF"
            product["img-url"] = result.find_element(By.TAG_NAME, "img").get_attribute("src")
            product["url"] = result.find_element(By.CSS_SELECTOR, "a.product_icon_lnk").get_attribute("href")
            product["page"] = page_num
            product["article-number"] = result.find_element(By.CSS_SELECTOR, "div.ut2--sku-text").text
            product["price-per-unit"] = None
            
            products.append(product)
        except Exception as ex:
            print("The program encountered an error!")
            print(ex)

driver.quit()

#Megadja annak a mappának az útvonalát, amiben fut az aktuális filunk
current_dir = os.path.dirname(os.path.abspath(__file__))
#Létrehozom a json file útvonalát:
file_path = os.path.join(current_dir, "products.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)