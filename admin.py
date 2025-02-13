import json
import os
import sys
import firebase_admin

from auth import auth
from firebase_admin import firestore


from auth import auth


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

    print("Creating documents...")
    for car in data:
        doc_ref = db.collection("cars").document()
        batch.set(doc_ref, car)

    batch.commit()


def drop_collection():
    db = firestore.client()
    docs = db.collection("cars").stream()
    batch = db.batch()

   
    print("Dropping collection...")
    for doc in docs:
        batch.delete(doc.reference)

    batch.commit()

main()

