from models.function import create_conection, close_conection
import json

with open(r"data\upiti.json", "r") as f:
    file = json.load(f)


def view_store():
    connection, cursor = create_conection()
    cursor.execute(file["select_store"])
    results = cursor.fetchall()
    close_conection(connection, cursor)
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
