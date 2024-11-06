import os
from playwright.sync_api import sync_playwright
from tools.auto_duplicate import initialize_browser, process_page, close_browser
from gui.index import show_gui

selected_ids, folder_path, type_shirt = show_gui()

def main():
    if not selected_ids or not folder_path:
        return

    for profile_id in selected_ids:
        gl, debugger_address = initialize_browser(profile_id)

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(debugger_address)
            context = browser.contexts[0]
            page = context.pages[0]
            folders = os.listdir(folder_path)
            for folder_name in folders:
                process_page(page, folder_path, folder_name, type_shirt)

            close_browser(browser, gl)

if __name__ == "__main__":
    main()