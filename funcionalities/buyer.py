from models.classes import Buyer
from utils import get_database_connection
from fastapi import HTTPException
import json

with open(r"data\upiti.json") as f:
    file = json.load(f)


def view_cart_buyer(kupac: Buyer):
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
    cursor.execute("SELECT *  FROM test.korpa WHERE moj_id = %s", (kupac.kupac_id,))
    cart_buyer = cursor.fetchall()
    cursor.close()
    connection.close()
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
