from pydantic import BaseModel


class Product(BaseModel):
    id: int
    naziv: str
    cena: int
    kolicina: int
    product_id: int


class Buyer(BaseModel):
    kupac_id: int
    ime_kupca: str
    Prezime_kupca: str
    username: str
    password: str
