import hashlib
import json
import os
from utils import (
    create_conection,
    load_queries,
    close_conection,
)


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()[:10]
    return hashed_password


def deidentify_passwords_and_save_to_json():
    connection, cursor = create_conection()
    file_path = os.environ.get("path_to_json")
    sql_queries = load_queries(file_path)

    cursor.execute(sql_queries["select_saler_passwords"])
    results = cursor.fetchall()

    deidentified_passwords = {}
    for result in results:
        original_password = result[0]
        if original_password not in deidentified_passwords:
            deidentified_password = hash_password(original_password)
            deidentified_passwords[original_password] = deidentified_password
            cursor.execute(
                sql_queries["select_hash"], (deidentified_password, original_password)
            )
        else:
            continue

    with open("deidentified_passwords.json", "w") as json_file:
        json.dump(deidentified_passwords, json_file, indent=3)

    connection.commit()
    close_conection(connection, cursor)
