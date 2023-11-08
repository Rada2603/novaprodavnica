from fastapi import FastAPI
import uvicorn
from funcionalities.store import view_store
from funcionalities.cart import view_cart, add_cart_buyer
from models.classes import Product, Buyer, Sales
from funcionalities.buyer import view_cart_buyer
from funcionalities.login import (
    login_buyer,
    check_out_buyer,
    login_prodavac,
    check_out_sales,
)

app = FastAPI()


@app.post("/login_buyer/")
def login_buyer_route(kupac: Buyer):
    return login_buyer(kupac)


@app.post("/login_seler/")
def login_prodavac_route(prodavac: Sales):
    return login_prodavac(prodavac)


@app.get("/check")
def check_out_buyer_route():
    return check_out_buyer()


@app.get("/check_sales")
def check_out_sales_route():
    return check_out_sales()


@app.get("/store")
def view_store_route():
    results = view_store()
    return {"store_data": results}


@app.get("/korpa")
def view_cart_route():
    results = view_cart()
    return {"cart_data": results}


@app.post("/add_cart")
def add_cart_buyer_route(product: Product):
    results = add_cart_buyer(product)
    return {"message": results}


@app.get("/view_buyer_cart")
def view_cart_buyer_route():
    result = view_cart_buyer()
    return {"korpa": result}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
