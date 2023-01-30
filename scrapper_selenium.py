import argparse

import scrapper_beau as sb
import utils.list_to_json as wl
import utils.selenium_script as selenium_script

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
    while pages < 5:

        url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={keyword}&normalizedJobTitleIds=&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page={pages}&sortBy=RELEVANCE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds="

        # Go to the site
        response = selenium_script.selenium(url)

        list_response.append(response.page_source)
        pages += 1
        response.close()
    try:
        print()
        print("Generating file with response...")
        wl.write_list(list_response, f"{file_name}")
        sb.infojobs_scrapper(f"{file_name}", keyword)
        print("Success")
    except Exception as e:
        raise e


if __name__ == "__main__":
    selenium_scrapper()
