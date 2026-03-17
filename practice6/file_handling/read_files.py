
try:
    with open("example.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print("Содержимое файла:")
        print(content)
except FileNotFoundError:
    print("Сначала запусти write_files.py!")