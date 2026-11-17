# visualizer.py - модуль для графіків

import os

import matplotlib.pyplot as plt


class Visualizer:
    # клас для побудови графіків

    def __init__(self, folder):
        # конструктор: запам'ятовуємо папку і створюємо її, якщо її немає
        self.folder = folder
        if not os.path.exists(folder):
            os.mkdir(folder)

    def price_histogram(self, df):
        # гістограма цін
        plt.figure(figsize=(8, 5))
        plt.hist(df["price"], bins=10, color="skyblue", edgecolor="black", label="Книги")
        plt.axvline(df["price"].mean(), color="red", linestyle="--", label="Середня ціна")
        plt.title("Розподіл цін на книги")
        plt.xlabel("Ціна, £")
        plt.ylabel("Кількість книг")
        plt.legend()
        plt.grid(True)
        plt.savefig(self.folder + "/price_histogram.png")
        plt.show()
        plt.close()

    def rating_bar(self, counts):
        # стовпчикова діаграма по рейтингу
        plt.figure(figsize=(8, 5))
        plt.bar(counts.index, counts.values, color="orange", label="Кількість книг")
        plt.title("Кількість книг за рейтингом")
        plt.xlabel("Рейтинг (зірки)")
        plt.ylabel("Кількість книг")
        plt.legend()
        plt.grid(True)
        plt.savefig(self.folder + "/rating_bar.png")
        plt.show()
        plt.close()

    def price_rating_plot(self, prices):
        # графік середньої ціни від рейтингу
        plt.figure(figsize=(8, 5))
        plt.plot(prices.index, prices.values, marker="o", color="green", label="Середня ціна")
        plt.title("Середня ціна залежно від рейтингу")
        plt.xlabel("Рейтинг (зірки)")
        plt.ylabel("Середня ціна, £")
        plt.legend()
        plt.grid(True)
        plt.savefig(self.folder + "/price_by_rating.png")
        plt.show()
        plt.close()