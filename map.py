import unittest
import sys
import os
import time
import datetime
import re
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Функция проверки наличие элемента
def check(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# Подключаем веб-браузер
s = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=s)
# Открытие ссылки
driver.get("https://yandex.ru/maps/")
# Открываем окно на весь экран
driver.maximize_window()
# Проверка заголовка
assert "Яндекс" in driver.title
assert "No results found." not in driver.page_source
# Находим Поисковую строку по XPATH
way = driver.find_element(By.XPATH, "//*[@class='input__control _bold']")
way.send_keys("Ростов-на-Дону площадь Гагарина, 1")
way.send_keys(Keys.ENTER)
# Ожидаем 20 секунд
driver.implicitly_wait(20)
# Находим маршрут по XPATH
route = driver.find_element(By.XPATH, "//*[text()='Маршрут']")
route.click()
# Находим поле места отбытия
to_place = driver.find_element(
    By.XPATH, "//*[@class='input__control' and @placeholder= 'Откуда']"
)
# Ввод места отбытия
to_place.send_keys("Большая Садовая ул., 134/157")
to_place.send_keys(Keys.ENTER)
# Выбираем маршшру
foot = driver.find_element(
    By.XPATH, "//*[@class='route-travel-modes-view__mode _mode_pedestrian']"
)
foot.click()
# Переменные для проверки наличия элменета
xpath = "//*[@class = 'route-list-view__list']/div[1]/div[1]/div[1]/div[1]"
i = 1
# Цикл while для проверки наличия вариантов маршрута
while check(xpath):
    # Находим время маршрута
    time = driver.find_element(
        By.XPATH,
        "//*[@class = 'route-list-view__list']/div["
        + str(i)
        + "]/div[1]/div[1]/div[1]",
    )
    # Находим растония маршрута
    distances = driver.find_element(
        By.XPATH,
        " //*[@class = 'route-list-view__list']/div["
        + str(i)
        + "]/div[1]/div[1]/div[2]",
    )
    # Выводим информацию
    print("Маршрут №", i, ":", time.text, ",", distances.text)
    # Увеличиваем i на 1 для проверки наличия следующего маршрута
    i += 1
    # Изменяем переменную Хpath для проверки наличия следующего маршрута
    xpath = (
        "//*[@class = 'route-list-view__list']/div[" + str(i) + "]/div[1]/div[1]/div[1]"
    )
# Закрываем браузер
driver.close()
