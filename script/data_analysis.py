import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy.signal import find_peaks


cleaned_data_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/cleaned_books_data.csv'
df = pd.read_csv(cleaned_data_path)
# Настройка отображения всех колонок и их ширины
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', 1000)  # Установить ширину вывода

print(df.describe())

# Распределение рейтингов
sns.histplot(df['rating'], bins=50)
plt.title('Распределение рейтингов книг')
plt.xlabel('Рейтинг')
plt.ylabel('Количество книг')
plt.show()

# Распределение цен
bins = [0, 5, 10, 20, 50, 100, df['price'].max()]
labels = ['0-5 евро', '5-10 евро', '10-20 евро', '20-50 евро', '50-100 евро', '100+ евро']
df['price_category'] = pd.cut(df['price'], bins=bins, labels=labels)

sns.countplot(data=df, x='price_category', order=labels)
plt.title('Категоризация цен на книги')
plt.xlabel('Категория цены')
plt.ylabel('Количество книг')
plt.xticks(rotation=45)
plt.show()

# Предполагаем, что столбец 'genres' содержит списки жанров в виде строк
# Разбиваем строки с жанрами и собираем все жанры в один список
genres_list = df['genres'].apply(lambda x: x.strip("[]").replace("'", "").split(', '))
all_genres = [genre for sublist in genres_list for genre in sublist]

# Считаем частоту каждого жанра
genre_counts = Counter(all_genres)

# Преобразуем в датафрейм для визуализации
genre_counts_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count'])
genre_counts_df = genre_counts_df.sort_values(by='Count', ascending=False)

# Визуализация топ-10 жанров
sns.barplot(x='Genre', y='Count', data=genre_counts_df.head(10))
plt.title('Топ-10 популярных жанров')
plt.xlabel('Жанр')
plt.ylabel('Количество книг')
plt.xticks(rotation=45)
plt.show()

# Выбираем числовые столбцы для корреляции
numeric_cols = ['rating', 'numRatings', 'pages', 'price', 'likedPercent', 'bbeScore', 'bbeVotes']

# Вычисляем корреляционную матрицу
corr_matrix = df[numeric_cols].corr()

# Визуализация тепловой карты корреляций
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Корреляционная матрица')
plt.show()

# Боксплот для цены
sns.boxplot(y=df['price'])
plt.title('Боксплот цен книг')
plt.show()

# Боксплот для количества страниц
sns.boxplot(y=df['pages'])
plt.title('Боксплот количества страниц')
plt.show()

df_price_filtered = df[df['price'] <= 400]
sns.regplot(x='rating', y='price', data=df_price_filtered, line_kws={'color': 'red'})
plt.title('Зависимость рейтинга от цены')
plt.xlabel('Рейтинг')
plt.ylabel('Цена')
plt.show()

df_page_filtered = df[df['pages'] <= 1000]
sns.regplot(x='rating', y='pages',data=df_page_filtered, line_kws={'color': 'red'})
plt.title('Зависимость рейтинга от количества страниц')
plt.xlabel('Рейтинг')
plt.ylabel('Количество страниц')
plt.show()

# Убедимся, что 'publishDate' в формате datetime
# df['publishYear'] = df['publishDate'].dt.year
df['publishDate'] = pd.to_datetime(df['publishDate'], errors='coerce')

# Проверка первых строк после преобразования
print(df['publishDate'].head())

# Проверка количества пропущенных значений после преобразования
print(f"Количество некорректных дат: {df['publishDate'].isna().sum()}")

# Вывод строк, где publishDate не смогла быть преобразована
invalid_dates = df[df['publishDate'].isna()]
print(invalid_dates[['title', 'publishDate']].head(20))  # Вывод первых 20 строк с некорректными датами
#
df = df.dropna(subset=['publishDate'])
df['publishDate'] = pd.to_datetime(df['publishDate'], format='%Y-%m-%d', errors='coerce')
# Извлечение года из даты
df['publishYear'] = df['publishDate'].dt.year

min_date = df['publishDate'].min()
max_date = df['publishDate'].max()

print(f"Минимальная дата: {min_date}")
print(f"Максимальная дата: {max_date}")
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['publishYear'])
plt.title('Боксплот для годов публикации')
plt.xlabel('Год публикации')
plt.show()


# Построение графика количества книг по годам
valid_years = df[(df['publishYear'] >= 1950) & (df['publishYear'] <= 2024)]

books_per_year = valid_years['publishYear'].value_counts().sort_index()

# Поиск локальных максимумов (пиков) и минимумов
years = books_per_year.index
counts = books_per_year.values

# Находим пики
peaks, _ = find_peaks(counts)
# Находим минимумы (между пиками)
valleys, _ = find_peaks(-counts)

plt.figure(figsize=(12, 6))
sns.lineplot(x=years, y=counts)
plt.title('Количество опубликованных книг по годам')
plt.xlabel('Год')
plt.ylabel('Количество книг')
plt.xlim(1950, 2024)  # Ограничиваем ось X

# Добавляем вертикальные линии для пиков
for peak in peaks:
    plt.axvline(x=years[peak], color='red', linestyle='--', lw=1)
    plt.text(years[peak], counts[peak] * 0.9, str(years[peak]), color='black', ha='center')

# Добавляем вертикальные линии для минимумов
for valley in valleys:
    plt.axvline(x=years[valley], color='blue', linestyle='--', lw=1)
    plt.text(years[valley], counts[valley] * 0.9, str(years[valley]), color='black', ha='center')

plt.show()