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

# Проверка наличия элемента
def check(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# Подключаем веб браузер
s = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=s)
# Открываем Яндекс
driver.get("https://yandex.ru/maps/")

# Открываем окно на весь экран
driver.maximize_window()

# Проверка
assert "Яндекс" in driver.title
assert "No results found." not in driver.page_source

# Находим Поисковую строку
way = driver.find_element(By.XPATH, "//*[@class='input__control _bold']")
way.send_keys("Ростов-на-Дону площадь Гагарина, 1")
way.send_keys(Keys.ENTER)

# Нажимаем на маршрут
driver.implicitly_wait(20)
route = driver.find_element(By.XPATH, "//*[text()='Маршрут']")
route.click()

# Ввод места отбытия
to_place = driver.find_element(
    By.XPATH, "//*[@class='input__control' and @placeholder= 'Откуда']"
)
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

# Цикл проверки наличия элмента
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
    # Выводим
    print("Маршрут №", i, ":", time.text, ",", distances.text)
    # Увеличиваем i на 1
    i += 1
    # Изменяем переменную xpath
    xpath = (
        "//*[@class = 'route-list-view__list']/div[" + str(i) + "]/div[1]/div[1]/div[1]"
    )

# Закрываем браузер
driver.close()
