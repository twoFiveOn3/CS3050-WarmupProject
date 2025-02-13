import json
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def auth():
    cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
    #cred = credentials.Certificate(f"{sys.path[-1]}/firebase_secrets.json")
    firebase_admin.initialize_app(cred)