from gologin import GoLogin
from playwright.sync_api import sync_playwright
import time

gl = GoLogin({
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NmY3ODRkMmJjZDIzZWVlMDUwZjUyNGIiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NzE4YzBhMTc2YThhZWNiOGEyMTc5NGUifQ.AKeuyGoOt-fWp_hpo2UoU_EeE9nz8BeBj8gQ93yhU5M",  
    "profile_id": "66f78272cedbe2a47d9fc25a", 
})

debugger_address = gl.start()
if not debugger_address.startswith("http://"):
    debugger_address = f"http://{debugger_address}"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(debugger_address)
    
    context = browser.contexts[0]
    page = context.pages[0]
    
    page.goto('https://seller-us.tiktok.com/product/create?shop_region=US', wait_until="domcontentloaded")
    page.wait_for_load_state('load', timeout=120000) 

    js_script = """
        var selectField = document.createElement('select');
        selectField.setAttribute('id', 'product-select');
        selectField.style.position = 'fixed';
        selectField.style.top = '10px';
        selectField.style.left = '10px';
        selectField.style.width = '300px';
        selectField.style.zIndex = '1000';
        selectField.style.padding = '10px';

        var option1 = document.createElement('option');
        option1.value = 'hoodie';
        option1.text = 'Hoodie';
        selectField.appendChild(option1);

        var option2 = document.createElement('option');
        option2.value = 'sweater';
        option2.text = 'Sweater';
        selectField.appendChild(option2);

        document.body.appendChild(selectField);

        var button = document.createElement('button');
        button.innerHTML = 'Submit';
        button.setAttribute('id', 'submit-button');
        button.style.position = 'fixed';
        button.style.top = '50px';
        button.style.left = '10px';
        button.style.zIndex = '1000';
        button.style.padding = '10px';
        button.style.backgroundColor = '#4CAF50';
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.cursor = 'pointer';
        document.body.appendChild(button);

        button.addEventListener('click', function() {
            var selectedValue = document.getElementById('product-select').value;
            window.selectedValue = selectedValue;
            document.body.removeChild(selectField);
            document.body.removeChild(button);
        });
    """
    page.evaluate(js_script)

    user_input = None
    while not user_input:
        user_input = page.evaluate("window.selectedValue")
        time.sleep(1)

    print(f"Người dùng đã chọn: {user_input}")

    try:
        file_path = 'D:/bind/name.txt'
        with open(file_path, 'r') as file:line = file.readline()
        product_name = line.split(':', 1)[1].strip()
        page.locator("//*[@id='preview-product-title']/div/div[1]/div/div/div/div/span/span/input").fill(product_name)

        page.locator("//*[@id='main_image_item_0']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/ash.png")

        page.locator("//*[@id='main_image_item_1']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/black.png")

        page.locator("//*[@id='main_image_item_2']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/forest_green.png")

        page.locator("//*[@id='main_image_item_3']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/light_pink.png")

        page.locator("//*[@id='main_image_item_4']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/light-blue.png")

        page.locator("//*[@id='main_image_item_5']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/red.png")

        page.locator("//*[@id='main_image_item_6']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/sand.png")

        page.locator("//*[@id='main_image_item_7']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/sport_grey.png")

        page.locator("//*[@id='main_image_item_8']/div/div/div[1]/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/white.png")

        text_content = """
        Celebrate the holiday season with this fun and festive Old Row Santa Hoodie! Featuring a playful design of Santa riding a beer keg sleigh, this hoodie is the perfect way to embrace the winter spirit with a touch of humor. Whether you're enjoying a holiday party or lounging by the fire, this hoodie will keep you warm and cozy while spreading holiday cheer.

        Features:
        - Soft Cotton Blend: Made with high-quality fabric for maximum comfort and warmth during the chilly months.
        - Unique Holiday Design: The front of the hoodie features a simple "Old Row" logo with a Santa hat, while the back showcases Santa riding a keg down a snowy hill with the caption "It's the most wonderful time for a beer!"
        - Classic Hoodie Fit: With a relaxed fit and spacious kangaroo pocket, this hoodie is ideal for casual wear and holiday events.
        - Durable and Stylish: Made to last with high-quality stitching and fabric, ensuring the design stays vibrant after multiple washes.
        - Available in Multiple Sizes: From snug to oversized, there's a fit for everyone to enjoy.

        Care Instructions:
        - Machine wash cold, inside out.
        - Tumble dry low or air dry to maintain the vibrancy of the graphic and the softness of the fabric.
        """
        # description
        page.locator('//*[@id="preview-product-description"]/div[2]/div[2]/div[2]/div[1]/div/div[2]/p').fill(text_content)
        # image
        page.locator("//*[@id='preview-product-description']/div[2]/div[2]/div[2]/div/div/input").set_input_files("C:/Users/Admin/Downloads/eclipse/Downloads/sw/white.png")

        # category
        page.locator('//*[@id="product-cascader-select-view"]').click()
        page.locator('//*[@id="theme-arco-cascader-popup-0"]/div/div[2]/div/div[1]/div/ul/li[5]').click()
        page.locator('//*[@id="theme-arco-cascader-popup-0"]/div/div[2]/div/div[2]/div/ul/li[1]').click()
        page.locator('//*[@id="theme-arco-cascader-popup-0"]/div/div[2]/div/div[3]/div/ul/li[5]').click()
        page.locator('//*[@id="theme-arco-cascader-popup-0"]/div/div[2]/div/div[4]/div/ul/li[1]').click()
        
        page.wait_for_selector('//html/body/div[10]/div[2]/div/div[2]/div/button[2]')
        page.locator('//html/body/div[10]/div[2]/div/div[2]/div/button[2]').click()

        # Product Attributes
        page.locator('//*[@id="product_properties"]/div/div[1]/div[1]/div/div').click()
        page.locator('//*[@id="theme-arco-select-popup-21"]/div/div/li[2]').click()

        page.locator('//*[@id="product_properties"]/div/div[1]/div[2]/div/div').click()
        page.locator('//*[@id="theme-arco-select-popup-22"]/div/div/li[2]').click()

        page.locator('//*[@id="product_properties"]/div/div[1]/div[3]/div/div').click()
        page.locator('//*[@id="theme-arco-select-popup-23"]/div/div/li[2]').click()

        page.locator('//*[@id="product_properties"]/div/div[1]/div[4]/div/div').click()
        page.locator('//*[@id="theme-arco-select-popup-24"]/div/div/li[2]').click()

        page.locator('//*[@id="product_properties"]/div/div[1]/div[5]/div/div').click()
        page.locator('//*[@id="theme-arco-select-popup-25"]/div/div/li[2]').click()

        page.locator('//*[@id="product_properties"]/div/div[1]/div[6]/div/div').click()
        page.locator('//*[@id="theme-arco-select-popup-26"]/div/div/li[2]').click()

        page.locator('//*[@id="product_properties"]/div/div[1]/div[7]/div/div').click()
        page.locator('//*[@id="theme-arco-select-popup-27"]/div/div/li[2]').click()

    except Exception as e:
        print(f"Đã có lỗi xảy ra: {e}")

    time.sleep(1000)

    browser.close()
    gl.stop()
