from enum import Enum
import firebase_admin
import json
import os
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
app = firebase_admin.initialize_app(cred)

data = []

with open('cars.json') as file:
    data = json.load(file)
    for car in data:
        print(car)


print(type(data))

db = firestore.client()

batch = db.batch()
print(data)
for car in data: 
    doc_ref = db.collection("cars").document()
    batch.set(doc_ref, car)

batch.commit()