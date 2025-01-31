from enum import Enum
import firebase_admin
import json
import os
from firebase_admin import credentials
from firebase_admin import firestore


class QueryVal(Enum):
    MAKE = 0
    MODEL = 1
    ALL_WHEEL = 2
    MSRP = 3
    DEALER_COST = 4
    HORSEPOWER = 5


# base exception class for the interface
class InterfaceError(Exception):
    pass

cred = credentials.Certificate(f"{os.getcwd()}/firebase_secrets.json")
app = firebase_admin.initialize_app(cred)

data = []

with open('cars.json') as file:
    data = json.load(file)
    for car in data:
        print(car)


print(type(data))

db = firestore.client()
print(data)

doc_ref = db.collection("Warm Up Project - Cars").document("Car")
batch = db.batch()

for car in data: 
    doc_ref = db.collection("cars").document()
    batch.set(doc_ref, car)

batch.commit()
# TODO: maybe add redundancy in the parser so users can search for fields in multiple ways
#  ie: 'horse power' or 'horse power'
def make_query(params: list):
    if len(params) < 1:
        raise InterfaceError
    if len(params) == 1:  # non compound query

        field = params[0][0]  # ex: will be one of the enumerated types specified above
        operator = params[0][1]  # ex: ==
        request = params[0][2]  # ex: 'Honda'
        if field == QueryVal.MAKE.value:
            # do query
        if field == QueryVal.MODEL.value:
            # ...
        if field == QueryVal.ALL_WHEEL.value:
            #...
        if field == QueryVal.MSRP.value:
            # ...
        if field == QueryVal.DEALER_COST.value:
            # ...
        if field == QueryVal.HORSEPOWER.value:
            # ...

    if len(params) == 2:  # compound query
        # TODO: make all cases for compound queries
        field_1 = params[0][0]
        field_2 = params[1][0]

        operator_1 = params[0][1]
        operator_2 = params[1][1]

        request_1 = params[0][2]
        request_2 = params[1][2]

        # do the same for 2 params


    if len(params) == 2:
        raise InterfaceError

# in the while loop polling for query requests, before doing the query we must check is the user entered 'help' or 'quit'
