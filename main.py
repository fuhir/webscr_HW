import requests
import bs4
import json
import re
from fake_headers import Headers

headers = Headers(browser='random', os='random')
url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

if __name__ == "__main__":
    res = requests.get(url=url, headers=headers.generate())
    soup = bs4.BeautifulSoup(res.text, "lxml")

    result = []
    for item in soup.find_all(class_="vacancy-serp-item__layout"):
        title_item = item.find(class_="serp-item__title")
        title = title_item.text
        desc_item = soup.find(class_="g-user-content")
        desc = desc_item.text if desc_item is not None else ""

        if "django" in (title + desc).lower() or "flask" in (title + desc).lower():
            salary = item.find("span", class_="bloko-header-section-3")
            if salary is None:
                salary = ""
            else:
                salary = salary.text
            city = item.find(
                "div", attrs={"data-qa": "vacancy-serp__vacancy-address"}
            ).text
            company = item.find(
                "div", class_="vacancy-serp-item__meta-info-company"
            ).text

            result.append(
                {
                    "link": title_item.attrs["href"],
                    "salary": salary.replace("\u202f", ""),
                    "company": company.replace("\xa0", " "),
                    "city": re.sub("\xa0", "", city),
                }
            )

    with open("result.json", "w", encoding="utf8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
