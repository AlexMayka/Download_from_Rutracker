import requests
from bs4 import BeautifulSoup
import urllib


def connection_setup():
    """
    Функция для настройка сессии requests для дальнейшей работы
    Function for setting up the requests session for further work

    :return: session - сессии requests
    """

    # Прокси (ip) для обхода блокировки сайта
    proxies = {
        "http": "http://145.40.121.201:3128",
        "https": "http://145.40.121.201:3128",
    }

    session = requests.Session()
    session.proxies.update(proxies)
    return session


def login_in_site(session):
    """
    Авторизация на сайте Rutraacker
    Authorization on the Rutracker website

    :param session: сессия запроса
    :return: req: ответ на вход
             session: сессия запроса
    """

    # Настройка параметров для авторизации
    data = {
        'login_username': "das912",
        'login_password': "lyc9x",
        'login': 'pushed',
        'redirect': 'index.php'
    }

    # Отправка запроса для авторизации
    req = session.post("https://rutracker.org/forum/login.php",
                       data=data)

    print(req)
    return req, session


def search_data(session):
    """
    Поиск на сайте и вывод результатов (задание б)
    :param session: сессия запроса
    :return: list_torrent_files: словарь с результатом поиска
             session: сессия запроса
    """
    def input_data():
        """
        Ввод дааных для поиска на сайте
        Entering data to search on the site

        :return: req: текста страницы с результатами запроса
                 count_query: кол-во выдаваемых результатов
        """
        # Ввод пользователя данных
        query_text = input("Введите данные для поиска: ")
        count_query = int(input("Введите данные для поиска (не наглеть!!!!): "))

        # Получение текста странички с результатами запроса
        req = session.get(f"https://rutracker.org/forum/tracker.php?nm={query_text}")
        return req, count_query

    def data_output():
        """
        Вывод результатов поиска сайта
        :param: req: текста страницы с результатами запроса
                count_query: кол-во выдаваемых результатов
        :return: list_torrent_files: словарь с результатом поиска
                 session: сессия запроса
        """
        # Парсинг сайта
        text_get = BeautifulSoup(req.text, "html.parser")
        allobject = text_get.findAll('a', class_='med tLink tt-text ts-text hl-tags bold')

        # Вывод результатов и занесение их в словарь
        num = 1
        list_torrent_files = {}
        while num <= count_query and num < len(allobject):
            print(f"{num} - {allobject[num].contents[0]}")
            list_torrent_files[str(num)] = {'id': allobject[num]['data-topic_id'], 'name': allobject[num].contents[0]}
            num += 1

        return list_torrent_files

    req, count_query = input_data()
    list_torrent_files = data_output()
    return list_torrent_files, session


def download_file(session, list_torrent_files):
    """
    Скачивание файла (задание с)
    :param session: сессия запроса
    :param list_torrent_files: словарь с результатом поиска
    :return: -
    """

    # Ввод номера списка для скачивания файла
    dow_num = input("Введите номер для скачивания: ")
    dow_id = list_torrent_files[dow_num]['id']
    dow_name = list_torrent_files[dow_num]['name']

    # Отправляем запрос для скачивания файла
    req = session.get(f"https://rutracker.org/forum/dl.php?t={dow_id}")

    # Записываем файл
    with open(f'tutorial.torrent', 'wb') as f:
        f.write(req.content)


if __name__ == '__main__':
    session = connection_setup()
    answer_one, session = login_in_site(session)
    list_torrent_files, session = search_data(session)
    download_file(session, list_torrent_files)
