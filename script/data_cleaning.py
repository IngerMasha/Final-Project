import pandas as pd
import re

# Загрузка данных
file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/books_1.Best_Books_Ever.csv'
df = pd.read_csv(file_path)

pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', 1000)  # Установить ширину вывода

print("Количество пропущенных значений после очистки:")
print(df.isnull().sum())
print(df.head())
# Функция для проверки, содержит ли название только латинские буквы
def is_latin(text):
    return bool(re.match(r'^[a-zA-Z0-9\s.,!?\'":;()-]*$', str(text)))

# Применяем функцию is_latin для фильтрации строк с латинскими названиями
df_latin = df[df['title'].apply(is_latin)]

# Удаление строк, содержащих '(Goodreads Author)' в имени автора
df_cleaned = df_latin[~df_latin['author'].str.contains(r'\(Goodreads Author\)', na=False)]

# Удаление явных дубликатов по ISBN, названию и автору
df_cleaned = df_cleaned.drop_duplicates(subset=['title', 'author'], keep='first')

# Сохранение очищенных данных
new_file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/cleaned_books_data.csv'
df_cleaned.to_csv(new_file_path, index=False)

print(f"Данные сохранены в файл: {new_file_path}")

# print(df_cleaned.isnull().sum())

