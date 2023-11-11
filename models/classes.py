from pydantic import BaseModel


class BaseClass(BaseModel):
    id: int
    name: str


class Users(BaseClass):
    surname: str
    username: str
    password: str


class Sales(Users):
    number: int


class Product(BaseClass):
    price: int
    quantity: int
