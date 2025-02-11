import json
import os
import sys
import firebase_admin

from auth import auth
from firebase_admin import firestore
from parser import parse
from query import make_query


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

    usr_query = ''
    print_help_menu()
    # begin while loop polling for using input
    while usr_query.lower() != 'quit':
        usr_query = input('> ')
        if usr_query.lower() == 'help':
            print_help_menu()
        if usr_query.lower() == 'quit':
            exit()
        # otherwise call parse
        query_elems = parse(usr_query)
        make_query(query_elems)
        # print return data
        usr_query = input('> ')


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

def print_help_menu():
    print("Query should be in the form: <field> <operator> <delimiter>\n"
          "The language supports the following operators: \n == \n >= \n <= \n < \n > \n "
          "The language supports the following fields: \n Make \n Model \n Price \n MSRP \n Horsepower \n AWD (boolean)"
          "To make a compound query, do so in the form: <field 1> <operator 1> <delimiter 1> 'and' <field 2> <operator 2> <delimiter 2 \n"
          "To search for a field longer than one word, wrap the field with double quotes \n"
          "For help: type 'help' to see this menu again \n"
          "To exit: type 'quit' ")


main()

