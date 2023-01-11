import re
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent(browsers=["chrome", "firefox"])
test = ua.random

my_headers = {
    "User-Agent": ua.random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "ACCEPT-ENCODING": "gzip, deflate, br",
    "ACCEPT-LANGUAGE": "en-US,en;q=0.9,es;q=0.8",
}
# my_headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
# }
session = requests.Session()
pages = 1
soup_list = []
with requests.Session() as s:

    while pages < 3:
        sleep(10)
        url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=Programador%2Fa%20web&normalizedJobTitleIds=2512_866c7813-2c03-47d7-9bdc-192cfbace57c&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page={pages}&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds="

        response = s.get(url, headers=my_headers)

        soup = BeautifulSoup(response.text, "html.parser")
        soup_list.append(soup)
        pages += 1

print(soup_list[0])
# with open("infojobs_html.json", "wb") as fp:
#     # To write data to new file
#     json.dump(soup_list, fp)


# with open("infojobs_html.txt", "r") as fh:
#     # print(fh.read())
#     html_soup = BeautifulSoup(fh, "html.parser")


company_names = []
company_urls = []
company_roles = []
roles_url = []

for i in soup_list:
    # test = BeautifulSoup(i, "lxml")
    container = i.find_all(
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
            url = lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get(
                "href"
            )
            company_roles.append(roles)
            roles_url.append(url)
            # print("keyword: ", roles)
            # print(
            #     "Foundation url:",
            #     lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get("href"),
            # )

        if lines.name == "h3":
            company = lines.text
            url = lines.find_all(
                "a", class_="ij-OfferCardContent-description-subtitle-link"
            )[0].get("href")
            company_names.append(company)
            company_urls.append(url)
# print("Company name:", company, "\n")
# if lines.name == "li":
#     company = lines.text
#     print("Info:", company, "\n")


# container = html_soup.find_all(
#     ["h2", "h3", "li"],
#     class_=[
#         "ij-OfferCardContent-description-title",
#         "ij-OfferCardContent-description-subtitle",
#         "ij-OfferCardContent-description-list-item",
#         # lambda x: x != "hidden",
#     ],
# )

# for lines in container:
#     if lines.name == "h2":
#         roles = lines.text
#         url = lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get("href")
#         company_roles.append(roles)
#         roles_url.append(url)
#         # print("keyword: ", roles)
#         # print(
#         #     "Foundation url:",
#         #     lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get("href"),
#         # )

#     if lines.name == "h3":
#         company = lines.text
#         url = lines.find_all(
#             "a", class_="ij-OfferCardContent-description-subtitle-link"
#         )[0].get("href")
#         company_names.append(company)
#         company_urls.append(url)
#         # print("Company name:", company, "\n")
#     # if lines.name == "li":
#     #     company = lines.text
#     #     print("Info:", company, "\n")

df = pd.DataFrame(
    {
        "Nombre de empresa": company_names,
        "Tecnologia": company_roles,
        "URL Empresa": company_urls,
        "URL Vacante": roles_url,
    }
)
cols = ["Nombre de empresa", "Tecnologia", "URL Empresa", "URL Vacante"]
df.to_csv("data/infojobs-1.csv", encoding="utf-8", index=False, columns=cols)
