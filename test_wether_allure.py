import unittest
import sys
import pytest
import os
import time
import datetime
import re
import allure
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType


class TestPageSearch:

    def setup(self):
        s = 'chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=s)

    def teardown(self):
        self.driver.quit()

    @allure.feature('Open pages')
    @allure.story('Погода')
    def test_wether(self):
        """
        Этот тест проверяет  поиск погоды
        """
        with allure.step("Открытия сайта Яндекс"):
            driver = self.driver
            driver.get("https://ya.ru/")
            assert "Яндекс" in driver.title
            assert "No results found." not in driver.page_source

        with allure.step("Ввод в поисковую строку"):
            elem = driver.find_element(By.ID, "text")
            elem.send_keys("Погода")
            elem.send_keys(Keys.ENTER)

        with allure.step("Поиск данных погоды"):
            weather = driver.find_element(By.XPATH, "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[1]")
            condition_web = driver.find_element(By.XPATH, "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[2]")

        with allure.step("Поиск скорости ветра"):
            flesh_web = driver.find_element(By.XPATH,
                                            "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[2]/div/div[1]/div[1]")
            flesh = flesh_web.text[0]
            condition = condition_web.text.partition(flesh)[0]

        # Создаем элемент сегоднешняя дата
        date_now = datetime.date.today()
        with allure.step("Запись в файл"):
            f = open("weather.txt", "w")
            f.write('Погода сейчаc: ' + weather.text + ' ' + condition.rstrip() + "\n")

        print('Погода сейчаc:', weather.text, condition.rstrip())
        # Создаем переменную для увеличение даты погоды
        day_count = 0
        with allure.step("Цикл погоды"):
            for day_count in range(0, 5):
                # Дата на следующего дня
                tomorrow = date_now + datetime.timedelta(days=day_count)

                with allure.step("Погда на день/ ночь"):
                    day = driver.find_element(By.XPATH,
                                          "//*[@id='search-result']/li[1]/div/div[3]/div/div[" + str(day_count + 1) + "]/div[2]")
                    niht = driver.find_element(By.XPATH,
                                           "//*[@id='search-result']/li[1]/div/div[3]/div/div[" + str(day_count + 1) + "]/div[4]")


                with allure.step("Запись в файл в цикле"):
                    print(tomorrow, 'день:', day.text, 'ночь:', niht.text)
                    f.write(str(tomorrow) + ' день:' + day.text + ' ночь:' + niht.text + "\n")

        f.close()
        driver.save_screenshot("weather.png")
