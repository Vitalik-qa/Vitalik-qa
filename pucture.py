import unittest
import sys
import pytest
import os
import time
import datetime
import re
import multiprocessing
import random
import urllib.request
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
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# Подключаем веб браузер
s = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=s)
# Открываем Яндекс
driver.get("https://yandex.ru/images/")

# Открываем окно на весь экран
driver.maximize_window()

# Проверка
assert "Яндекс" in driver.title
assert "No results found." not in driver.page_source

arr = []
for i in range(1, 5):
    # // *[ @class = 'PopularRequestList'] / div[2]
    images = driver.find_element(
        By.XPATH, "//*[@class ='PopularRequestList']/div[" + str(i) + "]"
    )
    print(i)
    print(images.text)
    arr.append(images.text)
# Выбираем тему картин
images_click = driver.find_element(
    By.XPATH, "//*[@class ='PopularRequestList']/div[" + str(random.randint(1, 4)) + "]"
)
images_click.click()

# Выбираем картинку
driver.implicitly_wait(20)
elem = driver.find_element(
    By.XPATH,
    "//*[@class = 'serp-list serp-list_type_search serp-list_unique_yes serp-list_rum_yes serp-list_justifier_yes serp-controller__list counter__reqid clearfix i-bem serp-list_js_inited']/div["
    + str(random.randint(1, 50))
    + "]",
)
elem.click()

# Получаем ссылку на изображение
open = driver.find_element(
    By.XPATH,
    "//*[@class = 'MMButton MMButton_type_link MMViewerButtons-OpenImage MMViewerButtons-OpenImage_isOtherSizesEnabled MMViewerButtons-OpenImage_theme_primary']",
)
link = open.get_attribute("href")
print(link)

# Скачиваем изображение
urllib.request.urlretrieve(link, "C://Users//Виталий//Desktop//Autotest//python.png")

# Ждем 20 сек
time.sleep(20)

# Закрываем браузер
driver.close()
