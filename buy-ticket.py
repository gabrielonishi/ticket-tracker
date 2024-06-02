# Selenium imports
import datetime
import random
import re
import time
import typing

# Beautiful Soup imports
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import utils


def greet() -> typing.Tuple[str, datetime.date, datetime.time]:
    event_name: str = input("Qual o nome da festa desejada?")

    ticket_sale_date: str = input(
        "Que dia os ingressos do evento abrem para venda? (dd/mm/aaaa)")

    # Validando data
    while not re.match(r"\d{2}/\d{2}/\d{4}", ticket_sale_date):
        ticket_sale_date = input(
            "Data inválida. Digite novamente usando o formato dd/mm/aaaa")

    day, month, year = ticket_sale_date.split("/")

    ticket_sale_date: datetime.date = datetime.date(
        int(year), int(month), int(day))

    ticket_sale_time: str = input(
        "Que horas os ingressos do evento abrem para venda? (hh:mm)")

    # Validando horário
    while not re.match(r"\d{2}:\d{2}", ticket_sale_time):
        ticket_sale_time = input(
            "Horário inválido. Digite novamente usando o formato hh:mm")

    horas: int = int(ticket_sale_time.split(":")[0])
    minutos: int = int(ticket_sale_time.split(":")[1])

    horas, minutos = ticket_sale_time.split(":")

    ticket_sale_time: datetime.time = datetime.time(int(horas), int(minutos))

    return event_name, ticket_sale_date, ticket_sale_time


def parse_html_date(html_date: str) -> datetime.date:
    months = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
        "Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4, "Mai": 5, "Jun": 6,
        "Jul": 7, "Ago": 8, "Set": 9, "Out": 10, "Nov": 11, "Dez": 12
    }
    day, month_name = html_date.split()[1], html_date.split()[3]
    month = months[month_name]
    year = datetime.datetime.now().year  # Assuming the year is the current year
    return datetime.date(year, month, int(day))


def buscar_evento(search_url: str, event_name: str, event_date: datetime.date) -> typing.Optional[str]:
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        eventos = soup.find_all('article', class_='card-event')
        for evento in eventos:
            titulo = evento.find('h5', class_='mb-1 mb-sm-3 text-dark').text.strip()
            data_html = evento.find('span', class_='mb-0 text-primary').text.strip()
            if titulo.lower() == event_name.lower() and parse_html_date(data_html) == event_date:
                link = evento.find('a', href=True)['href']
                return f"https://blacktag.com.br{link}"
    return None

def event_link(event_name: str, event_date: str, event_time: datetime.time) -> str:
    base_url = "https://blacktag.com.br/eventos?q="
    search_url = f"{base_url}{event_name.replace(' ', '-').lower()}"
    tempo_limite = 240  # tempo limite de 4 minutos

    # Convert event_date from string to datetime.date
    day, month, year = map(int, event_date.split('/'))
    event_date = datetime.date(year, month, day)

    inicio = time.time()
    while (time.time() - inicio) < tempo_limite:
        link_evento = buscar_evento(search_url, event_name, event_date)
        if link_evento:
            return link_evento
        time.sleep(10)  # Espera 10 segundos antes de tentar novamente

    return "Evento não encontrado dentro do limite de tempo."


def main() -> None:
    event_name, event_date, event_time = greet()
    link = event_link(event_name, event_date, event_time)
    print(f"Link do evento: {link}")


if __name__ == "__main__":
    main()


# def test_event_link():
#     # Simular entrada do usuário
#     event_name = "TINDER MATCH - SUPRA DOM PEDRO"
#     event_date = "31/05/2024"
#     event_time = datetime.time(10, 0)
    
#     # Testar a função event_link
#     link = event_link(event_name, event_date, event_time)
#     print(f"Link do evento: {link}")
#     assert "https://blacktag.com.br/eventos/21179/tinder-match-supra-dom-pedro" in link


# if __name__ == "__main__":
#     test_event_link()