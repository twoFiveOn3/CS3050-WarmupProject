import firebase_admin
import json
import os
import sys
from firebase_admin import credentials
from firebase_admin import firestore

#set up connection to firebase
cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


def main():
    user_input = sys.argv[1]
    
    #check if input
    if len(sys.argv) == 0:
        print("Give json file name")
        return

    # check if json file exists before deleting
    if not os.path.exists(f"{user_input}"):
        print(f"file {user_input} does not exist")
        return

    drop_collection()
    create_docs(user_input)


def create_docs(json_file: str):
    data = []
    batch = db.batch()

    with open(f'{json_file}') as file:
        data = json.load(file)

    for car in data:
        doc_ref = db.collection("cars").document()
        print(f"commited {car['name']} to be created")
        batch.set(doc_ref, car)

    batch.commit()


def drop_collection():
    docs = db.collection("cars").stream()
    batch = db.batch()

    for doc in docs:
        print(f"deleting {doc.id}")
        batch.delete(doc.reference)

    batch.commit()


main()
