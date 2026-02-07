car = {
    "brand": "Toyota",
    "year": 2020
}
print(car)


print(car["brand"])


car["year"] = 2023
print(car)



car["color"] = "white"
print(car)



print(car.keys())
print(car.values())



for key in car:
    print(key)

for value in car.values():
    print(value)
