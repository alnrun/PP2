names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# zip: объединяем два списка
combined = list(zip(names, scores))

# enumerate: получаем индекс и значение
print("Результаты теста:")
for index, (name, score) in enumerate(combined, start=1):
    print(f"{index}. {name} набрал {score} баллов")