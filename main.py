import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

db_config = {
    "host": "35.239.158.202",
    "user": "root",
    "password": "7$x[;*X-0qpT[J2n",
    "database": "test",
}

connection = mysql.connector.connect(**db_config)


class StoreItem(BaseModel):
    naziv: str
    cena: int
    kolicina: int


@app.get("/store")
def view_store():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test.store")
    results = cursor.fetchall()
    cursor.close()
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
