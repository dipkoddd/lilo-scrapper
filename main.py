from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from amazon.scrapper import AmazonScrapper
from config import MOCKED_NEWEGG_ITEM_ID
from microcenter.scrapper import MicroCenterScrapper
from new_egg.schema import NewEggItemData
from new_egg.scrapper import get_item_data_by_id
import undetected_chromedriver as uc

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--disable-webgl')
options.add_argument('--disable-accelerated-2d-canvas')
options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
service = Service(ChromeDriverManager().install())

new_egg_item_data_mocked = NewEggItemData(
    name="ASUS ROG Astral GeForce RTX 5090 32GB GDDR7 OC Edition ROG-ASTRAL-RTX5090-O32G-GAMING DLSS 4.0 PCI Express 5.0 Graphics Card",
    usd_price=123.45,
    gtin12="197105890299",
    mpn="ROG-ASTRAL-RTX5090-O32G-GAMING",
    model="ROG-ASTRAL-RTX5090-O32G-GAMING",
    link="None"
)

if __name__ == '__main__':
    driver = uc.Chrome(service=service, options=options)
    driver.set_window_size(2560, 1440)

    new_egg_item_id = input("Enter Item ID on newegg.com or just press enter:") or MOCKED_NEWEGG_ITEM_ID
    new_egg_result: NewEggItemData | None = get_item_data_by_id(driver, new_egg_item_id)

    if not new_egg_result:
        quit()

    # new_egg_result = new_egg_item_data_mocked

    amazon_scrapper = AmazonScrapper(driver=driver)
    amazon_search_result = amazon_scrapper.search_item(new_egg_result.mpn)

    microcenter_center = MicroCenterScrapper(driver=driver)
    microcenter_center_result = microcenter_center.search_item(search_text=new_egg_result.gtin12)

    print("NewEgg:\n")
    print(f"Item name: {new_egg_result.name}")
    print(f"Item price: ${new_egg_result.price_usd}")
    print(f"Item link: {new_egg_result.link}")

    print("\n\n")

    if len(amazon_search_result) > 0:
        print("Amazon:")
        for item in amazon_search_result:
            print(f"\nItem name: {item.name}")
            print(f"Item price: ${item.usd_price}")
            print(f"Item link: {item.link}")
    else:
        print("Not found on Amazon")

    print("\n\n")

    if microcenter_center_result:
        print("MicroCenter:\n")
        print(f"Item name: {microcenter_center_result.name}")
        print(f"Item price: ${microcenter_center_result.usd_price}")
        print(f"Item link: {microcenter_center_result.link}")

    else:
        print("Not found on MicroCenter")
