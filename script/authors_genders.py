import pandas as pd

# Загрузка данных
file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data.csv'
df = pd.read_csv(file_path)

# Сортировка по рейтингу и вывод топ-100 записей
top_100_books = df[['author', 'title', 'rating']].sort_values(by='rating', ascending=False).head(100)

# Вывод в консоль
for index, row in top_100_books.iterrows():
    print(f"Автор: {row['author']}")# Название: {row['title']}, Рейтинг: {row['rating']}")
