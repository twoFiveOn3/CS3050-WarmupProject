import json
import os
import sys
import firebase_admin

from auth import auth
from firebase_admin import firestore

def main():
    auth()

    # check if input
    if len(sys.argv) < 2: #argv always has length >= 1 because argv[0] is the program name
        print("Usage: admin.py <json-filename>")
        return
    
    user_input = sys.argv[1]

    # check if json file exists before deleting
    if not os.path.exists(f"{user_input}"):
        print(f"file {user_input} does not exist")
        return

    drop_collection()
    create_docs(user_input)


def create_docs(json_file: str):
    data = []
    db = firestore.client()
    batch = db.batch()

    with open(f"{json_file}") as file:
        data = json.load(file)

    for car in data:
        doc_ref = db.collection("cars").document()
        print(f"commited {car['name']} to be created")
        batch.set(doc_ref, car)

    batch.commit()


def drop_collection():
    db = firestore.client()
    docs = db.collection("cars").stream()
    batch = db.batch()

    for doc in docs:
        print(f"deleting {doc.id}")
        batch.delete(doc.reference)

    batch.commit()


main()

