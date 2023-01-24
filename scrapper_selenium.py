import argparse
from time import sleep

import selenium.webdriver.support.expected_conditions as EC
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait

import scrapper_beau as sb
import utils.list_to_json as wl

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
    file_name = "infojobs_responses"
    keyword = str(args.keyword) if args.keyword else "Programador"
    pages = 1
    list_response = []
    # while pages < 3:
    #     options = uc.ChromeOptions()
    #     options.headless = True
    #     options.add_argument("--headless")

    #     chrome = uc.Chrome(options=options)
    #     try:
    #         # Go to the site
    #         print("Get info from the site...")
    #         chrome.get(
    #             f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={keyword}&normalizedJobTitleIds=&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page={pages}&sortBy=RELEVANCE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds="
    #         )
    #     except WebDriverException as e:
    #         print("Error in the connection.")
    #         raise e("Error in the connection.")

    #     try:
    #         # Scroll Down to load the page dynamically
    #         last_scroll_pos = 0
    #         while True:
    #             WebDriverWait(chrome, 30).until(
    #                 EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    #             ).send_keys(Keys.DOWN)
    #             sleep(0.01)
    #             current_scroll_pos = str(
    #                 chrome.execute_script("return window.pageYOffset;"),
    #             )
    #             if current_scroll_pos == last_scroll_pos:
    #                 print("scrolling is finished")
    #                 break
    #             last_scroll_pos = current_scroll_pos
    #     except WebDriverException as e:
    #         print("Error obtaining data from the site...")
    #         raise e

    # list_response.append(chrome.page_source)
    # pages += 1

    try:
        print()
        print("Generating file with response...")
        # wl.write_list(list_response, f"{file_name}")
        sb.infojobs_scrapper(f"{file_name}", keyword)
        print("Success")
    except Exception as e:
        raise e


if __name__ == "__main__":
    selenium_scrapper()
