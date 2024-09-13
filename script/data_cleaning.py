import numpy as np
import pandas as pd


file_path = ('C:/Users/inger/PycharmProjects/pythonProject1/data/books_1.Best_Books_Ever.csv')
df = pd.read_csv(file_path)

# Настройка отображения всех колонок и их ширины
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', 1000)  # Установить ширину вывода

print("Количество пропущенных значений после очистки:")
print(df.isnull().sum())
print(df.info())

# Заполнение пропусков
# df['series'].fillna('Unknown', inplace=True) #df.method({col: value}, inplace=True)
df.fillna({'series': 'Unknown'},  inplace=True)
df.fillna({'language': df['language'].mode()[0]}, inplace=True)
df.fillna({'bookFormat': 'Unknown'}, inplace=True)
df.fillna({'publisher': 'Unknown'}, inplace=True)
df.fillna({'firstPublishDate': 'Unknown'}, inplace=True)
df.fillna({'publishDate': 'Unknown'}, inplace=True)


df['author'] = df['author'].str.replace(r'\s*\(Goodreads Author\)', ' (GA)', regex=True)

df.drop(columns=['edition'], inplace=True)
df.drop(columns=['coverImg'], inplace=True)

# Заполняем пропуски в числовых столбцах медианным значением
# df['price'] = df['price'].replace(0, np.nan)
df['pages'] = pd.to_numeric(df['pages'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df.fillna({'likedPercent': df['likedPercent'].median()}, inplace=True)
df.fillna({'pages': df['pages'].median()}, inplace=True)
df.fillna({'price': df['price'].median()}, inplace=True)



# Проверка на наличие пропусков после очистки
print("Количество пропущенных значений после очистки:")
print(df.isnull().sum())

print(df.head())

cleaned_data_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/cleaned_books_data.csv'
df.to_csv(cleaned_data_path, index=False)
