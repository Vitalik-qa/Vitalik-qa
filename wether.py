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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        # Подключаем веб браузер
        s = "chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=s)

    def test_searchKeys_in_python_org(self):
        driver = self.driver
        # Открываем Яндекс
        driver.get("https://yandex.ru/")
        # Открываем окно на весь экран
        driver.maximize_window()
        # Проверка
        assert "Яндекс" in driver.title
        assert "No results found." not in driver.page_source
        # Находим Поисковую строку
        elem = driver.find_element(By.ID, "text")
        # Вводим слово в поисковую строку
        elem.send_keys("Погода")
        # Нажимаем Enter
        elem.send_keys(Keys.ENTER)
        # Находим элементы с погоддой
        weather = driver.find_element(
            By.XPATH, "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[1]"
        )
        condition_web = driver.find_element(
            By.XPATH, "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[2]"
        )
        # Находим элемент с отображением скрости ветра
        flesh_web = driver.find_element(
            By.XPATH,
            "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[2]/div/div[1]/div[1]",
        )
        # Обрезаем его,до первого символа
        flesh = flesh_web.text[0]
        # Обрезаем состояния погода до скорости ветра
        condition = condition_web.text.partition(flesh)[0]
        # Создаем элемент сегоднешняя дата
        dt_now = datetime.date.today()
        # Открываем файл
        f = open("C://Users//Виталий//Desktop//Autotest//weather.txt", "w")
        # Запись погода в файл
        f.write("Погода сейчаc: " + weather.text + " " + condition.rstrip() + "\n")
        # Вывод погоды в  консоль
        print("Погода сейчаc:", weather.text, condition.rstrip())
        # Создаем переменную для увеличение даты погоды
        day_count = 0
        # Цикл для извлечение погоды на 6 дней
        for i in range(1, 7):
            # Дата на следующего дня
            tomorrow = dt_now + datetime.timedelta(days=day_count)
            # Температура на день
            day = driver.find_element(
                By.XPATH,
                "//*[@id='search-result']/li[1]/div/div[3]/div/div["
                + str(i)
                + "]/div[2]",
            )
            # Температура на ночь
            niht = driver.find_element(
                By.XPATH,
                "//*[@id='search-result']/li[1]/div/div[3]/div/div["
                + str(i)
                + "]/div[4]",
            )
            # Запись температуры в файл
            f.write(str(tomorrow) + " день:" + day.text + " ночь:" + niht.text + "\n")
            # Вывод температуры в консоль
            print(tomorrow, "день:", day.text, "ночь:", niht.text)
            # Увеличение переменной, следующий день
            day_count += 1
        # Закрываем файл
        f.close()
        # Делаем и сохраняем скрин с погодой
        driver.save_screenshot("C://Users//Виталий//Desktop//Autotest//weather.png")

    def tearDown(self):
        # Ожидание 5 сек.
        time.sleep(5)
        # Закрываем браузер
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
