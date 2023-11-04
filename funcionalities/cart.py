from utils import get_database_connection
import json

with open(r"data\upiti.json") as f:
    cart = json.load(f)


def view_cart():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(cart["select_cart"])
    results = cursor.fetchall()
    cursor.close()
    connection.close
    formatted_results = [
        {
            "store_id": row[0],
            "product_name": row[1],
            "product_price": row[2],
            "product_quantity": row[3],
        }
        for row in results
    ]

    return formatted_results
