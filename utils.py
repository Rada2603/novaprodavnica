import mysql.connector
import os
import json
from models.classes import Users, Sales
import pandas as pd
from fastapi import HTTPException


def get_database_connection():
    db_config = {
        "host": os.environ.get("HOST"),
        "user": os.environ.get("USER"),
        "password": os.environ.get("PASSWORD"),
        "database": os.environ.get("DATABASE"),
    }
    connection = mysql.connector.connect(**db_config)
    return connection


def check_user_existence(username, user_type: str):
    connection, cursor = create_conection()
    file_path = os.environ.get("path_to_json")
    sql_queries = load_queries(file_path)
    if user_type.lower() == "buyer":
        cursor.execute(sql_queries["select_buyer_username"], (username,))
    elif user_type.lower() == "sales":
        cursor.execute(sql_queries["select_saler_username"], (username,))
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")

    result = cursor.fetchone()
    close_conection(connection, cursor)

    return result is not None


def load_user_data(user_type: str):
    if user_type == "sales":
        login_user_1, login_user_df = read_csv_file(os.environ.get("login_sales_path"))

    elif user_type == "buyer":
        login_user_1, login_user_df = read_csv_file(os.environ.get("login_buyer_path"))
    else:
        raise HTTPException(status_code=400, detail="Invalid user role")
    file_path = os.environ.get("path_to_json")
    sql_queries = load_queries(file_path)
    return login_user_1, login_user_df, sql_queries


def create_conection():
    connection = get_database_connection()
    cursor = connection.cursor()
    return connection, cursor


def close_conection(connection, cursor):
    cursor.close()
    connection.close()


def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return file_path, df


def load_queries(file_path):
    with open(file_path) as f:
        return json.load(f)


def create_params_kupac(kupac: Users):
    params = (
        kupac.id,
        kupac.name,
        kupac.surname,
        kupac.username,
        kupac.password,
    )
    return params


def create_kupca(kupac: Users):
    kupac = {
        "buyer_id": kupac.id,
        "ime_kupca": kupac.name,
        "prezime_kupca": kupac.surname,
        "username": kupac.username,
        "password": kupac.password,
    }
    return kupac


def create_params_prodavac(prodavac: Sales):
    params_prodavac = (
        prodavac.id,
        prodavac.name,
        prodavac.surname,
        prodavac.username,
        prodavac.password,
        prodavac.number,
    )
    return params_prodavac


def create_prodavac(prodavac: Sales):
    prodavac = {
        "sales_id": prodavac.id,
        "name": prodavac.name,
        "surname": prodavac.surname,
        "username": prodavac.username,
        "lozinka": prodavac.password,
        "number_id": prodavac.number,
    }
    return prodavac
