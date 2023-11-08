from models.classes import Buyer, Sales
import json
from fastapi import HTTPException
import pandas as pd
from models.function import (
    create_conection,
    close_conection,
    read,
    create_params,
    create_kupca,
    read_prodavac,
    create_params_prodavac,
    create_prodavac,
)


with open(r"data\upiti.json") as f:
    file = json.load(f)


def login_buyer(kupac: Buyer):
    connection, cursor = create_conection()
    login_buyer_df, login_buyer_1 = read()
    params = create_params(kupac)
    cursor.execute(file["select_kupci"], params)
    results = cursor.fetchall()

    if not results:
        raise HTTPException(status_code=400, detail="buyer not found")

    if not login_buyer_df.empty:
        return {"message": "try again later"}

    existing_buyer = login_buyer_df[login_buyer_df["kupac_id"] == kupac.kupac_id]
    if not existing_buyer.empty:
        return {"message": "Buyer already exists"}

    kupac = create_kupca(kupac)
    login_buyer_df = login_buyer_df._append(kupac, ignore_index=True)
    login_buyer_df.to_csv(login_buyer_1, index=False)
    close_conection(connection, cursor)
    return {"message": "Welcome"}


def check_out_buyer():
    login_buyer_1, login_buyer_df = read()
    if not login_buyer_df.empty:
        login_buyer_df = pd.DataFrame(columns=login_buyer_df.columns)
        login_buyer_df.to_csv(login_buyer_1, index=False)
        return {"message": "Check out"}


def login_prodavac(prodavac: Sales):
    connection, cursor = create_conection()
    login_sales_1, login_sales_df = read_prodavac()
    params_prodavac = create_params_prodavac(prodavac)
    cursor.execute(file["select_prodavci"], params_prodavac)
    results = cursor.fetchall()

    if not results:
        raise HTTPException(status_code=400, detail="seler not found")

    if not login_sales_df.empty:
        return {"message": "try again later"}

    existing_sales = login_sales_df[login_sales_df["prodavac_id"] == prodavac.id]
    if not existing_sales.empty:
        return {"message": "Sales already exists"}

    prodavac_1 = create_prodavac(prodavac)
    login_sales_df = login_sales_df._append(prodavac_1, ignore_index=True)
    login_sales_df.to_csv(login_sales_1, index=False)
    close_conection(connection, cursor)
    return {"message": "Welcome"}


def check_out_sales():
    login_sales_1, login_sales_df = read_prodavac()
    if not login_sales_df.empty:
        login_sales_df = pd.DataFrame(columns=login_sales_df.columns)
        login_sales_df.to_csv(login_sales_1, index=False)
        return {"message": "Check out"}
