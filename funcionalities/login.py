from models.classes import Users, Sales
import os
from typing import Union, Any
from fastapi import HTTPException, Path
import pandas as pd
from utils import (
    create_conection,
    close_conection,
    read_csv_file,
    create_params_kupac,
    create_params_prodavac,
    load_queries,
    create_kupca,
    create_prodavac,
    load_user_data,
    check_user_existence,
)


def check_out_user(
    user_type: str = Path(..., title="The type of user (buyer or sales)")
):
    if user_type == "sales":
        login_path = os.environ.get("login_sales_path")
    elif user_type == "buyer":
        login_path = os.environ.get("login_buyer_path")
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")

    login_1, login_df = read_csv_file(login_path)
    if not login_df.empty:
        login_df = pd.DataFrame(columns=login_df.columns)
        login_df.to_csv(login_1, index=False)
        return {"message": "Check out"}
    else:
        return {"message": f"We are not logged in as {user_type}"}


def login_user(user_type: str, user: dict):
    username = user.get("username")
    if not check_user_existence(username, user_type):
        raise HTTPException(status_code=400, detail=f"{user_type} not found")
    login_user_1, login_user_df, sql_queries = load_user_data(user_type)
    connection, cursor = create_conection()
    if user_type == "sales":
        users = Sales(**user)
        user_data = create_prodavac(users)
        params = create_params_prodavac(users)
    elif user_type == "buyer":
        users = Users(**user)
        params = create_params_kupac(users)
        user_data = create_kupca(users)

    else:
        raise HTTPException(status_code=400, detail="Invalid user type")
    cursor.execute(sql_queries[f"select_{user_type.lower()}"], params)
    results = cursor.fetchall()
    if not results:
        raise HTTPException(status_code=400, detail=f"{user_type} not found")
    if not login_user_df.empty:
        return {"message": "try again later"}
    existing_user = login_user_df[login_user_df[f"{user_type}_id"] == users.id]
    if not existing_user.empty:
        return {"message": f"{user_type.capitalize()} already exists"}
    login_user_df = login_user_df._append(user_data, ignore_index=True)
    login_user_df.to_csv(login_user_1, index=False)
    close_conection(connection, cursor)
    return {"message": f"Welcome {user_type.capitalize()}"}
