from gologin import GoLogin
from playwright.sync_api import sync_playwright
from config.index import GOLOGIN_CONFIG
from tasks.auto_duplicate import run_tool
import time

def initialize_browser(profile_id):
    gl = GoLogin({
        "token": GOLOGIN_CONFIG['token'],
        "profile_id": profile_id
    })
    debugger_address = gl.start()
    if not debugger_address.startswith("http://"):
        debugger_address = f"http://{debugger_address}"
    return gl, debugger_address

def process_page(page, folder_path, folder_name):
    page.goto('https://seller-us.tiktok.com/product/create/1729677649988915313?online=1&tab=1', wait_until="domcontentloaded")
    page.wait_for_load_state('load', timeout=120000)

    try:

        run_tool(page, folder_path, folder_name)

        pass

    except Exception as e:
        print(f"An error has occurrend: {e}")

def close_browser(browser, gl):
    time.sleep(1000)
    browser.close()
    gl.stop()