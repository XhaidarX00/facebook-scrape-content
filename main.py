from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
from bs4 import BeautifulSoup






def initialize_driver():
    """Initialize the WebDriver."""
    service = ChromeService(executable_path = ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def load_cookies(driver, cookies_file="cookies.pkl"):
    """Load cookies from a file and add them to the browser session."""
    try:
        with open(cookies_file, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded successfully.")
    except FileNotFoundError:
        print("Cookies file not found. Please log in manually to create a cookies file.")

def login_with_credentials(driver, email, password):
    """Log in to Facebook using email and password."""
    driver.get("https://www.facebook.com")
    time.sleep(3)
    
    # Find the email and password fields and enter the credentials
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "pass")
    
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    # Submit the login form
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(20)  # Wait for login to complete
    print("Login successful.")
    save_cookies(driver)
    # try:
    #     driver.find_element(By.XPATH, "//div[@aria-label='Profile Anda']")
    #     print("Login successful.")
    #     save_cookies(driver)
    # except:
    #     print("Login failed. Please check your credentials.")
    #     driver.quit()
    #     exit()

def login_with_cookies_or_credentials(driver, email, password, cookies_file="facebook_cookies.pkl"):
    """Attempt to log in using cookies. If unsuccessful, use email and password."""
    driver.get("https://www.facebook.com")
    time.sleep(2)
    
    load_cookies(driver, cookies_file)
    driver.refresh()
    time.sleep(1)
    
    # try:
    #     driver.find_element(By.XPATH, "//a[@aria-label='Profile']")
    #     print("Login successful with cookies.")
    # except:
    #     print("Login with cookies failed. Attempting to log in with credentials.")
    #     login_with_credentials(driver, email, password)

def scroll_down(driver):
    """Scroll down the page to load more content."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(30)  # Adjust the sleep time as needed

def load_all_elements(driver, class_name):
    """Scroll and load all elements with the specified class name."""
    loaded_elements = set()
    
    while True:
        elements = driver.find_elements(By.CLASS_NAME, class_name)
        current_count = len(loaded_elements)
        
        for element in elements:
            loaded_elements.add(element)
        
        if len(loaded_elements) == current_count:
            print("All elements have been loaded.")
            break
        
        scroll_down(driver)
    
    return loaded_elements

def download_images(driver, elements):
    """Download images by clicking the 'Unduh' button in each element."""
    for element in elements:
        try:
            download_button = element.find_element(By.XPATH, "//span[text()='Unduh']/ancestor::a")
            download_button.click()
            time.sleep(5)  # Wait for the download to start
        except:
            print("Download button not found in this container.")

def save_cookies(driver, cookies_file="cookies.pkl"):
    """Save cookies to a file for future use."""
    with open(cookies_file, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("Save coookie succes!")

import os
import requests
import re

def sanitize_filename(filename):
    # Menghapus karakter yang tidak diizinkan dari nama file
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download_image(index, url, folder_path):
    # Membuat folder jika belum ada
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Mengambil konten gambar dari URL
    response = requests.get(url)
    if response.status_code == 200:
        # Menentukan nama file gambar
        # image_name = sanitize_filename(url.split('/')[-1])
        image_name = f'photo_{index}.jpg'
        image_path = os.path.join(folder_path, image_name)
        
        try:
            # Menyimpan gambar ke path yang ditentukan
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Image saved to {image_path}")
        except IOError as e:
            print(f"Failed to save image: {e}")
    else:
        print(f"Failed to download image from {url}, Status code: {response.status_code}")



def main(email, password):
    """Main function to execute the script."""
    driver = initialize_driver()
    login_with_cookies_or_credentials(driver, email, password)
    print('Proses membuka page ')
    # driver.get('https://www.facebook.com/muhamad.iskandar.9210256/photos_by')
    driver.get('https://www.facebook.com/rohim.tekik.1/photos_by')
    driver.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})
    time.sleep(2)
    print('Menunggu 2 detik')
    
    # Ambil seluruh body HTML
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Temukan elemen dengan class yang sesuai
    elements = soup.find_all('div', class_='x1a02dak')
    scrolled = 0
    scroll_size = 400
    
    # print(len(elements))
    # return
    # Filter elemen berdasarkan XPath yang diinginkan
    filtered_elements = [element for element in elements if element.find_parent('div', class_='x1e56ztr') and element.find_parent('div', class_='xyamay9')]
    
    scroll_times = len(filtered_elements)
    while scrolled < scroll_times:
        driver.execute_script('windows.scrollTo(0, arguments[0]);', scroll_size)
        scrolled += 1
        scroll_size += 400
        print(f"Jumlah elemen ditemukan: {len(filtered_elements)}")
        time.sleep(1)
    
    if filtered_elements:
        print(f"Jumlah elemen ditemukan: {len(filtered_elements)}")
        for element in filtered_elements:
            img_tags = element.find_all('img')
            print(img_tags)
            for index, img in enumerate(img_tags):
                index += 1
                img_url = img.get('src')
                if img_url:
                    print(f"Downloading image from {img_url}")
                    download_image(index, img_url, 'download/photos')
                    
                
        # for index, element in enumerate(filtered_elements):
        #     # Cetak isi elemen
        #     print(f"Elemen {index + 1}:")
        #     print(element.prettify())  # Menampilkan HTML dari elemen tersebut dengan format yang mudah dibaca
        #     if index == 2:
        #         break
    else:
        print("Tidak ditemukan elemen dengan class yang diberikan.")
    
    # # Download gambar
    # for element in filtered_elements:
    #     img_tags = element.find_all('img')
    #     for img in img_tags:
    #         img_url = img.get('src')
    #         if img_url:
    #             print(f"Downloading image from {img_url}")
    #             download_image(img_url, 'download/photos')
    
    # Driver cleanup
    driver.quit()
    
    # Driver cleanup
    # driver.quit()

    # element = driver.find_elements(By.XPATH, "//div[@class='xyamay9']/div[@class='x1e56ztr']/div[@class='x78zum5']")
    # print(element)
    # print(len(element))
    # class_name = "xyamay9"  # Replace with the actual class name of the elements you want to target
    # elements = load_all_elements(driver, class_name)
    # download_images(driver, elements)
    
    # # save_cookies(driver)
    # driver.quit()

if __name__ == "__main__":
    email = "tuyultermux777@gmail.com"  # Replace with your Facebook email
    password = "@Dardar777"        # Replace with your Facebook password
    main(email, password)
