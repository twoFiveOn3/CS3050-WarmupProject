from enum import Enum
import firebase_admin
import json
import os

from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

from car import Car


def translate_fieldname(field):
	field = lower(field)
	if field == "awd":
		field = "all_wheel"
	elif field == "price"
		field = "dealer_cost"
	return field

def translate_op(op):
	if op == "is":
		op = "=="
	return op


class InterfaceError(Exception):
    pass


def make_query(params: list):
    doc_ref = None
    db = firestore.client()
    #TODO: help command 
    if len(params) < 1:
        raise InterfaceError

	doc_ref = db.collection("cars")
	for (field, op, value) in params:
        field = translate(field)
		op = translate_op(op)
		doc_ref = doc_ref.where(filter(FieldFilter(field, op, value)))

    cars = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
    
    if len(cars) == 0:
        print("No cars found")    
        return 

    Car.print_cars(cars)
        

#for testing 
#make_query([["name", "==", "Mini Cooper"]])
#make_query([["msrp", ">", 30000]])p
#make_query([["msrp", ">", 30000], ["horsepower", ">", 300]])


    
