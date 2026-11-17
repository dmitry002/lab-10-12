# main.py - головна програма з меню

import requests

from scraper import BookScraper
from analyzer import BookAnalyzer
from visualizer import Visualizer

URL = "https://books.toscrape.com/"
FOLDER = "results"


def input_number(text, min_value, max_value):
    # вводимо число поки не буде правильне
    while True:
        try:
            value = float(input(text))
            if value >= min_value and value <= max_value:
                return value
            else:
                print("Число має бути від", min_value, "до", max_value)
        except ValueError:
            print("Помилка: потрібно ввести число")


def show_menu():
    print()
    print("===== АНАЛІЗ КНИЖКОВОГО САЙТУ =====")
    print("1 - Зібрати дані з сайту")
    print("2 - Показати статистику")
    print("3 - Пошук книг за ціною")
    print("4 - Побудувати графіки")
    print("5 - Зберегти результати (CSV, JSON, TXT)")
    print("6 - Завантажити дані з CSV-файлу")
    print("0 - Вихід")


def main():
    scraper = BookScraper(URL)
    analyzer = BookAnalyzer()
    visualizer = Visualizer(FOLDER)

    while True:
        show_menu()
        choice = input("Ваш вибір: ")

        try:
            if choice == "0":
                print("Роботу завершено")
                break

            elif choice == "1":
                pages = int(input_number("Скільки сторінок зібрати (1-50)? ", 1, 50))
                books = scraper.scrape(pages)
                analyzer.load_data(books)

            elif choice == "6":
                analyzer.load_csv(FOLDER + "/books.csv")

            elif choice in ["2", "3", "4", "5"] and not analyzer.has_data():
                print("Спочатку зберіть дані (пункт 1) або завантажте їх з файлу (пункт 6)")

            elif choice == "2":
                print()
                print("--- Статистика ---")
                stats = analyzer.get_stats()
                for key in stats:
                    print(key + ":", stats[key])
                print()
                print("Кількість книг за рейтингом:")
                counts = analyzer.count_by_rating()
                for rating in counts.index:
                    print("Рейтинг", rating, ":", counts[rating], "книг")
                print()
                print("Топ-5 найдорожчих книг:")
                top = analyzer.top_expensive()
                for index, row in top.iterrows():
                    print(row["title"][:50], "-", row["price"], "£, рейтинг", row["rating"])

            elif choice == "3":
                min_price = input_number("Мінімальна ціна: ", 0, 1000)
                max_price = input_number("Максимальна ціна: ", min_price, 1000)
                found = analyzer.find_by_price(min_price, max_price)
                print("Знайдено книг:", len(found))
                # показуємо тільки перші 20 книг щоб не було дуже довго
                count = 0
                for index, row in found.iterrows():
                    print(row["title"][:50], "-", row["price"], "£, рейтинг", row["rating"])
                    count = count + 1
                    if count == 20:
                        print("... показано 20 з", len(found), "(всі книги є у файлі books.csv)")
                        break

            elif choice == "4":
                df = analyzer.get_data()
                visualizer.price_histogram(df)
                visualizer.rating_bar(analyzer.count_by_rating())
                visualizer.price_rating_plot(analyzer.price_by_rating())
                print("Графіки збережено у папці", FOLDER)

            elif choice == "5":
                analyzer.save(FOLDER)

            else:
                print("Немає такого пункту меню")

        # обробка помилок
        except requests.exceptions.ConnectionError:
            print("Помилка: немає з'єднання з сайтом. Перевірте інтернет")
        except requests.exceptions.Timeout:
            print("Помилка: сайт не відповідає")
        except requests.exceptions.HTTPError as e:
            print("Помилка сторінки:", e)
        except FileNotFoundError as e:
            print("Помилка:", e)
        except ValueError as e:
            print("Помилка даних:", e)
        except Exception as e:
            print("Непередбачена помилка:", e)


main()