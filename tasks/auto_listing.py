file_path = 'C:/Users/Admin/Downloads/eclipse/Downloads/sw/data.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()

product_name = ""
seller_sku = ""
for line in lines:
    if line.startswith("name:"):
        product_name = line.split(':', 1)[1].strip()
    if line.startswith("sku:"):
        seller_sku = line.split(':', 1)[1].strip()

# set tên sản phẩm
def set_name(page):
    page.fill("//*[@id='preview-product-title']/div/div[1]/div/div/div/div/span/span/input", product_name)


# up hình sản phẩm
def upload_images(page):
    base_path = "C:/Users/Admin/Downloads/eclipse/Downloads/sw/"

    image_selectors = [
        f"//*[@id='main_image_item_{i}']/div/div/div[1]/input" for i in range(9)
    ]

    file_names = [
        "ash.png",
        "black.png",
        "forest_green.png",
        "light_pink.png",
        "light-blue.png",
        "red.png",
        "sand.png",
        "sport_grey.png",
        "white.png"
    ]

    image_paths = [f"{base_path}{file_name}" for file_name in file_names]

    for selector, path in zip(image_selectors, image_paths):
        page.set_input_files(selector, path)

# set thuộc tính sản phẩm
def set_product_attributes(page):
    div_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    popup_nums = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
    li_nums = [1, 2, 2, 1, 3, 2, 3, 2, 2, 1, 1, 3, 2, 1, 3, 3, 2, 2]

    for div_num, popup_num, li_num in zip(div_nums, popup_nums, li_nums):
        page.click(f'//*[@id="product_properties"]/div/div[1]/div[{div_num}]/div/div')
        page.click(f'//*[@id="theme-arco-select-popup-{popup_num}"]/div/div/li[{li_num}]')
    
    page.click('//*[@id="product_properties"]/div/div[2]')
    page.click('//*[@id="product_properties"]/div/div[1]/div[19]/div/div')
    page.click('//*[@id="theme-arco-select-popup-40"]/div/div/li[3]')

# mô tả
def set_description(page):
    page.fill('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[2]/input', product_name)

    page.click('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[2]/button')

    page.click('//*[@id="preview-product-description"]/div[2]/div[2]/div[1]/div[4]/button')

    page.set_input_files('//*[@id="preview-product-description"]/div[1]/div[2]/div/div/div/input', "C:/Users/Admin/Downloads/eclipse/Downloads/sw/white.png")

# danh mục
def set_categories(page):
    page.click('//*[@id="product-cascader-select-view"]')

    li_options = [5, 1, 5, 1]

    for index, li_num in enumerate(li_options):
        page.click(f'//*[@id="theme-arco-cascader-popup-0"]/div/div[2]/div/div[{index + 1}]/div/ul/li[{li_num}]')
    

# brand - thương hiệu
def set_brand(page):
    page.click('//*[@id="preview-product-brand"]/div[2]/div/div/div')
    page.click('//*[@id="theme-arco-select-popup-0"]/div/div/li[2]')

# Sales Information
def set_sale_infomation(page):
    base_path = "C:/Users/Admin/Downloads/eclipse/Downloads/sw/"
    input_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    file_names = [
        "sport_grey",
        "ash",
        "black",
        "forest_green",
        "light_pink",
        "light-blue",
        "red",
        "sand",
        "white"
    ]

    size_nums = [2, 3, 4, 5, 6, 7]
    size_names = ['S', 'M', 'L', 'XL', '2XL', '5XL']

    page.click('//*[@id="publish_enable_variation"]/div[1]/div/div/button')
    page.click('//*[@id="sale_properties"]/div/div[1]/div[2]/div/div')
    page.click('//*[@id="theme-arco-select-popup-45"]/div/div/li[2]')

    # color
    for file_name, input_num in zip(file_names, input_nums):
        page.set_input_files(
            f'//*[@id="sale_properties"]/div/div[3]/div[1]/div[{input_num}]/div/div[1]/div[1]/div/div/div[2]/input', 
            f'{base_path}{file_name}.png'
        )
        page.fill(
            f'//*[@id="sale_properties"]/div/div[3]/div[1]/div[{input_num}]/div/div[1]/div[2]/div/span/span/input', 
            file_name
        )
        page.click('//*[@id="sale_properties"]/div')

    page.click('//*[@id="sale_properties"]/div/div[3]/button')
    
    # size
    page.click('//*[@id="sale_properties"]/button')
    page.click('//*[@id="sale_properties"]/div[2]/div[1]/div[2]/div[1]/div')
    page.click('//*[@id="theme-arco-select-popup-55"]/div/div/li[1]')

    for size_name, size_num in zip(size_names, size_nums):
        page.fill(f'//*[@id="sale_properties"]/div[2]/div[3]/div[1]/div[{size_num}]/div/div[1]/div/div/span/span/input', size_name)
        page.click('//*[@id="sale_properties"]/div[2]')
    
    page.click('//*[@id="sale_properties"]/div[2]/div[3]/button')

def set_variations(page):
    page.click('//*[@id="skus"]/div[1]/div[2]/div/button')
    page.fill('//*[@id="skus"]/div[2]/div[2]/div[2]/div/span/span/input', '45')
    page.fill('//*[@id="skus"]/div[2]/div[3]/div/div/span/span/input', '50')
    page.fill('//*[@id="skus"]/div[2]/div[3]/div/div/span/span/input', '50')
    page.fill('//*[@id="skus"]/div[2]/div[4]/input', f'S_{seller_sku}')
    page.click('//*[@id="skus"]/div[2]/button')