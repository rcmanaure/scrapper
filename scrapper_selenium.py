import argparse
from time import sleep as s

import selenium.webdriver.support.expected_conditions as EC  # noqa
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait

import scrapper_beau as sb

# Setup args
parser = argparse.ArgumentParser()

parser.add_argument("--keyword", help="Keyword")

args = parser.parse_args()


def selenium_scrapper():
    """
    Selenium scrapper
    Pass the keyword to get info of the site.
    example: python scrapper_selenium.py --keyword administrador
    """
    keyword = str(args.keyword) if args.keyword else "Programador"
    pages = 1
    while pages < 2:
        pages += 1
        options = uc.ChromeOptions()
        # options.headless = True
        # options.add_argument("--headless")

        chrome = uc.Chrome(options=options)
        try:
            # Go to the site
            print("Get info from the site...")
            chrome.get(
                f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={keyword}&normalizedJobTitleIds=2512_866c7813-2c03-47d7-9bdc-192cfbace57c&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page=1&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds="
            )
        except WebDriverException as e:
            print("Error in the connection.")
            raise e("Error in the connection.")

        try:
            # accept the terms
            WebDriverWait(chrome, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[2]/div/div/footer/div/button[2]')
                )
            ).click()

            # Scroll Down
            last_scroll_pos = 0
            while True:
                WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
                ).send_keys(Keys.DOWN)
                s(0.01)
                current_scroll_pos = str(
                    chrome.execute_script("return window.pageYOffset;"),
                )
                if current_scroll_pos == last_scroll_pos:
                    print("scrolling is finished")
                    break
                last_scroll_pos = current_scroll_pos
        except WebDriverException as e:
            raise e

        print("Generating file with response...")
        with open("scrap_files/infojobs_html_selenium.txt", "w") as fp:
            # To write data to new file
            fp.write(chrome.page_source)

        # Run the soup top generate the CSV files
        print("Running scrapper fuction to the file created...")
        sb.infojobs_scrapper("infojobs_html_selenium.txt", keyword)

        #  Take screenshot
        # chrome.save_screenshot("datadome_undetected_webddriver4.png")

        print("Success")
        s(1)


selenium_scrapper()
