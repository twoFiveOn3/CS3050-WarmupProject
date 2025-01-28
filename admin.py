import firebase_admin
import json
import os
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
app = firebase_admin.initialize_app(cred)

cars = {}

with open('cars.json') as file:
    data = json.load(file)
    for car in data:


print(type(data))

db = firestore.client()

doc_ref = db.collection("Warm Up Project - Cars").document("Car")
doc_ref.set(data)