import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy.signal import find_peaks

# Загружаем данные
cleaned_data_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data.csv'
df = pd.read_csv(cleaned_data_path)

# Устанавливаем отображение всех колонок и ширины
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Описание данных
print(df.describe())

# Гистограмма распределения рейтингов
plt.figure()
sns.histplot(df['rating'], bins=50, color='skyblue', edgecolor='black')
plt.title('Distribution of Book Ratings')
plt.xlabel('Rating')
plt.ylabel('Number of Books')
plt.show(block=False)

# Круговая диаграмма ценовых категорий
plt.figure()
price_bins = [0, 5, 10, 20, 50, 100, np.inf]
price_labels = ['<5', '5-10', '10-20', '20-50', '50-100', '100+']
df['price_category'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)
price_counts = df['price_category'].value_counts()
plt.pie(price_counts, labels=price_labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Book Price Categories')
plt.show(block=False)

# Разделение и подсчет жанров
genres_list = df['genres'].apply(lambda x: x.strip("[]").replace("'", "").split(', '))
all_genres = [genre for sublist in genres_list for genre in sublist if genre]

# Счетчик частот жанров
genre_counts = Counter(all_genres)
genre_counts_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count'])
genre_counts_df = genre_counts_df.sort_values(by='Count', ascending=False)

# График топ-10 жанров
plt.figure()
sns.barplot(x='Genre', y='Count', data=genre_counts_df.head(10), hue='Genre', palette='Blues_d')
plt.title('Top-10 Popular Genres')
plt.xlabel('Genre')
plt.ylabel('Number of Books')
plt.xticks(rotation=45, ha='right')
plt.show(block=False)

# Корреляционная матрица
plt.figure()
numeric_cols = ['rating', 'numRatings', 'pages', 'price', 'likedPercent', 'bbeScore', 'bbeVotes']
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show(block=False)

# Боксплот для цены
plt.figure()
sns.boxplot(y=df['price'])#, palette='Set3')
plt.title('Book Price Boxplot')
plt.ylabel('Price')
plt.show(block=False)

# Боксплот для количества страниц
plt.figure()
sns.boxplot(y=df['pages'])#, palette='Set3')
plt.title('Book Pages Boxplot')
plt.ylabel('Number of Pages')
plt.show(block=False)

# Зависимость рейтинга от цены
plt.figure()
sns.scatterplot(x=df['rating'], y=df['price'], alpha=0.5)
plt.title('Rating vs. Price')
plt.xlabel('Rating')
plt.ylabel('Price')
plt.show(block=False)

# Зависимость рейтинга от количества страниц
plt.figure()
sns.scatterplot(x=df['rating'], y=df['pages'], alpha=0.5)
plt.title('Rating vs. Number of Pages')
plt.xlabel('Rating')
plt.ylabel('Number of Pages')
plt.show(block=False)

# Преобразование столбца 'publishDate' в datetime
df['publishDate'] = pd.to_datetime(df['publishDate'], errors='coerce')
df['publishYear'] = df['publishDate'].dt.year

# Проверка некорректных дат
invalid_dates = df[df['publishDate'].isna()]
print(f"Number of Invalid Dates: {len(invalid_dates)}")

# Удаление строк с некорректными датами
df = df.dropna(subset=['publishDate'])

# График боксплота для годов публикации
plt.figure()
sns.boxplot(x=df['publishYear'])#, palette='Set3')
plt.title('Publication Year Boxplot')
plt.xlabel('Publication Year')
plt.show(block=False)

# График количества книг по годам
valid_years = df[(df['publishYear'] >= 1950) & (df['publishYear'] <= 2024)]
books_per_year = valid_years['publishYear'].value_counts().sort_index()

# Поиск пиков и впадин
years = books_per_year.index
counts = books_per_year.values
peaks, _ = find_peaks(counts)
valleys, _ = find_peaks(-counts)

plt.figure(figsize=(12, 6))
sns.lineplot(x=years, y=counts, marker='o')
plt.title('Number of Books Published per Year')
plt.xlabel('Year')
plt.ylabel('Number of Books')
plt.xlim(1950, 2024)

# Добавление аннотаций для пиков
for peak in peaks:
    if years[peak] > 2000:  # Оставляем только годы после 2000
        plt.axvline(x=years[peak], color='red', linestyle='--', lw=1)
        plt.text(years[peak], counts[peak] * 0.9, str(int(years[peak])), color='black', ha='center')

# Добавление аннотаций для впадин
for valley in valleys:
    if years[valley] > 2000:  # Оставляем только годы после 2000
        plt.axvline(x=years[valley], color='blue', linestyle='--', lw=1)
        plt.text(years[valley], counts[valley] * 0.9, str(int(years[valley])), color='black', ha='center')

plt.show()
