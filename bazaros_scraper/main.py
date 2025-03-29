from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import math
import json
import os
from pagebuilder import generate_div_string_from_dict, generate_html_from_template

def remove_non_digit(string: str) -> int:
    """Removes every non digit character from the string, and returns an integer."""
    new_string = ""
    for char in string:
        if char.isdigit():
            new_string += char
    if new_string == "":
        return 0
    return int(new_string)


vendor_link = "https://bazarosonline.hu/by-rozane-cosmetics-hu/"
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

driver.get(vendor_link)

#"ty-mainbox-title__right"
num_of_products = driver.find_element(By.CSS_SELECTOR, "span.ty-mainbox-title__right").text
num_of_products = remove_non_digit(num_of_products)
num_of_pages = math.ceil(num_of_products / 50)

num_of_pages = 2 # felülírom, hogy ne 1 órág fésülgesse az oldalakat
products = []

for page_num in range(1, num_of_pages + 1):
    print(f"Scanning page no. {page_num}...")
    driver.get(f"{vendor_link}?page={page_num}")
    
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
            try:
                product["minimum-order"] = int(result.find_element(By.CLASS_NAME, "cm-amount").get_attribute("value"))
            except:   
                try:
                    dropdown = result.find_element(By.CSS_SELECTOR, "select[name*='amount']")
                    select = Select(dropdown)
                    quantities = [int(option.get_attribute("value")) for option in select.options]
                    product["minimum"] = min(quantities)
                except:
                    product["minimum-order"] = None
            
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
    
div_strings = []
for elem in products:
    div_strings.append(generate_div_string_from_dict(elem))

template_path = os.path.join(current_dir, "template.html")
destination_path = os.path.join(current_dir, "by_rozane.html")
generate_html_from_template(template_path, destination_path, div_strings)
    
    