import pandas as pd

# Путь к вашему CSV-файлу
csv_file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data_with_gender_and_genres.csv'

# Чтение данных из CSV
df = pd.read_csv(csv_file_path)

# Сохранение данных в формате Excel
excel_file_path = 'C:/Users/inger/PycharmProjects/pythonProject1/data/final_books_data_with_gender_and_genres.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Файл успешно сохранен в формате Excel: {excel_file_path}")
