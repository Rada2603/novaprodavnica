import pandas as pd
from utils import get_database_connection
from models.classes import Buyer, Sales


def create_conection():
    connection = get_database_connection()
    cursor = connection.cursor()
    return connection, cursor


def close_conection(connection, cursor):
    cursor.close()
    connection.close()


def read():
    login_buyer_1 = r"data\ulogovani_kupci.csv"
    login_buyer_df = pd.read_csv(login_buyer_1)
    return login_buyer_1, login_buyer_df


def read_prodavac():
    login_sales_1 = r"data\ulogovani_prodavci.csv"
    login_sales_df = pd.read_csv(login_sales_1)
    return login_sales_1, login_sales_df


def create_params(kupac: Buyer):
    params = (
        kupac.kupac_id,
        kupac.ime_kupca,
        kupac.prezime_kupca,
        kupac.username,
        kupac.password,
    )
    return params


def create_kupca(kupac: Buyer):
    kupac = {
        "kupac_id": kupac.kupac_id,
        "ime_kupca": kupac.ime_kupca,
        "prezime_kupca": kupac.prezime_kupca,
        "username": kupac.username,
        "password": kupac.password,
    }
    return kupac


def create_params_prodavac(prodavac: Sales):
    params_prodavac = (
        prodavac.id,
        prodavac.ime,
        prodavac.prezime,
        prodavac.username,
        prodavac.lozinka,
        prodavac.number,
    )
    return params_prodavac


def create_prodavac(prodavac: Sales):
    prodavac = {
        "prodavac_id": prodavac.id,
        "name": prodavac.ime,
        "surname": prodavac.prezime,
        "username": prodavac.username,
        "lozinka": prodavac.lozinka,
        "number_id": prodavac.number,
    }
    return prodavac
