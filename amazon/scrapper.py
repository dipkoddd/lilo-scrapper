from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from amazon.schema import AmazonItemData
from config import ACTION_COOLDOWN_FROM, ACTION_COOLDOWN_TO, MAX_AMAZON_LINKS_PER_REQUEST, AMAZON_POST_CODE
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class AmazonScrapper:
    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.is_location_set: bool = False

        self.driver.get("https://www.google.com/search?q=amazon")
        link_element = driver.find_element(By.XPATH, "//a[contains(@href, 'amazon.com')]")
        link_element.click()

        self.set_correct_location()

    def search_item(self, search_text: str) -> list[AmazonItemData]:
        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(ec.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
            search_input = self.driver.find_element(By.ID, "twotabsearchtextbox")
        except Exception: # noqa
            search_input = self.driver.find_element(By.ID, "nav-bb-search")

        search_input.send_keys(search_text)
        self.set_delay(1)
        search_input.send_keys(Keys.ENTER)

        self.set_correct_location()

        try:
            wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="listitem"]')))
            found_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
        except Exception: # noqa
            print("unable to find any items on Amazon")
            return

        links: list = []

        for item in found_items:
            asin = item.get_attribute("data-asin")

            if asin is None:
                continue

            try:
                sponsor_tags = item.find_elements(By.CSS_SELECTOR, "div.a-row.a-spacing-micro")

                if sponsor_tags > 0:
                    print("found sponsor tag, skipping...")
                    continue
            except Exception: # noqa
                pass

            if "No featured offers available" in item.text:
                print("found not available item, skipping...")
                continue

            link = f"https://www.amazon.com/dp/{asin}"
            links.append(link)

            if len(links) >= MAX_AMAZON_LINKS_PER_REQUEST:
                break

        items: list[AmazonItemData] = []

        for link in links:
            self.set_delay()
            item_data = self.get_item_data_by_link(link)
            items.append(item_data)

        return items

    def get_item_data_by_link(self, link: str) -> AmazonItemData:
        self.driver.get(link)

        name: str | None = None
        price: float | None = None

        try:
            name_element = self.driver.find_element(By.ID, "productTitle")
            name = name_element.text
        except Exception:  # noqa
            pass

        self.set_delay()

        try:
            price_element = self.driver.find_element(By.CLASS_NAME, "aok-offscreen")
            price = float(price_element.get_attribute('innerText').strip().replace("$", "").replace(",", ""))
        except Exception:  # noqa
            pass

        return AmazonItemData(name=name, usd_price=price, link=link)

    def set_correct_location(self):
        if self.is_location_set:
            return

        self.set_delay()

        try:
            location_bar = self.driver.find_element(By.ID, "nav-global-location-popover-link")
        except Exception: # noqa
            print("failed to find location bar")
            return

        if location_bar:
            location_bar.click()

            self.set_delay()

            try:
                zip_code_input = self.driver.find_element(By.ID, "GLUXZipUpdateInput")
                zip_code_input.send_keys(AMAZON_POST_CODE + Keys.ENTER)
            except Exception: # noqa
                print("failed to find zip code input")
                return

            self.set_delay()

            apply_button = self.driver.find_element(By.ID, "GLUXConfirmClose")
            self.driver.execute_script("arguments[0].click();", apply_button)

            self.is_location_set = True
            self.set_delay(5)

    @staticmethod
    def set_delay(time_seconds=random.randint(ACTION_COOLDOWN_FROM, ACTION_COOLDOWN_TO)):
        time.sleep(time_seconds)
