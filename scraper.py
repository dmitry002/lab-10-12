# scraper.py - модуль для збору даних з сайту

import requests
from bs4 import BeautifulSoup

# словник щоб перевести рейтинг зі слова в число
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class BookScraper:
    # клас який завантажує сторінки і дістає з них книги

    def __init__(self, base_url):
        # конструктор: запам'ятовуємо адресу сайту
        self.__base_url = base_url   # адреса сайту (приватна)
        self.books = []

    def get_page(self, url):
        # завантажуємо сторінку
        response = requests.get(url, timeout=10)
        response.raise_for_status()   # якщо сторінка не відкрилась буде помилка
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def parse_books(self, soup):
        # шукаємо всі книги на сторінці
        result = []
        cards = soup.find_all("article", class_="product_pod")
        for card in cards:
            title = card.h3.a["title"]
            price = card.find("p", class_="price_color").text
            rating = card.find("p", class_="star-rating")["class"][1]
            stock = card.find("p", class_="availability").text
            book = {"title": title, "price": price, "rating": rating, "availability": stock}
            result.append(book)
        return result

    def scrape(self, pages):
        # проходимо по сторінках каталогу
        self.books = []
        for i in range(1, pages + 1):
            url = self.__base_url + "catalogue/page-" + str(i) + ".html"
            print("Завантаження сторінки", i, "з", pages, "...")
            soup = self.get_page(url)
            books_on_page = self.parse_books(soup)
            self.books = self.books + books_on_page
        print("Зібрано книг:", len(self.books))
        return self.books