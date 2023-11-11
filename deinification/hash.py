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

    with open(r"deidentified_passwords.json") as f:
        file = json.load(f)
    for result in results:
        original_password = result[0]
        print(original_password)
        if original_password not in file.values():
            print(file.values())
            deidentified_password = hash_password(original_password)
            file[original_password] = deidentified_password
            with open("deidentified_passwords.json", "w") as f:
                json.dump(file, f, indent=3)
            cursor.execute(
                sql_queries["select_hash"],
                (deidentified_password, original_password),
            )
        else:
            continue

    connection.commit()
    close_conection(connection, cursor)
