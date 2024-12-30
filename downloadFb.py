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

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
    
    # href_link = driver.find_element(By.XPATH, '//div[contains(@class, "x9f619")]/a[contains(@class, "x1i10hfl") and @role="link"]').get_attribute('href')
    # href_link = driver.find_elements(By.XPATH, '//div[contains(@class, "x9f619")]//a[contains(@class, "x1i10hfl") and @role="link"]')
    
    # print(href_link)
    # print(len(href_link))
    # for index, href in enumerate(href_link):
    #     print(f'{index}. {href.get_attribute('href')}')
        
    # return
    scrolled = 0
    click_done = 1
    scroll_size = 500

    while scrolled < click_done:
        driver.execute_script('window.scrollTo(0, arguments[0]);', scroll_size)
        time.sleep(5)
        # data = driver.find_elements(By.XPATH, '//div[contains(@class, "x1923su1")]/div[@aria-label="Edit"]') # fhoto
        # href_link = driver.find_element_by_xpath('//a[contains(@class, "x1i10hfl") and @role="link"]/@href').get_attribute('href') # video
        data = driver.find_elements(By.XPATH, '//div[contains(@class, "x1923su1")]/div[@aria-label="Edit"]') # video
        if click_done > 1:
            data = data[click_done + 1:]
            
        for element in data:
            try:
                downloadVideo(href_link)
                click_done += 1
                print(f'download video ke - {click_done} : {href_link}')
                
            except Exception as e:
                print(f"Error click element : {e}")
                continue  # Lanjutkan ke elemen berikutnya jika ada error
            
            time.sleep(10)
            scrolled += 1
            
        scroll_size += 550
        print(f"Updated Data: {len(data)}")
        if len(data) == 0:
            break
    
    print('---------------------------')
    print(f"Final Videos : {click_done}")
    print('---------------------------')
    
    driver.quit()
    













import requests
import json
import subprocess
import os

output_folder = "download/videos"
# True = keep audio/video files separate and False = keep only the merged file
keep_raw_files = False


def downloadFile(link, file_name):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).content
    except:
        print("Failed to open {}".format(link))
        return
    with open(os.path.join(output_folder, file_name), 'wb') as f:
        f.write(resp)


def downloadVideo(link):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Dnt': '1',
        'Dpr': '1.3125',
        'Priority': 'u=0, i',
        'Sec-Ch-Prefers-Color-Scheme': 'dark',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Full-Version-List': '"Chromium";v="124.0.6367.156", "Google Chrome";v="124.0.6367.156", "Not-A.Brand";v="99.0.0.0"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Viewport-Width': '1463'
    }
    try:
        resp = requests.get(link, headers=headers)
    except:
        print("Failed to open {}".format(link))
        return
    link = resp.url.split('?')[0]
    resp = resp.text
    splits = link.split('/')
    video_id = ''
    for ids in splits:
        if ids.isdigit():
            video_id = ids
    try:
        target_video_audio_id = resp.split('"id":"{}"'.format(video_id))[1].split(
            '"dash_prefetch_experimental":[')[1].split(']')[0].strip()
    except:
        target_video_audio_id = resp.split('"video_id":"{}"'.format(video_id))[1].split(
            '"dash_prefetch_experimental":[')[1].split(']')[0].strip()
    list_str = "[{}]".format(target_video_audio_id)
    sources = json.loads(list_str)
    video_link = resp.split('"representation_id":"{}"'.format(sources[0]))[
        1].split('"base_url":"')[1].split('"')[0]
    video_link = video_link.replace('\\', '')
    print(video_link)
    audio_link = resp.split('"representation_id":"{}"'.format(sources[1]))[
        1].split('"base_url":"')[1].split('"')[0]
    audio_link = audio_link.replace('\\', '')
    print(audio_link)
    print("Downloading video...")
    downloadFile(video_link, 'video.mp4')
    print("Downloading audio...")
    downloadFile(audio_link, 'audio.mp4')
    print("Merging files...")
    video_path = os.path.join(output_folder, 'video.mp4')
    audio_path = os.path.join(output_folder, 'audio.mp4')
    combined_file_path = os.path.join(output_folder, f'{video_id}.mp4')
    cmd = 'ffmpeg -hide_banner -loglevel error -i "{}" -i "{}" -c copy "{}"'.format(
        video_path, audio_path, combined_file_path)
    subprocess.call(cmd, shell=True)
    if not keep_raw_files:
        os.remove(video_path)
        os.remove(audio_path)
    os.rename(combined_file_path,
              os.path.join(output_folder, '{}.mp4'.format(video_id)))
    
    print("Done! Please check in the {} folder".format(output_folder))

if __name__ == "__main__":
    main(cookies_file="facebook_cookies.pkl")
#     if not os.path.exists(output_folder):
#         os.mkdir(output_folder)
#     downloadVideo("https://www.facebook.com/rohim.tekik.1/videos/213430714573934")
#     print("Done! Please check in the {} folder".format(output_folder))
