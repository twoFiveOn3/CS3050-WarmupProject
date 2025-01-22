import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})