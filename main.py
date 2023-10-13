import os
import json

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


cookies_path = "json_cookies"
working_cookies_path = "working_cookies"
invalid_cookies_path = "invalid_cookies"

def load_cookies_from_json(FILEPATH: str):
    with open(FILEPATH, "r", encoding="utf-8") as cookie_file:
        cookie = json.load(cookie_file)
    return cookie

def open_webpage_with_cookies(URL: str, COOKIES: dict):
    firefox_options = Options()
    firefox_options.add_argument("start-maximized")
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(URL)

    for cookie in COOKIES:
        if cookie["domain"] == ".netflix.com":
            driver.add_cookie(cookie)

    driver.refresh()

    if driver.find_elements(By.CSS_SELECTOR, ".login-form"):
        print(f"❌ Expired cookies! - {filename}")
    else:
        print(f"✅ Working cookies! - {filename}")
        
        try:
            os.mkdir(working_cookies_path)
        except FileExistsError:
            pass
        
        new_filepath = os.path.join(working_cookies_path, filename)
        with open(new_filepath, "w", encoding="utf-8") as c:
            c.write(content)
        
    driver.quit()
    os.remove(filepath)


for filename in os.listdir(cookies_path):
    filepath = os.path.join(cookies_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            url = "https://netflix.com/login"

            try:
                cookies = load_cookies_from_json(filepath)
                open_webpage_with_cookies(url, cookies)
            except (InvalidCookieDomainException, UnableToSetCookieException) as e:
                print(f"🚫 Invalid cookies! - {filename} - {str(e)}")
                
                try:
                    os.mkdir(invalid_cookies_path)
                except FileExistsError:
                    pass

                new_filepath = os.path.join(invalid_cookies_path, filename)
                with open(new_filepath, "w", encoding="utf-8") as c:
                    c.write(content)

                os.remove(filepath)
            except Exception as e:
                print(f"⚠️ ERROR! - {filename} - {str(e)}")
