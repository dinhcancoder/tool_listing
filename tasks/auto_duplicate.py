import time
import os
import json
from utils.index import show_toast

def read_product_data(data_file_path):
    product_name = sku = price = quantity = description = ""

    with open(data_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('name:'):
                product_name = line.split('name:')[1].strip()
                is_description = False
            elif line.startswith('sku:'):
                sku = line.split('sku:')[1].strip()
                is_description = False
            elif line.startswith('price:'):
                price = line.split('price:')[1].strip()
                is_description = False
            elif line.startswith('quantity:'):
                quantity = line.split('quantity:')[1].strip()
                is_description = False
            elif line.startswith('description:'):
                description = line.split('description:')[1].strip()
                is_description = True
            elif is_description:
                description += f"\n{line.strip()}"

    return product_name, sku, quantity, price, description

def prepare_product_data(folder_path, folder_name):
    image_folder_path = os.path.join(folder_path, folder_name)
    data_file_path = os.path.join(folder_path, folder_name, 'data.txt')
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg'))]
    product_name, sku, price, quantity, description = read_product_data(data_file_path)

    return image_folder_path, data_file_path, image_files, product_name, sku, price, quantity, description

def remove_images(page):
    try:
        page.wait_for_selector('#preview-product-image > div > div.index__dndContainer--WQKEF > div:nth-child(2) .index__succeed--vbk4A')
        img_elements = page.query_selector_all('.index__succeed--vbk4A img[src^="https"]')
        img_length = len(img_elements)
        print(f'Số lượng hình hiện tại: {img_length}')

        for i in range(img_length):
            page.hover('//*[@id="main_image_item_0"]/div/div')
            page.click('//*[@id="main_image_item_0"]/div/div/div[1]/div[3]')
            img_elements = page.query_selector_all('.index__succeed--vbk4A img[src^="https"]')

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

def create_description_and_upload_image(page, image_files, image_folder_path, product_name, description):
    img_path_one = os.path.join(image_folder_path, image_files[0])
    img_path_two = os.path.join(image_folder_path, image_files[1])
    img_path_three = os.path.join(image_folder_path, image_files[2])
    arr_img = [img_path_one, img_path_two, img_path_three]
    
    try:
        if description:
            page.fill('//*[@id="preview-product-description"]/div[2]/div[2]/div[2]/div/div/div[2]', description)
        else:
            page.fill('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[2]/input', product_name)
            page.click('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[2]/button')
            page.click('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[4]/button')

        for img in arr_img:
            page.set_input_files('//*[@id="preview-product-description"]/div[2]/div[2]/div[2]/div/div/input', img)

        page.wait_for_function("""
            () => {
                const img = document.querySelector('#preview-product-description > div.relative.flex.mt-12 > div.w-full > div.index__container--aLzDH > div > div > div.ProseMirror mask img');
                return img && (img.src.startsWith('https') || img.src.startsWith('blob'));
            }
        """)

        time.sleep(3)
    except Exception as e:
        print("Error in create_description_and_upload_image, retrying...", e)

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
                print("Not found element to click.")

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

def set_variations(page, price, quantity, sku, is_style):
    try:
        page.click('//*[@id="skus"]/div[1]/div[2]/div/button')
        page.fill('//*[@id="skus"]/div[2]/div[4]/div[2]/div/span/span/input', price)
        page.fill('//*[@id="skus"]/div[2]/div[5]/div/div/span/span/input', quantity)
        
        if is_style:
            page.click('//*[@id="skus"]/div[2]/div[3]')
            page.wait_for_selector("body > div:nth-of-type(9) > span > div > div:first-child > div > div")

            # Duyệt qua từng tùy chọn kiểu, bỏ qua tùy chọn đầu tiên
            for index in range(1, len(page.query_selector_all("body > div:nth-of-type(9) > span > div > div:first-child > div > div > li"))):
                # Truy vấn lại `optionStyles` sau mỗi lần thao tác để đảm bảo phần tử vẫn tồn tại trong DOM
                optionStyles = page.query_selector_all("body > div:nth-of-type(9) > span > div > div:first-child > div > div > li")
                
                li = optionStyles[index]  # Lấy phần tử tại vị trí hiện tại

                # Lấy văn bản kiểu dáng và tạo SKU mới
                style_text = li.text_content()
                first_char = style_text[0]
                new_sku = f'{first_char}_{sku}'
                print(new_sku)

                # Thực hiện thao tác click và điền SKU
                li.click()
                page.wait_for_selector('//*[@id="skus"]/div[2]/div[6]/input')
                page.fill('//*[@id="skus"]/div[2]/div[6]/input', new_sku)

                # Nhấn nút lưu sau mỗi SKU
                page.click('//*[@id="skus"]/div[2]/button')

                # Mở lại danh sách kiểu dáng cho lần chọn tiếp theo
                page.click('//*[@id="skus"]/div[2]/div[3]')
                page.wait_for_selector("body > div:nth-of-type(9) > span > div > div:first-child > div > div")

            # Nhấn nút lưu sau khi hoàn thành vòng lặp
            page.click('//*[@id="skus"]/div[2]/button')

        else:
            page.fill('//*[@id="skus"]/div[2]/div[6]/input', sku)
            page.click('//*[@id="skus"]/div[2]/button')   

    except Exception as e:
        print("Error setting variations:", e)


def submit(page):
    try:
        time.sleep(20)
        print("done")
        # page.click('//*[@id="GEC-main"]/div[2]/div[1]/div/div/div[2]/div[4]/button')
        # page.wait_for_selector('//*[@id="GEC-main"]/div[2]/div[1]/span')
    except Exception as e:
        print("Error in submit:", e)


def run_tool(page, folder_path, folder_name, is_style):
    image_folder_path, data_file_path, image_files, product_name, sku, price, quantity, description = prepare_product_data(folder_path, folder_name)

    remove_images(page)
    load_images(page, image_files, image_folder_path)
    set_product_name(page, product_name)
    create_description_and_upload_image(page, image_files, image_folder_path, product_name, description)
    if not is_style:
        set_color_and_size(page, image_files, image_folder_path)
    set_variations(page, price, quantity, sku, is_style)
    submit(page)
