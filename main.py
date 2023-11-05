from fastapi import FastAPI
import uvicorn
from funcionalities.store import view_store
from funcionalities.cart import view_cart, add_cart
from models.classes import Product, Buyer

app = FastAPI()


@app.get("/store")
def view_store_route():
    results = view_store()
    return {"store_data": results}


@app.get("/korpa")
def view_cart_route():
    results = view_cart()
    return {"cart_data": results}


@app.post("/add_cart")
def add_cart_route(kupac: Buyer, product: Product):
    results = add_cart(kupac, product)
    return {"add_cart": results}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
