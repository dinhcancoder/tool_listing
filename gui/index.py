import os
import PySimpleGUI as sg
import requests
from config.index import GOLOGIN_CONFIG

def get_profiles():
    url = "https://api.gologin.com/browser/v2"
    headers = {
        "Authorization": f"Bearer {GOLOGIN_CONFIG['token']}",
        "Content-Type": "application/json"
    }
    params = {
        "limit": 99
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        profiles = data.get("profiles", [])
        profile_data = [{"name": profile["name"], "id": profile["id"]} for profile in profiles if "name" in profile and "id" in profile]
        profile_names = [profile["name"] for profile in profile_data]
        return profile_data, profile_names
    else:
        sg.popup(f"Cannot get profile. error code: {response.status_code}")
        return [], []

def get_folder_profiles():
    url = "https://api.gologin.com/folders"
    headers = {
        "Authorization": f"Bearer {GOLOGIN_CONFIG['token']}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    associated_profiles = next((item['associatedProfiles'] for item in response_data if item['name'] == GOLOGIN_CONFIG['folder_name']), None)
    
    if not associated_profiles:
        print(f"Not found associated profiles trong folder '{GOLOGIN_CONFIG['folder_name']}'")
        return [], []

    profile_data = []
    for profile_id in associated_profiles:
        profile_url = f"https://api.gologin.com/browser/{profile_id}"
        profile_response = requests.get(profile_url, headers=headers)
        if profile_response.status_code == 200:
            profile = profile_response.json()
            if "name" in profile and "id" in profile:
                profile_data.append({"name": profile["name"], "id": profile["id"]})
        else:
            print(f"Failed get profile {profile_id}: {profile_response.status_code}")

    profile_data = [profile for profile in profile_data if profile['id'] not in GOLOGIN_CONFIG['excluded_profile_ids']]
    profile_names = [profile["name"] for profile in profile_data]
    return profile_data, profile_names

def show_gui():
    sg.theme("Reddit")
    sg.set_options(font=("SF Mono", 11))

    profile_data, profile_names = get_folder_profiles()

    layout_content = [
        [sg.Text("Automatically select required records", font=("Cascadia", 16), text_color="Black")],
        [sg.Text("Select Folder:"), sg.Input(key="folder_path", size=(54, 1)), sg.FolderBrowse(size=(12, 1))],
        [sg.Text("Type Duplicate:"), sg.Combo(['hoodie', 'sweatshirt', 't-shirt'], key="product_type", default_value='hoodie', size=(20, 1)), sg.Checkbox("Auto Desc", key="auto_desc"), sg.Checkbox("Is Style", key="is_style")],
        [sg.Listbox(values=profile_names, size=(82, 18), key="selected_profiles", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, enable_events=True)],
        [sg.Button("Submit", size=(10, 1)), sg.Button("Cancel", size=(10, 1))]
    ]

    layout = [
        [sg.Column(layout_content, size=(825, 510), scrollable=True, vertical_scroll_only=True)]
    ]

    window = sg.Window("Auto Listing Gologin Tiktok", layout, size=(825, 510))
    selected_ids = []
    folder_path = type_shirt = auto_desc = is_style = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Submit":
            selected_profiles = values["selected_profiles"]
            folder_path = values["folder_path"]
            type_shirt = values["product_type"]

            if not folder_path:
                sg.popup("Please select a folder!")
            elif not os.path.isdir(folder_path) or not any(os.path.isdir(os.path.join(folder_path, item)) for item in os.listdir(folder_path)):
                sg.popup("Empty folder with no products to tool!")
            elif not selected_profiles:
                sg.popup("Please select at least 1 profile!")
            else:
                selected_ids = [profile["id"] for profile in profile_data if profile["name"] in selected_profiles]
                window.close()
                break

    window.close()
    return selected_ids, folder_path, type_shirt