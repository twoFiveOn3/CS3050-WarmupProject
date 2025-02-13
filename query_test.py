from enum import Enum
import firebase_admin
import json
import os

from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter
from car import Car


# NOTE: eventually removed when we call auth() in parser



class QueryVal(Enum):
    MAKE = 0
    MODEL = 1
    ALL_WHEEL = 2
    MSRP = 3
    DEALER_COST = 4
    HORSEPOWER = 5


class DBVal(Enum):
    MAKE = 'make'
    MODEL = 'model'
    ALL_WHEEL = 'all_wheel'
    MSRP = 'msrp'
    DEALER_COST = 'dealer_cost'
    HORSEPOWER = 'horsepower'


# base exception class for the interface
class InterfaceError(Exception):
    pass


def set_field(field):
    if field == QueryVal.MAKE.value:
        field = DBVal.MAKE.value
    if field == QueryVal.MODEL.value:
        field = DBVal.MODEL.value
    if field == QueryVal.ALL_WHEEL.value:
        field = DBVal.ALL_WHEEL.value
    if field == QueryVal.MSRP.value:
        field = DBVal.MSRP.value
    if field == QueryVal.DEALER_COST.value:
        field = DBVal.DEALER_COST.value
    if field == QueryVal.HORSEPOWER.value:
        field = DBVal.HORSEPOWER.value
    return field


def make_query(params: list):
    #doc_ref = None
    #doc_ref = []
    db = firestore.client()
    print("Given string: ", params)
    #nest params further
    #TODO: help command 
    if len(params) < 1:
        raise InterfaceError

    print("PARAMS", params)
    # non compound query
    if len(params) == 1:

        # print(params, "PARAMS IN IF")
        field = params[0][0]  # ex: will be one of the enumerated types specified above
        operator = params[0][1]  # ex: ==
        request = params[0][2]  # ex: 'Honda'
        #
        # print(field, operator, request, "FIELD, OPERATOR, REQUEST")
        # formatting field to be correct to make query, operator and request are fir right now



        # NOTE: this should work for all len(params[1]) == 1
        doc_ref = db.collection("cars").where(filter=FieldFilter(field, operator, request)).stream()
        # doc_ref = db.collection("cars").where(filter=FieldFilter(params[0], params[1], params[2])).stream()
       
       
    # compound query
    if len(params) == 2:
        field_1 = params[0][0]
        field_2 = params[1][0]

        operator_1 = params[0][1]
        operator_2 = params[1][1]

        request_1 = params[0][2]
        request_2 = params[1][2]

        # do the same for 2 params
        

        #AND
        doc_ref = db.collection("cars").where(filter=FieldFilter(field_1, operator_1, request_1)).where(
            filter=FieldFilter(field_2, operator_2, request_2)
            ).stream()
        
    cars = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
    # cars = []
    # for car in doc_ref:
    #     newCar = car.to_dict()
    #     cars.append(Car(**newCar))

    #print("THIS IS CARS", cars)
    if len(cars) == 0:
        print("No cars found")    
        #return

    if len(params) > 2:
        raise InterfaceError
    
    Car.print_cars(cars)
        

#for testing 
#make_query([["", "==", "Mini Cooper"]])
#make_query([["msrp", ">", 30000]])
#make_query([["msrp", ">", 50000], ["horsepower", ">", 300]])


    