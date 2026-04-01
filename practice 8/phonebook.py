from connect import connect


# 🔹 Добавить или обновить контакт
def upsert(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


# 🔹 Поиск по шаблону
def search(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# 🔹 Пагинация
def pagination(limit, offset):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# 🔹 Массовая вставка
def insert_many():
    conn = connect()
    cur = conn.cursor()

    names = ["Ali", "Bob", "John"]
    phones = ["87771234567", "123", "87005554433"]

    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))

    conn.commit()
    cur.close()
    conn.close()


# 🔹 Удаление
def delete(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()


# 🔥 тест
if __name__ == "__main__":
    upsert("Ali", "87770000000")
    search("Ali")
    pagination(5, 0)
    insert_many()
    delete("Ali")