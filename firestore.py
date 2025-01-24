import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
import json 

cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
app = firebase_admin.initialize_app(cred)

with open('Cars.csv')
db = firestore.client()

doc_ref = db.collection("users").document("car_data")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})


