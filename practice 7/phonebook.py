import csv
from connect import connect

# Создание таблицы
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


# Вставка из CSV
def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV данные добавлены")


# Вставка с консоли
def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен")


# Обновление
def update_contact():
    name = input("Введите имя для обновления: ")
    new_phone = input("Введите новый телефон: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Контакт обновлен")


# Поиск с фильтром
def query_contacts():
    print("1 - Показать все")
    print("2 - По имени")
    print("3 - По номеру (начало)")
    choice = input("Выбор: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        name = input("Введите имя: ")
        cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    elif choice == "3":
        prefix = input("Введите начало номера: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + "%",))

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# Удаление
def delete_contact():
    print("Удалить по:")
    print("1 - Имени")
    print("2 - Номеру")
    choice = input("Выбор: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Введите имя: ")
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif choice == "2":
        phone = input("Введите номер: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))

    conn.commit()
    cur.close()
    conn.close()
    print("Контакт удален")


# Меню
def menu():
    create_table()

    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Импорт из CSV")
        print("2. Добавить контакт")
        print("3. Обновить контакт")
        print("4. Показать контакты")
        print("5. Удалить контакт")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Ошибка выбора")


if __name__ == "__main__":
    menu()