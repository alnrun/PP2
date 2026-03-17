from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map: возводим всё в квадрат
squared = list(map(lambda x: x**2, numbers))

# filter: оставляем только четные
evens = list(filter(lambda x: x % 2 == 0, numbers))

# reduce: находим сумму всех чисел
total_sum = reduce(lambda x, y: x + y, numbers)

print(f"Квадраты: {squared}")
print(f"Четные: {evens}")
print(f"Сумма: {total_sum}")