import pandas as pd
import requests
import time

# Загрузка очищенных данных
file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/cleaned_books_data.csv'
df = pd.read_csv(file_path)

# Функция для получения данных книги по названию с использованием Open Library API
def get_book_data_by_title(title):
    url = f'https://openlibrary.org/search.json?title={title}'
    for _ in range(3):  # Попробовать запрос трижды
        try:
            response = requests.get(url, timeout=10)  # Устанавливаем тайм-аут на 10 секунд
            response.raise_for_status()  # Проверка статуса ответа
            books = response.json().get('docs', [])
            if books:
                book_info = books[0]
                pages = book_info.get('number_of_pages_median', None)
                publish_date = book_info.get('first_publish_year', None)
                return pages, publish_date
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API для книги '{title}': {e}")
            # time.sleep(2)  # Увеличиваем время задержки перед повторной попыткой
    return None, None

# Функция для заполнения пропущенных данных
def fill_missing_data(df, save_interval=50):
    processed_count = 0  # Счетчик обработанных записей
    total_processed = 0  # Общий счетчик обработанных записей
    try:
        for index, row in df.iterrows():
            if pd.isna(row['publishDate']) or pd.isna(row['pages']):
                title = row['title']
                original_pages = row['pages']
                original_publish_date = row['publishDate']

                # Получаем данные по названию
                pages, publish_date = get_book_data_by_title(title)

                # Если данные найдены, обновляем DataFrame
                if pd.isna(row['pages']) and pages:
                    df.at[index, 'pages'] = pages
                if pd.isna(row['publishDate']) and publish_date:
                    publish_date_formatted = f"{publish_date}-01-01" if publish_date else None
                    df.at[index, 'publishDate'] = publish_date_formatted

                # Выводим информацию для проверки
                print(f"number: {total_processed + 1}")
                # print(f"ISBN: {row['isbn']}")
                print(f"Title: {title}")
                print(f"Pages: {original_pages} -> {df.at[index, 'pages']}")
                print(f"Publish Date: {original_publish_date} -> {df.at[index, 'publishDate']}")
                print("-" * 40)

                processed_count += 1
                total_processed += 1

                # Проверка, нужно ли сохранить результаты
                if processed_count >= save_interval:
                    save_data(df, file_path)
                    processed_count = 0  # Сброс счетчика после сохранения

        # Сохранение оставшихся данных, если они есть
        if processed_count > 0:
            save_data(df, file_path)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        save_data(df, file_path)
        print("Данные сохранены перед завершением программы.")
    print(f"Всего обработано записей: {total_processed}")

# Функция для сохранения данных
def save_data(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

# Заполняем пропущенные данные для всех строк с пустыми значениями
fill_missing_data(df)
save_data(df, file_path)

print(f"Обновленные данные сохранены в {file_path}")
