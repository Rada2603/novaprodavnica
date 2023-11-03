import mysql.connector
from mysql.connector import Error

db_config = {
    "host": "35.239.158.202",
    "user": "root",
    "password": "7$x[;*X-0qpT[J2n",
    "database": "test",
}

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Uspješno povezan na bazu podataka")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test.store limit 2")
    results = cursor.fetchall()
    for row in results:
        print(row)


except Error as e:
    print("Greška prilikom povezivanja na bazu podataka:", e)


finally:
    # Zatvori vezu
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Veza zatvorena")
