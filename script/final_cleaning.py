import pandas as pd
import numpy as np
from datetime import datetime

# Загрузка данных
file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/cleaned_books_data.csv'
df = pd.read_csv(file_path)

# Функция для приведения дат к формату yyyy-mm-dd
def reformat_date(date):
    if pd.isna(date) or date == 'Unknown':
        return date  # Если дата отсутствует или указана как Unknown, возвращаем как есть

    # Если дата в формате yyyy-mm-dd, возвращаем как есть
    try:
        return pd.to_datetime(date).strftime('%Y-%m-%d')
    except:
        pass

    # Если дата только год, добавляем месяц и день
    try:
        year = int(date)
        return f'{year}-01-01'
    except:
        pass

    # Если дата в формате, например, "February 20th 2015"
    try:
        return datetime.strptime(date, '%B %dth %Y').strftime('%Y-%m-%d')
    except:
        pass

    try:
        return datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
    except:
        pass

    return 'Unknown'  # Возвращаем Unknown, если формат не удалось определить

# Применение функции ко всем значениям в столбце publishDate
df['publishDate'] = df['publishDate'].apply(reformat_date)
# Заполнение оставшихся пропусков в столбце publishDate значением 'Unknown'
df['publishDate'] = df['publishDate'].fillna('Unknown')

# Преобразование столбца pages в числовой формат, удаление некорректных значений
df['pages'] = pd.to_numeric(df['pages'], errors='coerce')
df.fillna({'pages': df['pages'].median()}, inplace=True)

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df.fillna({'price': df['price'].median()}, inplace=True)

df.fillna({
    'series': 'Unknown',
    'language': df['language'].mode()[0],  # Заполнение модой
    'bookFormat': 'Unknown',
    'publisher': 'Unknown',
    'firstPublishDate': 'Unknown'
}, inplace=True)




# Сохранение финальных данных
final_file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data.csv'
df.to_csv(final_file_path, index=False)
print(f"Финальные данные сохранены в файл: {final_file_path}")
