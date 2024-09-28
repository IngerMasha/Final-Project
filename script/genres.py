import pandas as pd
import re

# Загрузка данных
file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data_with_gender.csv'
df = pd.read_csv(file_path)

# Список предпочтительных жанров (приоритетный порядок)
preferred_genres = [
    'Fiction', 'Fantasy', 'Science Fiction', 'Mystery', 'Romance', 'Thriller',
    'Historical Fiction', 'Horror', 'Nonfiction', 'Classics',
    'Graphic Novels', 'Poetry', 'Biography', 'Children’s', 'Drama', 'Contemporary',
    'Adventure', 'Crime', 'Dystopia'
]

# Функция для определения основного жанра
def determine_main_genre(genres, preferred_genres):
    genres_list = re.findall(r"'(.*?)'", genres) if pd.notna(genres) else []
    for genre in genres_list:
        if genre in preferred_genres:
            return genre
    # Возвращаем первый жанр или "Unknown", если нет подходящего жанра
    # return genres_list[0] if genres_list else 'Unknown'
    return 'Unknown'


pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', 1000)  # Установить ширину вывода
# Создание нового столбца с основным жанром
df['main_genre'] = df['genres'].apply(lambda x: determine_main_genre(x, preferred_genres))
print(df.head())
# Сохранение обработанных данных в новый CSV файл
output_file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data_with_gender_and_genres.csv'
df.to_csv(output_file_path, index=False)

print(f"Обработанная таблица сохранена в {output_file_path}")
