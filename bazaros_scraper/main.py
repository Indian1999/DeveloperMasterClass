from selenium import webdriver
from selenium.webdriver.common.by import By

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
print(num_of_products)


driver.quit()