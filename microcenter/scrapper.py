from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from microcenter.schema import MicroCenterItemData


class MicroCenterScrapper:
    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver

        self.driver.get("https://www.microcenter.com/")

    def search_item(self, search_text: str) -> MicroCenterItemData | None:
        try:
            WebDriverWait(self.driver, 15).until(
                ec.presence_of_element_located((By.ID, "search-query"))
            )
            search_input_element = self.driver.find_element(By.ID, "search-query")
            search_input_element.send_keys(search_text)
            search_input_element.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, 15).until(
                ec.presence_of_element_located((By.ID, "hypProductH2_0"))
            )
            found_item = self.driver.find_element(By.ID, "hypProductH2_0")

            found_item_name = found_item.get_attribute("data-name")
            found_item_link = found_item.get_attribute("href")
            found_item_price = found_item.get_attribute("data-price")

            return MicroCenterItemData(name=found_item_name,
                                       usd_price=float(found_item_price) if found_item_price is not None else None,
                                       link=found_item_link)
        except Exception:  # noqa
            return None
