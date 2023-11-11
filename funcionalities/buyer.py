from utils import close_conection, create_conection, read_csv_file
import os


def view_cart_buyer():
    connection, cursor = create_conection()
    file_path, login_buyer_df = read_csv_file(os.environ.get("login_buyer_path"))
    if login_buyer_df.empty:
        return {"message": "You must log in"}
    else:
        kupac_id = int(login_buyer_df["kupac_id"].values[0])

    print(kupac_id)
    cursor.execute("SELECT *  FROM test.korpa WHERE moj_id = %s", (kupac_id,))
    cart_buyer = cursor.fetchall()
    close_conection(connection, cursor)
    formatted_results = [
        {
            "korpa_id": row[0],
            "kolicina": row[1],
            "product_id": row[2],
            "moj_id": row[3],
        }
        for row in cart_buyer
    ]

    return formatted_results
