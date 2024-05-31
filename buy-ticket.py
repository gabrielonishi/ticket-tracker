# Selenium imports
import datetime
import random
import re
import time
import typing

# Beautiful Soup imports
import bs4
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
    event_date: str = input("Qual a data do evento? (dd/mm/aaaa)")

    # Validando data
    while not re.match(r"\d{2}/\d{2}/\d{4}", event_date):
        event_date = input(
            "Data inválida. Digite novamente usando o formato dd/mm/aaaa")

    day, month, year = event_date.split("/")

    event_date: datetime.date = datetime.date(int(year), int(month), int(day))

    event_time: str = input("Qual o horário do evento? (hh:mm)")

    # Validando horário
    while not re.match(r"\d{2}:\d{2}", event_time):
        event_time = input(
            "Horário inválido. Digite novamente usando o formato hh:mm")

    horas: int = int(event_time.split(":")[0])
    minutos: int = int(event_time.split(":")[1])

    horas, minutos = event_time.split(":")

    event_time: datetime.time = datetime.time(int(horas), int(minutos))

    return event_name, event_date, event_time


def main() -> None:
    event_name, event_date, event_time = greet()
