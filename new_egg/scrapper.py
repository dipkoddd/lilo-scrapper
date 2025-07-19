import json
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from new_egg.schema import NewEggItemData


def get_item_data_by_id(driver: WebDriver, item_id: str) -> NewEggItemData | None:
    driver.get(f"https://www.newegg.com/p/{item_id}")

    name: str | None = None
    gtin12: str | None = None
    mpn: str | None = None
    model: str | None = None

    try:
        not_found_item_element = driver.find_element(By.CLASS_NAME, "page-404-text")
        if "We can't find this Item" in not_found_item_element.text:
            print("ITEM ID NOT FOUND")
            driver.quit()
            return
    except Exception: # noqa
        pass

    page_content_element = driver.find_element(By.CLASS_NAME, "page-content")
    price = page_content_element.find_element(By.CLASS_NAME, "price-current")
    usd_price = float(price.text.replace("$", "").replace(",", ""))

    scripts = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')

    for script in scripts:
        try:
            data = json.loads(script.get_attribute("innerHTML"))

            if "name" in data:
                name = data.get("name")

            if "gtin12" in data:
                gtin12 = data.get("gtin12")

            if "mpn" in data:
                mpn = data.get("mpn")

            if "Model" in data:
                model = data.get("Model")

        except json.JSONDecodeError:
            continue

    return NewEggItemData(name=name, usd_price=usd_price, gtin12=gtin12, mpn=mpn, model=model, link=f"https://www.newegg.com/p/{item_id}")
