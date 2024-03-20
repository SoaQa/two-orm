from django.db import connection as engine


def hello_world():
    with engine.cursor() as cursor:
        cursor.execute("SELECT 'HELLO WORLD!'")
        row = cursor.fetchall()

        print(row)

if __name__ == '__main__':
    hello_world()
