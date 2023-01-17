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


def scrapper():
    """Infojobs scrapper"""
    session = requests.Session()

    pages = 1
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
    with requests.Session() as session:
        # keyowords = [
        #     "Developer",
        #     "desarrollador",
        #     "programador",
        #     "programmer",
        #     "Navision",
        #     "Power BI",
        # ]
        # while pages < 2:
        #     # Espera de 10 segundos para evitar captcha
        #     sleep(10)
        #     print(f"Get response from infojobs page {pages}")
        #     # https://www.infojobs.net/ofertas-trabajo?keyword=Desarrollador%2Fa%20web%20desarrollador%20programador%20programmer%20Power%20platform%20Power%20Apps%20Power%20BI%20Navision&normalizedJobTitleIds=2512_ij001&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page=1&sortBy=RELEVANCE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds=
        #     url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=Programador%2Fa%20web&normalizedJobTitleIds=2512_866c7813-2c03-47d7-9bdc-192cfbace57c&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page={pages}&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds="

        #     response = session.get(url, headers=my_headers)
        #     response.raise_for_status()
        #     pages += 1

        #     print("Processing response")
        #     # html_soup = BeautifulSoup(response.text, "lxml")
        #     with open("infojobs_html_test2.txt", "w") as fp:
        #         # To write data to new file
        #         fp.write(response.text)

        with open("infojobs_html_test2.txt", "r") as fh:
            # print(fh.read())
            html_soup = BeautifulSoup(fh, "html.parser")

        container = html_soup.find_all(
            ["div"],
            class_=["ij-OfferCardContent-description"],
        )

        # print(html_soup)
        print("Obtain all necessary data from the response")
        for lines in container:
            if lines.name == "div":

                # Tecnologia o Roles
                container_2 = lines.find_all(
                    ["h2"], class_="ij-OfferCardContent-description-title"
                )
                h2_roles = (
                    container_2[0].text if container_2 != [] else "Not found data"
                )
                company_roles.append(h2_roles)

                # URL Vacante
                url_h2 = lines.find_all("a", href=re.compile("//www.infojobs.net/"))[
                    0
                ].get("href")
                format_url2 = f"https:{url_h2}"
                roles_urls.append(format_url2 if url_h2 != [] else "Not found data")

                # Nombre de empresa
                container_3 = lines.find_all(
                    ["h3"], class_="ij-OfferCardContent-description-subtitle"
                )
                h3_company = (
                    container_3[0].text if container_3 != [] else "Not found data"
                )
                company_names.append(h3_company)

                # URL Empresa (InfoJobs)
                url_h3 = lines.find_all(
                    "a", class_="ij-OfferCardContent-description-subtitle-link"
                )[0].get("href")
                company_urls.append(url_h3 if url_h3 != [] else "Not found data")

                # Ciudad
                container_4 = lines.find_all(
                    "span",
                    class_="ij-OfferCardContent-description-list-item-truncate",
                )
                li_city = container_4[0].text if container_4 != [] else "Not found data"

                cities.append(li_city)

                # s = lines.find_all("span")
                # print(s[4])

                # Fecha de creación de Vacante
                container_5 = lines.find_all(
                    "span",
                    class_="ij-FormatterSincedate ij-FormatterSincedate--success ij-FormatterSincedate--xs",
                )
                li_vacancy = (
                    container_5[0].text if container_5 != [] else "Not found data"
                )
                vacancy_dates.append(li_vacancy)

                container_6 = lines.find_all(
                    ["li"],
                    class_=[
                        "ij-OfferCardContent-description-list-item ij-OfferCardContent-description-list-item--hideOnMobile",
                    ],
                )

                # Tipo de contrato
                li_3 = container_6[0].text if container_6 != [] else "Not found data"
                contract_types.append(li_3)

                # Horario de trabajo
                li_6 = container_6[1].text if container_6 != [] else "Not found data"
                work_schedules.append(li_6)

                # Salario
                container_7 = lines.find_all(
                    "span",
                    class_="ij-OfferCardContent-description-salary-info",
                )
                li_salary = (
                    container_7[0].text if container_7 != [] else "Not found data"
                )
                salaries.append(li_salary)

            # print(salaries)
            # # Tipo de trabajo
            # container_7 = lines.find_all(
            #     "li",
            #     class_="ij-OfferCardContent-description-list-item",
            # )
            # li_work_types = (
            #     container_7[0].text if container_7 != [] else "Not found data"
            # )
            # work_types.append(li_work_types)
            #     li_1 = container_2[3].text
            #     work_types.append(li_1)

            # print(work_types)

    # Creating the CSV file
    print("Creating CSV file")
    df = pd.DataFrame(
        {
            "Nombre de empresa": company_names,
            "Tecnologia": company_roles,
            "Ciudad": cities,
            "Fecha de creación de Vacante": vacancy_dates,
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
        "URL Empresa",
        "URL Vacante",
        "Tipo de contratacion",
        "Horario de trabajo",
        "Salario",
    ]
    df.to_csv("data/infojobs-demo-5.csv", encoding="utf-8", index=False, columns=cols)
    print("Sucess")


scrapper()
