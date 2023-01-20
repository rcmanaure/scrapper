import re

import pandas as pd
from bs4 import BeautifulSoup


def infojobs_scrapper(file_name: str):
    """
    Infojobs scrap with Beautifulsoup.
    Pass the file name to generate the CSV file.
    """

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

    print("Opening file to get all the response...")
    with open(f"scrap_files/{file_name}", "r") as fh:
        html_soup = BeautifulSoup(fh, "lxml")

    container = html_soup.find_all(
        ["div"],
        class_=["ij-OfferCardContent-description"],
    )

    print("Obtain all necessary data from the file...")
    for lines in container:
        if lines.name == "div":
            # Tecnologia o Roles
            container_2 = lines.find_all(
                ["h2"], class_="ij-OfferCardContent-description-title"
            )
            h2_roles = container_2[0].text if container_2 != [] else "No data"
            company_roles.append(h2_roles)
            # URL Vacante
            url_h2 = lines.find_all("a", href=re.compile("//www.infojobs.net/"))[0].get(
                "href"
            )
            format_url2 = f"https:{url_h2}"
            roles_urls.append(format_url2 if url_h2 != [] else "No data")
            # Nombre de empresa
            container_3 = lines.find_all(
                ["h3"], class_="ij-OfferCardContent-description-subtitle"
            )
            h3_company = container_3[0].text if container_3 != [] else "No data"
            company_names.append(h3_company)
            # URL Empresa (InfoJobs)
            url_h3 = lines.find_all(
                "a", class_="ij-OfferCardContent-description-subtitle-link"
            )[0].get("href")
            company_urls.append(url_h3 if url_h3 != [] else "No data")
            # Ciudad
            container_4 = lines.find_all(
                "span",
                class_="ij-OfferCardContent-description-list-item-truncate",
            )
            li_city = container_4[0].text if container_4 != [] else "No data"
            cities.append(li_city)
            # Fecha de creación de Vacante
            container_5 = lines.find_all(
                "span",
                class_="ij-FormatterSincedate ij-FormatterSincedate--success ij-FormatterSincedate--xs",
            )
            li_vacancy = container_5[0].text if container_5 != [] else "No data"
            vacancy_dates.append(li_vacancy)
            # Tipo de contrato y horario
            container_6 = lines.find_all(
                ["li"],
                class_=[
                    "ij-OfferCardContent-description-list-item ij-OfferCardContent-description-list-item--hideOnMobile",
                ],
            )
            # Tipo de contrato
            li_3 = container_6[0].text if container_6 != [] else "No data"
            contract_types.append(li_3)
            # Horario de trabajo
            li_6 = container_6[1].text if container_6 != [] else "No data"
            work_schedules.append(li_6)
            # Salario
            container_7 = lines.find_all(
                "span",
                class_="ij-OfferCardContent-description-salary-info",
            )
            li_salary = (
                container_7[0].text if container_7 != [] else "Salario no disponible"
            )
            salaries.append(li_salary)
            # Tipo de trabajo
            # container_8 = lines.find_all(
            #     ["li"],
            #     class_=[
            #         "ij-OfferCardContent-description-list-item",
            #     ],
            # )

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
    df.to_csv(
        "csv_files/infojobs-demo-10.csv",
        encoding="utf-8",
        index=False,
        columns=cols,
    )
    print("CSV file generated...")


# scrapper()
