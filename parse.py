from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

URL = "https://bank.gov.ua/ua/markets/exchangerates"

@dataclass
class Currency:
    name: str
    official_exchange_rate: float
    number_of_currency_units: int


def parse_single_currency(currency_soup) -> Currency:
    currency_name = currency_soup.select_one('td[data-label="Назва валюти"] > a').text.strip()
    currency_value = float(currency_soup.select_one('td[data-label="Офіційний курс"]').text.replace(",", "."))
    currency_number = int(currency_soup.select_one('td[data-label="Кількість одиниць валюти"]').text)

    return Currency(
        name=currency_name,
        official_exchange_rate=currency_value,
        number_of_currency_units=currency_number
    )



def get_all_currencies(url) -> [Currency]:
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")

    currencies_soup = soup.select("tbody > tr")
    return [parse_single_currency(currency_soup) for currency_soup in currencies_soup]


def main():
    currencies = get_all_currencies(URL)

    for currency in currencies:
        print(currency.name + ((40 - len(currency.name)) * " ") + "|   " +
              str(round((currency.official_exchange_rate / currency.number_of_currency_units), 4)))



if __name__ == "__main__":
    main()
