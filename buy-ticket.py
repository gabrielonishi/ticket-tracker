# Selenium imports
import datetime
import os
import random
import re
import time
import typing

import requests
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import utils

# Amount of time before and after the ticket sale should open
SEARCH_TIME = 240
# Amount of time between requests
BETWEEN_REQUEST_TIME = 10


def greet() -> typing.Tuple[str, float]:
    event_name: str = input("Qual o nome da festa desejada?")

    ticket_sale_date: str = input(
        "Que dia os ingressos do evento abrem para venda? (dd/mm/aaaa)")

    # Validando data
    while not re.match(r"\d{2}/\d{2}/\d{4}", ticket_sale_date):
        ticket_sale_date = input(
            "Data inválida. Digite novamente usando o formato dd/mm/aaaa")

    day = int(ticket_sale_date.split("/")[0])
    month = int(ticket_sale_date.split("/")[1])
    year = int(ticket_sale_date.split("/")[2])

    ticket_sale_time: str = input(
        "Que horas os ingressos do evento abrem para venda? (hh:mm)")

    # Validando horário
    while not re.match(r"\d{2}:\d{2}", ticket_sale_time):
        ticket_sale_time = input(
            "Horário inválido. Digite novamente usando o formato hh:mm")

    horas: int = int(ticket_sale_time.split(":")[0])
    minutos: int = int(ticket_sale_time.split(":")[1])

    ticket_sale_epoch = datetime.datetime(
        year, month, day, horas, minutos).timestamp()

    if ticket_sale_epoch < datetime.datetime.now().timestamp():
        raise ValueError(
            "Data e hora de venda de ingressos inválida (no passado)")

    return event_name, ticket_sale_epoch


def get_event_path(search_url: str) -> typing.Optional[str]:
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.find_all('article', class_='card-event')
        if len(events) > 1:
            raise ValueError(
                "More than one event found, please be more specific")
        elif len(events) == 0:
            return None
        event = events[0]
        return event.find('a', href=True)['href']
    return None


def sleep_until(set_time: float) -> None:
    while True:
        if datetime.datetime.now().timestamp() > set_time:
            break
        print(set_time, datetime.datetime.now().timestamp())
        print('entrou')
        time.sleep(1)


def search_event(event_name: str, ticket_sale_epoch: str) -> str:
    base_url = "https://blacktag.com.br/eventos?q="
    search_url = base_url + event_name.replace(' ', '+').lower()

    # Sleep until 2 minutes before the ticket sale
    sleep_until(ticket_sale_epoch - SEARCH_TIME / 2)

    inicio = time.time()
    while datetime.datetime.now().timestamp() < ticket_sale_epoch + SEARCH_TIME:
        event_path = get_event_path(search_url)
        if event_path:
            return "https://blacktag.com.br" + event_path + "/ingressos"
        time.sleep(BETWEEN_REQUEST_TIME)

    raise TimeoutError("Event not found")


def buy_ticket(buy_ticket_url: str) -> None:
    # Using random user agents to avoid host suspition
    u_agent = random.choice(utils.user_agents)

    arguments = [
        "--disable-cookies",
        "--disable-local-storage",
        "--disable-session-storage",
        "--block-third-party-cookies"
        f"user-agent={u_agent}"
    ]

    chrome_options = Options()
    for arg in arguments:
        chrome_options.add_argument(arg)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url=buy_ticket_url)

    driver.implicitly_wait(10)
    select_element = driver.find_element(By.ID, 'event-ticket-0-quantity')

    select = Select(select_element)

    select.select_by_value('1')

    button_element = driver.find_element(
        By.XPATH, "//button[text()='Comprar' and contains(@class, 'btn-info')]")
    button_element.click()

    email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'email')))

    load_dotenv(find_dotenv())

    email.send_keys(os.environ.get('BLACKTAG_USERNAME'))
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(os.environ.get('BLACKTAG_PASSWORD'))

    button_element = driver.find_element(
        By.XPATH, "//button[text()='Entrar']")
    button_element.click()

    request_code_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
                                       By.XPATH, "//button[contains(@class, 'btn-whatsapp') and @data-provider='whatsapp']")))

    request_code_element.click()

    code_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sms-code"))
    )

    confirm_button = driver.find_element(
        By.XPATH, "//button[text()='Confirmar']")

    WebDriverWait(driver, 300, poll_frequency=1).until(
        lambda d: len(code_input.get_attribute("value")
                      ) == 6 and code_input.get_attribute("value").isdigit()
    )

    confirm_button.click()

    ok_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='OK']"))
    )

    ok_button.click()

    time.sleep(10)


def main() -> None:
    # event_name, ticket_sale_date, ticket_sale_time = greet()
    # buy_ticket_url = search_event(event_name, ticket_sale_epoch)
    buy_ticket_url = "https://blacktag.com.br/eventos/20565/pagode-da-arena/ingressos"

    buy_ticket(buy_ticket_url)

    # link = event_link(event_name, ticket_sale_date, ticket_sale_time)
    # print(f"Link do evento: {link}")


if __name__ == "__main__":
    main()
