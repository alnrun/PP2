import psycopg2

def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook",
        user="postgres",
        password="1234"  # поставь свой пароль
    )