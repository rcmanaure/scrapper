from time import sleep

import chromedriver_autoinstaller
import selenium.webdriver.support.expected_conditions as EC
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait

chromedriver_autoinstaller.install()


def selenium(url: str):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--headless")

    chrome = uc.Chrome(options=options)
    try:
        # Go to the site
        print(f"Get info from the site...{url}")
        sleep(5)
        chrome.get(url)
        chrome.maximize_window()
        # Scroll Down to load the page dynamically
        last_scroll_pos = 0
        while True:
            WebDriverWait(chrome, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            ).send_keys(Keys.DOWN)
            sleep(0.01)
            current_scroll_pos = str(
                chrome.execute_script("return window.pageYOffset;"),
            )
            if current_scroll_pos == last_scroll_pos:
                print("scrolling is finished")
                break
            last_scroll_pos = current_scroll_pos

    except WebDriverException as e:
        print("Error in the connection.")
        chrome.quit()
        raise e("Error in the connection.")

    return chrome
