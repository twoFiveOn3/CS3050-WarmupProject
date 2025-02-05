from enum import Enum
import firebase_admin
import json
import os

from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

from car import Car


#NOTE: eventually removed when we call auth() in parser 
from auth import auth
auth()





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


# TODO: maybe add redundancy in the parser so users can search for fields in multiple ways
#  ie: 'horse power' or 'horse power'
def make_query(params: list):

    db = firestore.client()
    #TODO: help command 
    if len(params) < 1:
        raise InterfaceError
    if len(params) == 1:  # non compound query

        field = params[0][0]  # ex: will be one of the enumerated types specified above
        operator = params[0][1]  # ex: ==
        request = params[0][2]  # ex: 'Honda'

        #NOTE: depending on what parsed params are, don't need this 
        # if field == something like "CAR_NAME" we would use these ifs to change "CAR_NAME" to "name" (matches the field in the database)
        if field == QueryVal.MAKE.value:
            # do query
           pass
        if field == QueryVal.MODEL.value:
            # ...
            pass
        if field == QueryVal.ALL_WHEEL.value:
            #...
            pass
        if field == QueryVal.MSRP.value:
            # ...
            pass
        if field == QueryVal.DEALER_COST.value:
            # ...
            pass
        if field == QueryVal.HORSEPOWER.value:
            # ...
            pass
        #NOTE: this should work for all len(params[1]) == 1
        #TODO: make function params = field,operator,request 
        doc_ref = db.collection("cars").where(filter=FieldFilter(field, operator, request)).stream()
        cars: list[Car] = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
        Car.print_cars(cars)
        return cars 


        

    if len(params) == 2:  # compound query
        # TODO: make all cases for compound queries
        field_1 = params[0][0]
        field_2 = params[1][0]

        operator_1 = params[0][1]
        operator_2 = params[1][1]

        request_1 = params[0][2]
        request_2 = params[1][2]

        # do the same for 2 params

        #NOTE: for 2 queries, can do AND and OR 

        #AND
        doc_ref = db.collection("cars").where(filter=FieldFilter(field_1, operator_1, request_1)).where(
            filter=FieldFilter(field_2, operator_2, request_2)
            ).stream()
        cars: list[Car] = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
        Car.print_cars(cars)
        return cars 

    if len(params) > 2:
        raise InterfaceError
        

# in the while loop polling for query requests, before doing the query we must check is the user entered 'help' or 'quit'

#for testing 
#make_query([["name", "==", "Mini Cooper"]])
#make_query([["msrp", ">", 30000]])
make_query([["msrp", ">", 30000], ["horsepower", ">", 300]])


    