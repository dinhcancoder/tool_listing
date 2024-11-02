from playwright.sync_api import sync_playwright
from tools.auto_listing import initialize_browser, process_page, close_browser

def main():
    gl, debugger_address = initialize_browser()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(debugger_address)
        context = browser.contexts[0]
        page = context.pages[0]

        process_page(page)

        close_browser(browser, gl)

if __name__ == "__main__":
    main()
