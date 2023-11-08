from models.function import close_conection, create_conection, read
import json
from models.classes import Product, Buyer
from fastapi import HTTPException
import pandas as pd

with open(r"data\upiti.json") as f:
    file = json.load(f)


def view_cart():
    connection, cursor = create_conection()
    cursor.execute(file["select_cart"])
    results = cursor.fetchall()
    close_conection(connection, cursor)
    formatted_results = [
        {
            "korpa_id": row[0],
            "kolicina": row[1],
            "product_id": row[2],
            "moj id": row[3],
        }
        for row in results
    ]

    return formatted_results


def add_cart_buyer(product: Product):
    connection, cursor = create_conection()
    login_buyer_1, login_buyer_df = read()

    # proverava da li je kupac ulogovan
    if login_buyer_df.empty:
        return {"message": "You must log in"}
    else:
        kupac_id = int(login_buyer_df["kupac_id"].values[0])

    # proveravam da li proizvod postoji u prodavnici i da li ima dovolno kolicine
    cursor.execute(file["select_store"])
    results = cursor.fetchall()
    for row in results:
        if (
            product.id == row[0]
            and product.naziv == row[1]
            and product.kolicina <= row[3]
        ):
            break
    else:
        raise HTTPException(
            status_code=400, detail="Product not found in store or not enough quantity"
        )
    new_product_quantitiy = row[3] - product.kolicina
    cursor.execute(
        "UPDATE test.store SET product_quantity =%s WHERE store_id = %s",
        (new_product_quantitiy, row[0]),
    )
    # proveravam da li proizvod vec postoji u korpi
    cursor.execute(file["select_cart"])
    cart = cursor.fetchall()
    korpa_id = None
    for row in cart:
        if product.id == row[2] and kupac_id == row[3]:
            new_quantity = row[1] + product.kolicina
            cursor.execute(
                "UPDATE test.korpa SET kolicina = %s WHERE korpa_id = %s",
                (new_quantity, row[0]),
            )
            korpa_id = row[0]
            break
    else:
        cursor.execute("SELECT MAX(korpa_id) FROM test.korpa")
        max_korpa_id = cursor.fetchone()[0]
        if max_korpa_id is not None:
            korpa_id = max_korpa_id + 1
        else:
            korpa_id = 200

        cursor.execute(
            "INSERT INTO test.korpa (korpa_id, kolicina, product_id, moj_id) VALUES (%s, %s, %s, %s)",
            (korpa_id, product.kolicina, product.id, kupac_id),
        )
        korpa_id += 1
    connection.commit()
    close_conection(connection, cursor)

    return {"message": "Product append"}
