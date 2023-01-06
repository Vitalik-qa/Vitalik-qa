import sys
import os
import time
import datetime
import random
import allure
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from allure_commons.types import AttachmentType


class TestPageSearch:

    def setup(self):
        s = 'chromedriver.exe'
        options = Options()
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(executable_path=s, chrome_options=options)

    def teardown(self):
        self.driver.quit()

    @allure.feature('Open pages')
    @allure.story('Музыка')
    def test_music(self):

        with allure.step("Открытия сайта Яндекс"):
            driver = self.driver
            # Открываем сайт
            driver.get("https://ru.hitmotop.com")
            # Проверка
            assert "Слушать" in driver.title
            assert "No results found." not in driver.page_source

        # Создаем файл
        f = open("C://Users//Vitaliy//Desktop//Avtotest//Музыка.txt","w")
        # Создаем элемент даты
        date_now = datetime.date.today()
        # Создаем массив
        collection_music = []
        # Записываем в файл
        f.write('ТОП-8 Музыка ' + str(date_now) + "\n")

        with allure.step("Цикл просмотра ТОП"):
            for count_div in range(1,9):
                # Находим элемент название песни
                name_music = driver.find_element(By.XPATH, "//*[@id='pjax-container']/div[1]/ul/li[" + str(count_div) + "]/div[3]/a/div[1]")
                # Находим элемент имя автора
                author_music = driver.find_element(By.XPATH, "//*[@id='pjax-container']/div[1]/ul/li[" + str(count_div) + "]/div[3]/a/div[2]")
                # Находим элемент продолжительность трека
                time_music = driver.find_element(By.XPATH, "//*[@id='pjax-container']/div[1]/ul/li[" + str(count_div) + "]/div[3]/div/div/div[1]")
                # Выводи в консоль
                print(name_music.text, author_music.text, time_music.text)
                # Запись в файл
                f.write(str(count_div) + '. Название: ' + name_music.text + ' Автор:' + author_music.text + ' Длительность:' + time_music.text + "\n")
                # Запись названия песни в массив
                collection_music.append(name_music.text)

        f.close()
        # Вывод массива
        print(collection_music)
        # Получаем слуйное название песни
        play_music = random.choice(collection_music)

        with allure.step("Ввод названи песни"):
            # Находим поисковую строку
            search = driver.find_element(By.NAME, 'q')
            # Ввод  название песни
            search.send_keys(play_music)
            search.send_keys(Keys.ENTER)


        with allure.step("Воспроизведение песни"):
            # Ожидаем кнопку запуска трека
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'p-track-play__text')))
            # Находим кнопу воспроизведение музыки
            # play = driver.find_element(By.XPATH, '//*[@id="jp_container"]/div/div/div[2]/div/div[1]/button[2]')
            # Жмем кнопку воспроизведение музыки
            element.click()
            # Ждем 20 сек
            time.sleep(5)




