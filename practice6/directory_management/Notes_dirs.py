import os

# Создаем вложенные папки
os.makedirs("test_folder/sub_folder", exist_ok=True)

# Список всех файлов и папок в текущей директории
print("Список объектов:", os.listdir("."))