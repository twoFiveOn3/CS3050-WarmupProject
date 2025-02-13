import json
import os
import sys
import firebase_admin

from auth import auth
from firebase_admin import firestore
from parser import parse
from query_test import make_query
from car import Car


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

if __name__ == "__main__":
    # check the user inputted a json filename
    if len(sys.argv) < 2: #argv always has length >= 1 because argv[0] is the program name
        print("Usage: admin.py <json-filename>")
        return
    
    json_filename = sys.argv[1]

    # check if json file exists before deleting
    if not os.path.exists(f"{json_filename}"):
        print(f"file {json_filename} does not exist")
        return
    
    # authenticate firebase connection
    auth()

    # delete existing data
    drop_collection()
    # write new data from inputted json filename
    create_docs(json_filename)
    
