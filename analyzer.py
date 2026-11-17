# analyzer.py - модуль для обробки і аналізу даних

import json
import os

import pandas as pd

from scraper import RATINGS


class BookAnalyzer:
    # клас для очищення і аналізу даних

    def __init__(self):
        self.__df = None   # тут буде таблиця з книгами

    def load_data(self, books):
        # очищаємо дані і робимо таблицю
        if len(books) == 0:
            raise ValueError("немає даних")
        for book in books:
            # ціна "£51.77" -> 51.77
            book["price"] = float(book["price"].replace("£", ""))
            # рейтинг "Three" -> 3
            book["rating"] = RATINGS[book["rating"]]
            # прибираємо пробіли
            book["availability"] = book["availability"].strip()
        df = pd.DataFrame(books)
        df = df.drop_duplicates()
        df = df.dropna()
        self.__df = df
        print("Дані очищено. Записів:", len(df))

    def has_data(self):
        # перевірка чи є дані
        if self.__df is None:
            return False
        return len(self.__df) > 0

    def get_data(self):
        return self.__df

    def get_stats(self):
        # основна статистика
        df = self.__df
        stats = {}
        stats["Кількість книг"] = len(df)
        stats["Мінімальна ціна"] = round(df["price"].min(), 2)
        stats["Максимальна ціна"] = round(df["price"].max(), 2)
        stats["Середня ціна"] = round(df["price"].mean(), 2)
        stats["Медіана ціни"] = round(df["price"].median(), 2)
        stats["Середній рейтинг"] = round(df["rating"].mean(), 2)
        return stats

    def count_by_rating(self):
        # скільки книг з кожним рейтингом
        return self.__df["rating"].value_counts().sort_index()

    def price_by_rating(self):
        # середня ціна для кожного рейтингу
        return self.__df.groupby("rating")["price"].mean().round(2)

    def top_expensive(self, n=5):
        # n найдорожчих книг
        df = self.__df.sort_values("price", ascending=False)
        return df.head(n)

    def find_by_price(self, min_price, max_price):
        # пошук книг в діапазоні цін
        df = self.__df
        found = df[(df["price"] >= min_price) & (df["price"] <= max_price)]
        found = found.sort_values("price")
        return found

    def save(self, folder):
        # зберігаємо в csv, json і txt
        if not os.path.exists(folder):
            os.mkdir(folder)
        self.__df.to_csv(folder + "/books.csv", index=False, encoding="utf-8-sig")
        data = self.__df.to_dict(orient="records")
        with open(folder + "/books.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open(folder + "/stats.txt", "w", encoding="utf-8") as f:
            stats = self.get_stats()
            for key in stats:
                f.write(key + ": " + str(stats[key]) + "\n")
        print("Збережено: books.csv, books.json, stats.txt у папці", folder)

    def load_csv(self, path):
        # завантаження даних з csv файлу
        if not os.path.exists(path):
            raise FileNotFoundError("файл " + path + " не знайдено")
        df = pd.read_csv(path)
        if "price" not in df.columns or "rating" not in df.columns:
            raise ValueError("у файлі немає потрібних стовпців")
        self.__df = df
        print("Завантажено записів:", len(df))