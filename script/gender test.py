import pandas as pd
import re

# Загрузка данных имен из файлов
def load_names(file_path):
    with open(file_path, 'r') as file:
        names = {line.strip().lower() for line in file.readlines()}
    return names

# Путь к файлам с именами
male_names_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/names_data/male.txt'
female_names_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/names_data/female.txt'

# Загрузка имен
male_names = load_names(male_names_path)
female_names = load_names(female_names_path)

# Списки окончаний для определения пола
female_endings = ['a', 'ia', 'na', 'ine', 'ette', 'elle', 'y', 'ie']
male_endings = ['o', 'er', 'an', 'en', 'on', 'us', 's']

# Функция для проверки окончания имени
def check_name_ending(name):
    name = name.lower().strip()
    if any(name.endswith(end) for end in female_endings):
        return 'Female'
    if any(name.endswith(end) for end in male_endings):
        return 'Male'
    return 'Unknown'

# Функция для определения пола по имени
def get_gender(name):
    name = name.lower()
    if name in male_names:
        return 'Male'
    elif name in female_names:
        return 'Female'
    else:
        # Проверка на окончания
        return check_name_ending(name)

# Функция для выделения основного имени из строки автора
def extract_first_name(author):
    # Удаление скобок и всего, что в них содержится, а также удаление редакторов и переводчиков
    author = re.sub(r'\(.*?\)|editor|translator|illustrator', '', author, flags=re.IGNORECASE)
    # Разделение строки по запятым, союзам и символу "/"
    author_parts = re.split(r',| and | & |/', author)

    # Обработка первой части строки, которая обычно содержит основное имя
    first_part = author_parts[0].strip()

    # Удаление возможных инициалов и титулов в начале строки (например, "Dr.", "Mr.", "Ms.")
    first_part = re.sub(r'^[A-Z]\.?([A-Z]\.?)?\s+|Dr\.|Mr\.|Ms\.', '', first_part).strip()

    # Разделение на слова и выбор самого первого значимого слова
    name_parts = first_part.split()
    # Вернем первое слово, если оно длиннее 2 символов, иначе следующее
    for part in name_parts:
        if len(part) > 2:  # Проверяем, что слово длиннее 2 символов
            return part
    return name_parts[0] if name_parts else ''

# Функция для добавления столбца с полом автора
def add_gender_column(file_path):
    # Загрузка данных
    df = pd.read_csv(file_path)

    # Определение пола авторов и добавление в DataFrame
    df['gender'] = df['author'].apply(lambda x: get_gender(extract_first_name(x)))

    # Сохранение обновленного DataFrame в новый CSV файл
    output_file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data_with_gender.csv'
    df.to_csv(output_file_path, index=False)
    pd.set_option('display.max_columns', None)  # Показать все столбцы
    pd.set_option('display.width', 1000)  # Установить ширину вывода

    print(df.head())
    print(f"Обновленный файл сохранен как: {output_file_path}")

# Запуск функции для добавления колонки с полом автора
file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data.csv'
add_gender_column(file_path)
