import sys
import os
import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service


# Запускаем браузе с настройка на отключение уведомления
s = "chromedriver.exe"
options = Options()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(executable_path=s, chrome_options=options)
# Открываем окно на весь экран
driver.get("https://ru.hitmotop.com")
# Раскрываем вкладку на весь экран
driver.maximize_window()
# Проверка заголовка
assert "Слушать" in driver.title
assert "No results found." not in driver.page_source
# Создаем файл для записи информации о музыке
f = open("C://Users//Виталий//Desktop//Autotest//ТОП-8 Музыка.txt", "w")
# Создаем  сегоднешнюю дату
dt_now = datetime.date.today()
# Создаем массив для хранение названия песен
collection = []
# Записываем в файл сегоднешнюю дату
f.write("ТОП-8 Музыка" + str(dt_now) + "\n")
# Цикл  for для  записи популярных песен
for i in range(1, 9):
    # Находим элемент Название песни
    name_music = driver.find_element(
        By.XPATH,
        "//*[@id='pjax-container']/div[1]/ul/li[" + str(i) + "]/div[3]/a/div[1]",
    )
    # Находим элемент Имя автора
    author_music = driver.find_element(
        By.XPATH,
        "//*[@id='pjax-container']/div[1]/ul/li[" + str(i) + "]/div[3]/a/div[2]",
    )
    # Находим элемент Продолжительность трека
    time_music = driver.find_element(
        By.XPATH,
        "//*[@id='pjax-container']/div[1]/ul/li[" + str(i) + "]/div[3]/div/div/div[1]",
    )
    # Выводи в консоль
    print(name_music.text, author_music.text, time_music.text)
    # Запись  информации о песни в файл
    f.write(
        str(i)
        + ". Название: "
        + name_music.text
        + " Автор:"
        + author_music.text
        + " Длительность:"
        + time_music.text
        + "\n"
    )
    # Запись названия песен в массив
    collection.append(name_music.text)
f.close()
# Выводи массива в консоль
print(collection)
# Получаем слуйное название песни
play_music = random.choice(collection)
# Находим поисковую строку на сайте по Name
search = driver.find_element(By.NAME, "q")
# Вводи в нее выбранное название песни
search.send_keys(play_music)
search.send_keys(Keys.ENTER)
# Ожидаем кнопку запуска трека
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="jp_container"]/div/div/div[2]/div/div[1]/button[2]')
    )
)
# Находим кнопу воспроизведение музыки
play = driver.find_element(
    By.XPATH, '//*[@id="jp_container"]/div/div/div[2]/div/div[1]/button[2]'
)
# Жмем кнопку воспроизведение музыки
play.click()
# Ждем 20 сек
time.sleep(20)
# Закрываем браузер
driver.close()
