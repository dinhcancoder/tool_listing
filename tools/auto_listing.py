from gologin import GoLogin
from playwright.sync_api import sync_playwright
import time
from config.index import GOLOGIN_CONFIG
from tasks.auto_listing import set_name, upload_images, set_product_attributes, set_description, set_categories, set_brand, set_sale_infomation, set_variations

def initialize_browser():
    gl = GoLogin(GOLOGIN_CONFIG)
    debugger_address = gl.start()
    if not debugger_address.startswith("http://"):
        debugger_address = f"http://{debugger_address}"
    return gl, debugger_address

def process_page(page):
    page.goto('https://seller-us.tiktok.com/product/create?shop_region=US', wait_until="domcontentloaded")
    page.wait_for_load_state('load', timeout=120000)

    try:
        # set danh mục
        set_categories(page)

        # set thương hiệu
        set_brand(page)

        # set tên sản phẩm
        set_name(page)

        # up hình sản phẩm
        upload_images(page)

        # set thuộc tính
        set_product_attributes(page)

        # description
        set_description(page)

        # set size & color
        set_sale_infomation(page)

        # set variations
        set_variations(page)

        pass

    except Exception as e:
        print(f"Đã có lỗi xảy ra: {e}")

def close_browser(browser, gl):
    time.sleep(1000)
    browser.close()
    gl.stop()
