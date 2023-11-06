from utils import get_database_connection
import json
from models.classes import Product, Buyer
from fastapi import HTTPException

with open(r"data\upiti.json") as f:
    file = json.load(f)


def view_cart():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(file["select_cart"])
    results = cursor.fetchall()
    cursor.close()
    connection.close()
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


def add_cart(kupac: Buyer, product: Product):
    connection = get_database_connection()
    cursor = connection.cursor()
    params = (
        kupac.kupac_id,
        kupac.ime_kupca,
        kupac.Prezime_kupca,
        kupac.username,
        kupac.password,
    )
    # proveravam da li je kupac registrovan
    cursor.execute(file["select_kupci"], params)
    res = cursor.fetchall()
    if not res:
        raise HTTPException(status_code=400, detail="buyer not found")

    # proveravam da li proizvod postoji u prodavnici i da li ima dovolno kolicine
    cursor.execute(file["select_store"])
    result = cursor.fetchall()
    for row in result:
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
        if product.id == row[2] and kupac.kupac_id == row[3]:
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
            (korpa_id, product.kolicina, product.id, kupac.kupac_id),
        )
        korpa_id += 1
    connection.commit()
    cursor.execute(file["select_cart"])
    cart = cursor.fetchall()  # Potvrdite promene
    cursor.close()
    connection.close()
    print("2222")
    formatted_results = [
        {
            "korpa_id": row[0],
            "kolicina": row[1],
            "product_id": row[2],
            "moj_id": row[3],
        }
        for row in cart
    ]

    return formatted_results
