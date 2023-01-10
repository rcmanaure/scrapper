import json
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
my_headers = {
    "User-Agent": ua.random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}
session = requests.Session()
pages = 1
# with requests.Session() as s:

#     # my_headers = {
#     #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
#     #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     # }

#     url = "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=Programador%2Fa%20web&normalizedJobTitleIds=2512_866c7813-2c03-47d7-9bdc-192cfbace57c&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page=1&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds="

#     response = s.get(url, headers=my_headers)


# soup = BeautifulSoup(response.text, "html.parser")


# with open("infojobs_html.txt", "w") as fp:
#     # To write data to new file
#     fp.write(response.text)


with open("infojobs_html.txt", "r") as fh:
    # print(fh.read())
    html_soup = BeautifulSoup(fh, "html.parser")
    # html_soup = fh

# print(html_soup.prettify())

container = html_soup.find_all(
    ["h2", "h3", "li"],
    class_=[
        "ij-OfferCardContent-description-title",
        "ij-OfferCardContent-description-subtitle",
        "ij-OfferCardContent-description-list-item",
        # lambda x: x != "hidden",
    ],
)

for lines in container:
    if lines.name == "h2":
        roles = lines.text
        print("keyword: ", roles)
    if lines.name == "h3":
        company = lines.text
        print("Company name:", company)
    if lines.name == "li":
        company = lines.text
        print("Info:", company)
