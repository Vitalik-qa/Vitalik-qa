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
import requests
import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from allure_commons.types import AttachmentType


class TestPageSearch:

    def setup(self):
        s = 'chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=s)

    def teardown(self):
        time.sleep(5)
        self.driver.quit()

    @allure.feature('Open pages')
    @allure.story('Картинка')
    def test_pucture(self):
        """
        Этот тест проверяет  поиск картинки
        """
        with allure.step("Открытия сайта Яндекс"):
            driver = self.driver
            driver.get("https://yandex.ru/images/")
            # Проверка
            assert "Яндекс" in driver.title
            assert "No results found." not in driver.page_source

        arr_pucture = []

        with allure.step("Сохранение названия картинок"):
            for i in range(1,5):
                images = driver.find_element(By.XPATH, "//*[@class ='PopularRequestList']/div["+str(i)+"]")
                print(i)
                print(images.text)
                arr_pucture.append(images.text)

        with allure.step("Выбор тематики"):
            images_click = driver.find_element(By.XPATH, "//*[@class ='PopularRequestList']/div["+str(random.randint(1, 4))+"]")
            images_click.click()

        with allure.step("Выбор картинки"):
            driver.implicitly_wait(20)
            elem = driver.find_element(By.XPATH,"//*[@class = 'serp-list serp-list_type_search serp-list_unique_yes serp-list_rum_yes serp-list_justifier_yes serp-controller__list counter__reqid clearfix i-bem serp-list_js_inited']/div["+str(random.randint(1, 50))+"]")
            elem.click()

        with allure.step("Получение ссылки на скачивание"):
            open = driver.find_element(By.XPATH,"//*[@class = 'Button2 Button2_size_m Button2_type_link Button2_view_action Button2_width_max ViewerButton MMViewerButtons-OpenImage MMViewerButtons-OpenImage_isOtherSizesEnabled']")
            link = open.get_attribute('href')
            print(link)

        with allure.step("Скачивание картинки"):
            urllib.request.urlretrieve(link, "python.jpg")
