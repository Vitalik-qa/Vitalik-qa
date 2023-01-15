import unittest
import sys
import pytest
import os
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

# Функция проверки наличия веб элемента
def check(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# Подключаем веб-браузер
s = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=s)
# Открываем ссылку
driver.get("https://pass.rzd.ru/")
# Открываем окно на весь экран
driver.maximize_window()
# Проверка заголовка
assert "Пассажирам" in driver.title
assert "No results found." not in driver.page_source
# Находим поля для поиска маршрута: Место отправки
from_place = driver.find_element(By.ID, "name0")
from_place.send_keys("Москва")
from_place.send_keys(Keys.ENTER)
# Находим поля для поиска маршрута: Место прибытия
to_place = driver.find_element(By.ID, "name1")
to_place.send_keys("Ростов-на-Дону")
to_place.send_keys(Keys.ENTER)
# Находим поля для поиска маршрута: Время отправки
from_time = driver.find_element(By.ID, "date0")
# Создание даты
dt_now = datetime.date.today()
# Изменение дата  + 1 день
tomorrow = dt_now + datetime.timedelta(days=1)
# Очистка старой даты
from_time.send_keys(Keys.CONTROL + "a")
from_time.send_keys(Keys.DELETE)
# Ввод даты на завтра
from_time.send_keys(tomorrow.strftime("%d.%m.%Y"))
# Нажатие кнопки Поиск
search = driver.find_element(By.ID, "Submit")
search.send_keys(Keys.ENTER)
# Ожидание появления поездов
train_xpath = "//*[@id='Page0']/div/div[2]/div[1]/div[3]/div[1]"
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, train_xpath)))
# Переменные для цикла
price = 100000
j = 1
i = 1
# Цикл while для проверки наличия следующего поезда по порядку
while check(train_xpath):
    # Изменения переменных для проверки наличия элемента на страницы
    price_xpath = (
        "//*[@id='Page0']/div/div[2]/div[1]/div[3]/div["
        + str(j)
        + "]/div/div/div[1]/div[2]/div[1]/div["
        + str(i)
        + "]/div/div[3]/span[2]"
    )
    train_xpath = "//*[@id='Page0']/div/div[2]/div[1]/div[3]/div[" + str(j) + "]"
    # Цикл while для проверки наличие цены
    while check(price_xpath):
        # Поиск минимальной цены
        print(driver.find_element(By.XPATH, price_xpath).text)
        if price > int(
            (driver.find_element(By.XPATH, price_xpath).text).replace(" ", "")
        ):
            # Сохранения переменных: Названия поезда
            name = driver.find_element(
                By.XPATH,
                "//*[@id='Page0']/div/div[2]/div[1]/div[3]/div["
                + str(j)
                + "]/div/div/div[1]/div[1]/div[2]/span[2]",
            ).text
            # Сохранения переменных: Тип вагона
            ticket = driver.find_element(
                By.XPATH,
                "//*[@id='Page0']/div/div[2]/div[1]/div[3]/div["
                + str(j)
                + "]/div/div/div[1]/div[2]/div[1]/div["
                + str(i)
                + "]/div/div[2]/span",
            ).text
            # Сохранения переменных: Цена
            price = driver.find_element(
                By.XPATH,
                "//*[@id='Page0']/div/div[2]/div[1]/div[3]/div["
                + str(j)
                + "]/div/div/div[1]/div[2]/div[1]/div["
                + str(i)
                + "]/div/div[3]/span[2]",
            ).text
            # Убираем пробел в переменной с ценой и преобразуем в int
            price = int(price.replace(" ", ""))
        # Переходим на следующую цену
        i += 1
        # Изменяем  адрес цен на следующую
        price_xpath = (
            "//*[@id='Page0']/div/div[2]/div[1]/div[3]/div["
            + str(j)
            + "]/div/div/div[1]/div[2]/div[1]/div["
            + str(i)
            + "]/div/div[3]/span[2]"
        )
    # Изменяем и обновляем переменные для изменения адресов веб элементов, чтобы проверить наличие еще маршрутов
    j += 1
    i = 1
# Вывод информациив  консоль
print(
    "Минимальная цена покупки билета на сайте РЖД у ФПК:",
    price,
    "руб.",
    ticket,
    "Поезд:",
    name,
)
# Ожидание 5 сек.
time.sleep(5)
# Закрываем браузер
driver.close()
