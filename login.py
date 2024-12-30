from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle


def initialize_driver():
    """Initialize the WebDriver."""
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


def load_cookies(driver, cookies_file="facebook_cookies.pkl"):
    """Load cookies from a file and add them to the browser session."""
    try:
        with open(cookies_file, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded successfully.")
    except FileNotFoundError:
        print("Cookies file not found. Please log in manually to create a cookies file.")

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException


def main(cookies_file="facebook_cookies.pkl"):
    driver = initialize_driver()
    driver.get("https://www.facebook.com")
    load_cookies(driver, cookies_file)
    driver.refresh()
    print('Proses membuka page ')
    # driver.get('https://www.facebook.com/rohim.tekik.1/photos_by') # photo
    driver.get('https://www.facebook.com/rohim.tekik.1/videos_by') # video
    driver.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})
    print('Menunggu 3 detik')
    time.sleep(3)

    scroll_times = len(driver.find_elements(By.XPATH, '//div[contains(@class, "x1923su1")]/div[@aria-label="Edit"]'))
    print(f"Initial scroll times: {scroll_times}")
    # data = driver.find_elements(By.XPATH, '//div[contains(@class, "x1923su1")]/div[@aria-label="Edit"]')
    # print(len(data))
    # scroll_size = 400
    # for element in data:
    #     try:
            # Tunggu hingga tombol edit bisa di-click
            # tombol_edit = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable(element)
            # )
            # tombol_edit.click()

            # Tunggu hingga menu dropdown muncul, sesuaikan dengan teks tombol yang diinginkan
            # tombol_unduh = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Unduh')]"))
            # )
            # tombol_unduh.click()

            # Berhenti setelah operasi sukses
            # break
        #     scroll_size += 250
        #     driver.execute_script('window.scrollTo(0, arguments[0]);', scroll_size)

        # except (TimeoutException, NoSuchElementException) as e:
        #     print(f"Error click element : {e}")
        #     continue  # Lanjutkan ke elemen berikutnya jika ada error

        # Tambahkan jeda kecil antara operasi
        # time.sleep(0.5)
    
    # print(len(data))
    # data = driver.find_elements(By.XPATH, '//div[contains(@class, "x1923su1")]/div[@aria-label="Edit"]')
    # print(len(data))
    # return
    scrolled = 0
    click_done = 1
    scroll_size = 500

    while scrolled < click_done:
        driver.execute_script('window.scrollTo(0, arguments[0]);', scroll_size)
        time.sleep(5)
        # data = driver.find_elements(By.XPATH, '//div[contains(@class, "x1923su1")]/div[@aria-label="Edit"]') # fhoto
        data = driver.find_elements(By.XPATH, '//div[contains(@class, "x1923su1")]/div[@aria-label="Edit"]') # video
        if click_done > 1:
            data = data[click_done + 1:]
            
        for element in data:
            try:
                # Tunggu hingga tombol edit bisa di-click
                tombol_edit = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(element)
                )

                try:
                    tombol_edit.click()
                except WebDriverException as e:
                    print(f"Error click element: {str(e)}")
                    break

                # Tunggu hingga menu dropdown muncul, sesuaikan dengan teks tombol yang diinginkan
                tombol_unduh = WebDriverWait(driver, 10).until(
                    # EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Unduh')]")) # photo
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Unduh SD')]")) #video
                )
                
                try:
                    tombol_unduh.click()
                except WebDriverException as e:
                    print(f"Error click element: {str(e)}")
                    break


                # Berhenti setelah operasi sukses
                # break
                click_done += 1
                print(f'Terdownload {click_done}')
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error click element : {e}")
                continue  # Lanjutkan ke elemen berikutnya jika ada error
            
            time.sleep(7)
            scrolled += 1
            
        scroll_size += 550
        print(f"Updated Data: {len(data)}")
        if len(data) == 0:
            break
        # Tambahkan jeda kecil antara operasi
        # time.sleep(0.5)

        # time.sleep(5)
        # scroll_size += 400
        # scrolled += 1
        # scroll_times = len(driver.find_elements(By.XPATH, '//div[contains(@class, "html-div")]//a[contains(@class, "x1i10hfl")]/img[contains(@class, "xzg4506")]'))
        # # scroll_times = len(driver.find_elements(By.XPATH, '//div[@class="html-div x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x1ey2m1c x9f619 x78zum5 xdt5ytf x1iyjqo2 xs83m0k xds687c x17qophe x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x18d9i69 x4uap5 xkhd6sd xexx8yu x10l6tqk x13vifvy x1ja2u2z"]/a[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lliihq x5yr21d x1n2onr6 xh8yej3"]/img[@class="xzg4506 xycxndf xua58t2 x4xrfw5 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x9f619 x5yr21d xl1xv1r xh8yej3"]'))
        # # scroll_times = len(driver.find_elements(By.XPATH, '//div[@class="x9f619 x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 x6s0dn4 x78zum5 xdt5ytf xl56j7k"]'))
        # print(f"Updated scroll times: {scroll_times}")
    
    # scroll_times = len(driver.find_elements(By.XPATH, '//div[contains(@class, "html-div")]//a[contains(@class, "x1i10hfl")]/img[contains(@class, "xzg4506")]'))
    # scroll_times = len(driver.find_elements(By.XPATH, '//div[@class="x9f619 x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 x6s0dn4 x78zum5 xdt5ytf xl56j7k"]'))
    print('---------------------------')
    print(f"Final scroll times: {click_done}")
    print('---------------------------')
    
    time.sleep(3600) 
    # Don't forget to quit the driver after all operations
    driver.quit()

if __name__ == "__main__":
    main(cookies_file="facebook_cookies.pkl")
