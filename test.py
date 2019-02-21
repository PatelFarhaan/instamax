import time
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-extentions')
options.add_argument('--enable-popup-blocking')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
print("Done")
driver.close()