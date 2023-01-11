from dataclasses import dataclass
from datetime import datetime

import requests
import translators as ts
from bs4 import BeautifulSoup


date_today = datetime.now()
date_today.strftime("%d.%m.%Y")

URL = f"https://bank.gov.ua/ua/markets/exchangerates?date={date_today}&period=daily"

@dataclass
class Currency:
    name: str
    official_exchange_rate: float


def parse_single_currency(currency_soup) -> Currency:
    currency_name = currency_soup.select_one('td[data-label="Назва валюти"] > a').text.strip()
    currency_value = float(currency_soup.select_one('td[data-label="Офіційний курс"]').text.replace(",", "."))
    currency_number = int(currency_soup.select_one('td[data-label="Кількість одиниць валюти"]').text)

    translated_currencys_name = ts.translate_text(f"{currency_name}", to_language="en")

    return Currency(
        name=translated_currencys_name,
        official_exchange_rate=round(currency_value / currency_number, 4)
    )



def get_all_currencies() -> [Currency]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    currencies_soup = soup.select("tbody > tr")
    return [parse_single_currency(currency_soup) for currency_soup in currencies_soup]


def main():
    print(get_all_currencies())



if __name__ == "__main__":
    main()
