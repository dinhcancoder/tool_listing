from gologin import GoLogin
from playwright.sync_api import sync_playwright
from config.index import GOLOGIN_CONFIG
from tasks.auto_duplicate import run_tool
import time

def initialize_browser(profile_id):
    gl = GoLogin({
        "token": GOLOGIN_CONFIG['token'],
        "profile_id": '66f78272cedbe2a47d9fc25a'
    })
    debugger_address = gl.start()
    if not debugger_address.startswith("http://"):
        debugger_address = f"http://{debugger_address}"
    return gl, debugger_address

def process_page(page, folder_path, folder_name, type_shirt, is_style):
    if type_shirt == "hoodie":
        page.goto(GOLOGIN_CONFIG['link_duplicate_hoodie'], wait_until="domcontentloaded")
        page.wait_for_load_state('load', timeout=120000)

    try:

        run_tool(page, folder_path, folder_name, is_style)

        pass

    except Exception as e:
        print(f"An error has occurrend: {e}")

def close_browser(browser, gl):
    time.sleep(2)
    browser.close()
    gl.stop()