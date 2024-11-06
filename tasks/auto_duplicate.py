import time
import os
import json

def read_product_data(data_file_path):
    product_name = sku = price = quantity = ""

    with open(data_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('name:'):
                product_name = line.split('name:')[1].strip()
            if line.startswith('sku:'):
                sku = line.split('sku:')[1].strip()
            if line.startswith('price:'):
                price = line.split('price:')[1].strip()
            if line.startswith('quantity:'):
                quantity = line.split('quantity:')[1].strip()

    return product_name, sku, quantity, price

def prepare_product_data(folder_path, folder_name):
    image_folder_path = os.path.join(folder_path, folder_name)
    data_file_path = os.path.join(folder_path, folder_name, 'data.txt')
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg'))]
    product_name, sku, price, quantity = read_product_data(data_file_path)

    return image_folder_path, data_file_path, image_files, product_name, sku, price, quantity

def remove_images(page):
    try:
        page.wait_for_selector('.index__succeed--vbk4A img[src^="https"]')
        img_elements = page.query_selector_all('.index__succeed--vbk4A img[src^="https"]')
        img_length = len(img_elements)
        print(f'so luong 1: {img_length}')

        for i in range(img_length):
            page.hover('//*[@id="main_image_item_0"]/div/div')
            page.click('//*[@id="main_image_item_0"]/div/div/div[1]/div[3]')
    except Exception as e:
        print("Error in remove_images:", e)

def load_images(page, image_files, image_folder_path):
    for index, img_name in enumerate(image_files):
        img_path = os.path.join(image_folder_path, img_name)
        try:
            page.set_input_files(f'//*[@id="main_image_item_{index}"]/div/div/div[1]/input', img_path)
        except Exception as e:
            print(f"Error loading image {img_name}:", e)

def check_images_loaded(page, image_files):
    all_images_loaded = False
    while not all_images_loaded:
        all_images_loaded = True 
        for index in range(len(image_files)):
            img_xpath = f"//*[@id='sale_properties']/div[1]/div[3]/div[1]/div[{index + 1}]/div/div[1]/div[1]/div/div/div/div[2]/img"
            try:
                image_loaded = page.evaluate(f'''
                    () => {{
                        const element = document.evaluate("{img_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return element && element.src && element.src.length > 0;
                    }}
                ''')
                if not image_loaded:
                    all_images_loaded = False
                    break
            except Exception as e:
                print(f"Error checking image loaded for index {index}:", e)

def set_product_name(page, product_name):
    try:
        page.fill('//*[@id="preview-product-title"]/div/div[1]/div/div/div/div/span/span/input', product_name)
    except Exception as e:
        print("Error setting product name:", e)

def generate_description_and_upload_image(page, image_files, image_folder_path, product_name):
    try:
        page.fill('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[2]/input', product_name)
        page.click('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[2]/button')
        page.click('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[4]/button')
        first_img_name = image_files[0]
        img_path_one = os.path.join(image_folder_path, first_img_name)
        page.set_input_files('//*[@id="preview-product-description"]/div[1]/div[2]/div/div/div/input', img_path_one)
    except Exception as e:
        print("Error in create_description_and_upload_image:", e)

def format_image_name(img_name):
    formatted_name = img_name.replace('_', ' ')
    extensions = ['.png', '.jpg', '.jpeg', '.gif']
    
    for ext in extensions:
        if formatted_name.lower().endswith(ext):
            formatted_name = formatted_name[:-len(ext)]
            break

    return formatted_name.strip()

def set_color_and_size(page, image_files, image_folder_path):
    try:
        page.wait_for_selector('.index__iconUploadListStyle--p\\+nWF img[src^="https"]')
        img_elements = page.query_selector_all('.index__iconUploadListStyle--p\\+nWF img[src^="https"]')
        img_length = len(img_elements)

        print(f'so luong 2: {img_length}')

        for i in range(img_length - 1):
            page.wait_for_selector('#sale_properties > div:nth-child(1) > div.Property__Container-sc-16fbzyl-0.hYXwqd > div:nth-child(1) > div:nth-child(2) > div > div.absolute.right-0.flex.flex-row.h-36.top-0.items-center > svg.theme-arco-icon.theme-arco-icon-delete.w-16.h-16.mr-16.text-gray-3.fill-current.cursor-pointer')
            
            el = page.query_selector('#sale_properties > div:nth-child(1) > div.Property__Container-sc-16fbzyl-0.hYXwqd > div:nth-child(1) > div:nth-child(2) > div > div.absolute.right-0.flex.flex-row.h-36.top-0.items-center > svg.theme-arco-icon.theme-arco-icon-delete.w-16.h-16.mr-16.text-gray-3.fill-current.cursor-pointer')
            
            if el:
                el.click()
            else:
                print("Không tìm thấy phần tử để click.")

        page.hover('//*[@id="sale_properties"]/div[1]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div')
        page.click('//*[@id="sale_properties"]/div[1]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div/div/div[1]/div[2]')

        for index, img_name in enumerate(image_files):
            input_index = index + 2
            img_path = os.path.join(image_folder_path, img_name)
            page.set_input_files(f'//*[@id="sale_properties"]/div[1]/div[3]/div[1]/div[{input_index}]/div/div[1]/div[1]/div/div/div[2]/input', img_path)
            formatted_name = format_image_name(img_name)
            page.fill(f'//*[@id="sale_properties"]/div[1]/div[3]/div[1]/div[{input_index}]/div/div[1]/div[2]/div/span/span/input', formatted_name)
            page.wait_for_function(
                f"""
                () => {{
                    const img = document.querySelector('#sale_properties > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child({input_index}) > div > div:nth-child(1) > div:nth-child(1) > div > div > div > div:nth-child(2) > img');
                    return img && img.src.startsWith('blob');
                }}
                """
            )

            page.click('//*[@id="sale_properties"]/div[1]')

        page.click('//*[@id="sale_properties"]/div[1]/div[3]/button')
        page.click('//*[@id="sale_properties"]/div[2]/div[3]/button')
    except Exception as e:
        print("Error in set_color_and_size:", e)

def set_variations(page, price, quantity, sku):
    try:
        page.click('//*[@id="skus"]/div[1]/div[2]/div/button')
        page.fill('//*[@id="skus"]/div[2]/div[3]/div[2]/div/span/span/input', price)
        page.fill('//*[@id="skus"]/div[2]/div[4]/div/div/span/span/input', quantity)
        page.fill('//*[@id="skus"]/div[2]/div[5]/input', sku)
        page.click('//*[@id="skus"]/div[2]/button')
    except Exception as e:
        print("Error setting variations:", e)

def submit(page):
    try:
        page.click('//*[@id="GEC-main"]/div[2]/div[1]/div/div/div[2]/div[4]/button')
        page.wait_for_selector('//*[@id="GEC-main"]/div[2]/div[1]/span')
    except Exception as e:
        print("Error in submit:", e)

def run_tool(page, folder_path, folder_name):
    image_folder_path, data_file_path, image_files, product_name, sku, price, quantity = prepare_product_data(folder_path, folder_name)

    remove_images(page)
    load_images(page, image_files, image_folder_path)
    set_product_name(page, product_name)
    generate_description_and_upload_image(page, image_files, image_folder_path, product_name)
    set_color_and_size(page, image_files, image_folder_path)
    set_variations(page, price, quantity, sku)
    submit(page)
