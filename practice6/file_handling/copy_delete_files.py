import shutil
import os

# Копируем файл
shutil.copy("example.txt", "example_backup.txt")
print("Резервная копия создана.")

# Удаляем оригинал (если нужно по заданию)
# os.remove("example.txt")