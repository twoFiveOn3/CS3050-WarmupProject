from enum import Enum
import firebase_admin
import json
import os

from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

from car import Car


# NOTE: eventually removed when we call auth() in parser
from auth import auth
auth()


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

    db = firestore.client()
    #TODO: help command 
    if len(params) < 1:
        raise InterfaceError

    # non compound query
    if len(params) == 1:
        field = params[0][0]  # ex: will be one of the enumerated types specified above
        operator = params[0][1]  # ex: ==
        request = params[0][2]  # ex: 'Honda'

        # formatting field to be correct to make query, operator and request are fir right now
        field = set_field(field)

        # NOTE: this should work for all len(params[1]) == 1
        doc_ref = db.collection("cars").where(filter=FieldFilter(field, operator, request)).stream()
        cars: list[Car] = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
        Car.print_cars(cars)
        return cars

    # compound query
    if len(params) == 2:
        field_1 = params[0][0]
        field_2 = params[1][0]

        operator_1 = params[0][1]
        operator_2 = params[1][1]

        request_1 = params[0][2]
        request_2 = params[1][2]

        # do the same for 2 params
        field_1 = set_field(field_1)
        field_2 = set_field(field_2)

        #AND
        doc_ref = db.collection("cars").where(filter=FieldFilter(field_1, operator_1, request_1)).where(
            filter=FieldFilter(field_2, operator_2, request_2)
            ).stream()
        cars: list[Car] = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
        Car.print_cars(cars)
        return cars 

    if len(params) > 2:
        raise InterfaceError
        

#for testing 
#make_query([["name", "==", "Mini Cooper"]])
#make_query([["msrp", ">", 30000]])
make_query([["msrp", ">", 30000], ["horsepower", ">", 300]])


    