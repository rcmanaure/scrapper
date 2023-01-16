import re
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent(browsers=["chrome", "firefox"])


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
# with requests.Session() as s:

#     while pages < 3:
#         sleep(10)
#         url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=Programador%2Fa%20web&normalizedJobTitleIds=2512_866c7813-2c03-47d7-9bdc-192cfbace57c&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page={pages}&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds="

#         response = s.get(url, headers=my_headers)

#         soup = BeautifulSoup(response.text, "html.parser")
#         soup_list.append(soup)
#         pages += 1

# print(soup_list[0])
# with open("infojobs_html.json", "wb") as fp:
#     # To write data to new file
#     json.dump(soup_list, fp)


with open("infojobs_html.txt", "r") as fh:

    html_soup = BeautifulSoup(fh, "html.parser")


company_names = []
company_urls = []
company_roles = []
roles_urls = []
work_types = []
vacancy_dates = []
contract_types = []
work_schedules = []
salaries = []
cities = []

# for i in soup_list:
#     # test = BeautifulSoup(i, "lxml")
#     container = i.find_all(
#         ["h2", "h3", "li"],
#         class_=[
#             "ij-OfferCardContent-description-title",
#             "ij-OfferCardContent-description-subtitle",
#             "ij-OfferCardContent-description-list-item",
#             # lambda x: x != "hidden",
#         ],
#     )

#     for lines in container:
#         if lines.name == "h2":
#             roles = lines.text
#             url = lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get(
#     "href"
# )
# company_roles.append(roles)
# roles_url.append(url)
#             # print("keyword: ", roles)
#             # print(
#             #     "Foundation url:",
#             #     lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get("href"),
#             # )

#         if lines.name == "h3":
# company = lines.text
# url = lines.find_all(
#     "a", class_="ij-OfferCardContent-description-subtitle-link"
# )[0].get("href")
#             company_names.append(company)
#             company_urls.append(url)
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

container = html_soup.find_all(
    ["div"],
    class_=["ij-OfferCardContent-description"],
)

# container_list = []
for lines in container:
    if lines.name == "div":
        container_2 = lines.find_all(
            ["h2", "h3", "li"],
            class_=[
                "ij-OfferCardContent-description-title",
                "ij-OfferCardContent-description-subtitle",
                "ij-OfferCardContent-description-list-item",
            ],
        )

        # Tecnologia
        h2_roles = container_2[0].text
        company_roles.append(h2_roles)
        # URL Vacante
        url_h2 = lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get(
            "href"
        )
        format_url2 = f"https:{url_h2}"
        roles_urls.append(format_url2)
        # Nombre de empresa
        h3 = container_2[1].text
        company_names.append(h3)
        # URL Empresa (InfoJobs)
        url_h3 = lines.find_all(
            "a", class_="ij-OfferCardContent-description-subtitle-link"
        )[0].get("href")
        company_urls.append(url_h3)

        # Ciudad
        li_0 = container_2[2].text
        cities.append(li_0)
        # Tipo de trabajo
        li_1 = container_2[3].text
        work_types.append(li_1)
        # Fecha de creación de Vacante
        li_2 = container_2[4].text
        vacancy_dates.append(li_2)
        # Tipo de contrato
        li_3 = container_2[5].text
        contract_types.append(li_3)
        # Horario de trabajo
        li_6 = container_2[6].text
        work_schedules.append(li_6)
        # Salario
        li_7 = container_2[7].text
        salaries.append(li_7)

# Creating the CSV file
df = pd.DataFrame(
    {
        "Nombre de empresa": company_names,
        "Tecnologia": company_roles,
        "Ciudad": cities,
        "Fecha de creación de Vacante": vacancy_dates,
        "Type of work": work_types,
        "URL Empresa": company_urls,
        "URL Vacante": roles_urls,
        "Tipo de contratacion": contract_types,
        "Horario de trabajo": work_schedules,
        "Salario": salaries,
    }
)

cols = [
    "Nombre de empresa",
    "Tecnologia",
    "Ciudad",
    "Fecha de creación de Vacante",
    "Type of work",
    "URL Empresa",
    "URL Vacante",
    "Tipo de contratacion",
    "Horario de trabajo",
    "Salario",
]
df.to_csv("data/infojobs-1.csv", encoding="utf-8", index=False, columns=cols)
