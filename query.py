from enum import Enum
import firebase_admin
import json
import os

from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

from car import Car


def translate_fieldname(field):
	field = field.lower()
	if field == "awd":
		field = "all_wheel"
	elif field == "price":
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

	results = []   
    for (field, op, value) in params:
        print(field, op, value, "IN FOR")
        field = translate_fieldname(field)
        op = translate_op(op)
        
        query_result = doc_ref.where(filter=FieldFilter(field, op, value)).stream()
        
		new_cars = [Car.from_dict(doc.to_dict()) for doc in query_result]
        
		if results == []:
             results = new_cars
        else:
			 new_result = []
             for car in new_cars:
                 if car in results:
                     new_result.append(car)
             results = new_result
                     
    
    
    cars = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
    
    if len(cars) == 0:
        print("No cars found")    
        return 

    Car.print_cars(cars)
        

#for testing 
#make_query([["name", "==", "Mini Cooper"]])
#make_query([["msrp", ">", 30000]])
#make_query([["msrp", ">", 30000], ["horsepower", ">", 300]])


    
