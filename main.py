from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Any, Union
from dotenv import load_dotenv
from models.classes import Product
from funcionalities.store import view_store
from funcionalities.cart import view_cart, add_cart_buyer
from models.classes import Users, Sales
from funcionalities.buyer import view_cart_buyer
from funcionalities.login import check_out_user, login_user

app = FastAPI()
load_dotenv()


@app.post("/login/{user_type}")
def login_user_route(user_type, user: dict):
    return login_user(user_type, user)


@app.get("/check/{user_type}")
def check_out_user_route(user_type: str):
    return check_out_user(user_type)


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
