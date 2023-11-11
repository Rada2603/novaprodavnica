from utils import create_conection, close_conection, load_queries
import os


def view_store():
    file_path = os.environ.get("path_to_json")
    sql_queries = load_queries(file_path)
    connection, cursor = create_conection()
    cursor.execute(sql_queries["select_store"])
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
