from enum import Enum
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter
from car import Car



# base exception class for the interface
class InterfaceError(Exception):
    pass

#change param field to firebase field 
def set_field(field):
    if field == "price":
        field ="dealer_cost"
    if field == "awd":
        field = "all_wheel"
    return field

#just need num fields to be converted from string
def set_request(request, field):
    #db field names
    if field == "msrp":
        request = int(request)
    if field == "horsepower":
        request = int(request)
    if field == "dealer_cost":
        request = int(request)
    if field == "all_wheel":
        #str in db "FALSE" or "TRUE"
        request = str(request).upper()
    return request

def set_operator(operator):
    #need to change is to ==
    if operator == "is":
        operator = "=="
    return operator

def make_query(params):
    doc_ref = None
    db = firestore.client()

    if len(params) < 1:
        raise InterfaceError

    # non compound query
    if len(params) == 1:
        
        field = set_field(params[0][0])  # ex: will be one of the enumerated types specified above
        operator = set_operator(params[0][1])  # ex: ==
        request = set_request(params[0][2], field)  # ex: 'Honda'
        

        # NOTE: this should work for all len(params[1]) == 1
        doc_ref = db.collection("cars").where(filter=FieldFilter(field, operator, request)).stream()
        
    
       
    # compound query
    if len(params) == 2:
        field_1 = set_field(params[0][0])
        field_2 = set_field(params[1][0])

        operator_1 = set_operator(params[0][1])
        operator_2 = set_operator(params[1][1])

        request_1 = set_request(params[0][2], field_1)
        request_2 = set_request(params[1][2], field_2)

        # do the same for 2 params
        #AND
        doc_ref = db.collection("cars").where(filter=FieldFilter(field_1, operator_1, request_1))\
                              .where(filter=FieldFilter(field_2, operator_2, request_2))\
                              .stream()
    
    cars = [Car.from_dict(doc.to_dict()) for doc in doc_ref]
  
    if len(cars) == 0:
        print("No cars found")    
        return 

    if len(params) > 2:
        raise InterfaceError
    
    
    Car.print_cars(cars)
    
        



    