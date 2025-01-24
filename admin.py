import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref.set({"cars": cars}

