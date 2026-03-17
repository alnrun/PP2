import os
import shutil

# Переносим бэкап в созданную папку
if os.path.exists("example_backup.txt"):
    shutil.move("example_backup.txt", "test_folder/example_backup.txt")
    print("Файл перемещен в test_folder.")