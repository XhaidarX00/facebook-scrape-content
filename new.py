import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Inisialisasi WebDriver (gunakan ChromeDriver yang sesuai)
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Akses halaman login atau halaman yang mengatur cookie
driver.get('https://www.google.com/search?q=apa+yang+dimaksud+dengan+cinta&rlz=1C1UEAD_enID1025ID1025&oq=apa&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MggIARBFGCcYOzIICAIQRRgnGDsyBggDEEUYOTIGCAQQRRg7MgYIBRBFGD0yBggGEEUYPTIGCAcQRRg90gEIMTE4M2owajeoAgCwAgA&sourceid=chrome&ie=UTF-8')

# Tunggu beberapa saat untuk login secara manual jika diperlukan
input("Tekan Enter setelah login manual dan halaman dimuat...")

# Simpan cookies ke file
cookies = driver.get_cookies()
with open('cookies_google.pkl', 'wb') as cookie_file:
    pickle.dump(cookies, cookie_file)

# Tutup driver
driver.quit()



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# # Inisialisasi WebDriver (gunakan ChromeDriver yang sesuai)
# service = ChromeService(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

# # Definisikan fungsi untuk menangkap permintaan
# def capture_audio_requests(request):
#     if 'audio' in request.url:
#         print(f"Audio URL ditemukan: {request.url}")

# # Mendaftarkan listener untuk permintaan jaringan
# driver.request_interceptor = capture_audio_requests

# # Buka halaman web
# driver.get('https://www.google.com/search?q=apa+yang+dimaksud+dengan+cinta&rlz=1C1UEAD_enID1025ID1025&oq=apa&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MggIARBFGCcYOzIICAIQRRgnGDsyBggDEEUYOTIGCAQQRRg7MgYIBRBFGD0yBggGEEUYPTIGCAcQRRg90gEIMTE4M2owajeoAgCwAgA&sourceid=chrome&ie=UTF-8')
# time.sleep(5)
# # Klik tombol "Dengarkan"
# play_button = driver.find_element(By.XPATH, '//div[@jsname="rMP3uf"]')
# play_button.click()

# # Tunggu beberapa saat agar audio mulai dimuat
# time.sleep(30)

# # Tutup browser
# driver.quit()