import re
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

import utils.list_to_json as wr


def infojobs_scrapper(file_name: str = None, keyword: str = None):
    """
    Infojobs scrap with Beautifulsoup.
    Pass the file name and keyword to generate the CSV file.
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

    list_responses = wr.read_list(file_name)

    for response in list_responses:
        print("Opening file to get all the response...")
        html_soup = BeautifulSoup(response, "lxml")

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
                url_h2 = lines.find_all("a", href=re.compile("//www.infojobs.net/"))[
                    0
                ].get("href")
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
                li_city = (
                    container_4[0].text if container_4 != [] else "Solo teletrabajo"
                )
                cities.append(li_city)

                # Fecha de creación de Vacante
                container_5 = lines.find_all(
                    "span",
                    class_="ij-FormatterSincedate ij-FormatterSincedate--success ij-FormatterSincedate--xs",
                )
                if container_5 == []:
                    container_5 = lines.find_all(
                        "span",
                        class_="ij-FormatterSincedate ij-FormatterSincedate--primary ij-FormatterSincedate--xs",
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
                    container_7[0].text
                    if container_7 != []
                    else "Salario no disponible"
                )
                salaries.append(li_salary)
                # Tipo de trabajo
                container_8 = lines.find_all(
                    ["li"],
                    class_=[
                        "ij-OfferCardContent-description-list-item",
                    ],
                )

                types_of_works = ["Híbrido", "Presencial", "Solo teletrabajo"]

                if container_8[0].text in types_of_works:
                    work_type = container_8[0].text
                elif container_8[1].text in types_of_works:
                    work_type = container_8[1].text
                elif container_8[2].text in types_of_works:
                    work_type = container_8[2].text
                elif container_8[3].text in types_of_works:
                    work_type = container_8[3].text
                else:
                    work_type = "No data"

                work_types.append(work_type)

    # Creating the CSV file
    print()
    print("Creating CSV file")
    df = pd.DataFrame(
        {
            "Nombre de empresa": company_names,
            "Tecnologia": company_roles,
            "Ciudad": cities,
            "Tipo de trabajo": work_types,
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
        "Tipo de trabajo",
        "Fecha de creación de Vacante",
        "URL Empresa",
        "URL Vacante",
        "Tipo de contratacion",
        "Horario de trabajo",
        "Salario",
    ]
    date = datetime.now().strftime("%Y-%m-%d")
    df.to_csv(
        f"csv_files/infojobs_{keyword}_{date}.csv",
        encoding="utf-8",
        index=False,
        columns=cols,
    )
    print()
    print("CSV file generated...")
