import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


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


# Основная функция для анализа гендера и визуализации
def analyze_gender(file_path):
    # Загрузка данных
    df = pd.read_csv(file_path)

    # Сортировка по рейтингу и выбор топ-100 записей
    top_100_books = df[['author', 'title', 'rating', 'price']].sort_values(by='rating', ascending=False).head(1000)

    # Создаем новую колонку с именами для анализа
    top_100_books['first_name'] = top_100_books['author'].apply(extract_first_name)

    # Определение пола авторов и добавление в DataFrame
    top_100_books['gender'] = top_100_books['first_name'].apply(get_gender)

    # Счетчик по гендеру
    gender_counts = top_100_books['gender'].value_counts()

    # Круговая диаграмма распределения гендера
    plt.figure(figsize=(8, 6))
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette('pastel'))
    plt.title('Gender Distribution of Top-100 Book Authors')
    plt.show(block=False)

    # Фильтрация данных для удаления Unknown
    top_100_books_filtered = top_100_books[top_100_books['gender'] != 'Unknown']

    # Диаграмма рассеяния рейтинг-цена с линиями и цветовой кодировкой гендера
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='rating', y='price', hue='gender', data=top_100_books_filtered,
                    palette={'Male': 'blue', 'Female': 'red'}, alpha=0.7, s=100)
    plt.title('Rating vs Price by Gender. First 1000 rows.')
    plt.xlabel('Rating')
    plt.ylabel('Price')

    # Настройка подписей на оси X
    plt.xticks([round(x, 2) for x in top_100_books['rating'].unique()[::4]])
    plt.legend(title='Gender')
    plt.show(block=False)

    # Боксплоты для сравнения цен по гендеру
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='gender', y='price', data=top_100_books_filtered,
                hue='gender', palette={'Male': 'lightblue', 'Female': 'lightpink'}, dodge=False, legend=False)
    plt.title('Price Distribution by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Price')
    plt.show()


# Внешний вызов функции из другого файла
# file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data.csv'
# analyze_gender(file_path)
def run_gender_analysis():
    file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data.csv'
    analyze_gender(file_path)
