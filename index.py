import os
import requests
import PySimpleGUI as sg
from playwright.sync_api import sync_playwright
from tools.auto_duplicate import initialize_browser, process_page, close_browser
from gologin import GoLogin
from config.index import GOLOGIN_CONFIG

sg.theme("Reddit")
sg.set_options(font=("Cascadia Code", 11))

url = "https://api.gologin.com/browser/v2"
headers = {
    "Authorization": f"Bearer {GOLOGIN_CONFIG['token']}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    profiles = data.get("profiles", [])
    profile_data = [{"name": profile["name"], "id": profile["id"]} for profile in profiles if "name" in profile and "id" in profile]
    profile_names = [profile["name"] for profile in profile_data]
else:
    sg.popup(f"Cannot get profile. error code: {response.status_code}")
    profile_data = []
    profile_names = []

layout = [
    [sg.Text("Automatically select required records", font=("Cascadia", 16), text_color="Black")],
    [sg.Listbox(values=profile_names, size=(60, 15), key="selected_profiles", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
    [sg.Button("Submit", size=(10, 1)), sg.Button("Cancel", size=(10, 1))]
]

window = sg.Window("Auto Listing Gologin Tiktok", layout, size=(600, 400))
selected_ids = []

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    elif event == "Submit":
        selected_profiles = values["selected_profiles"]
        if selected_profiles:
            selected_ids = [profile["id"] for profile in profile_data if profile["name"] in selected_profiles]
            window.close()
            break
        else:
            sg.popup("Please select at least 1 profile!")

window.close()

def main():
    if not selected_ids:
        return

    for profile_id in selected_ids:
        gl, debugger_address = initialize_browser(profile_id)

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(debugger_address)
            context = browser.contexts[0]
            page = context.pages[0]
            folder_path = 'D:/bind/listing'
            folders = os.listdir(folder_path)
            for folder_name in folders:
                process_page(page, folder_path, folder_name)

            close_browser(browser, gl)

if __name__ == "__main__":
    main()
