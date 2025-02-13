from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

from car import Car
from parser import parse
from auth import auth

# parser syntax varies slightly from data syntax
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


def make_query(conditions: list):
    # this function is temporarily disable to avoid excess queries
    # at present, submitting even a hard coded query returns everything in the database
    # everytime for me.
    print("Aborting query with conditions: ", conditions)
    return
    
    # open database handle
    db = firestore.client()
    doc_ref = db.collection("cars")
    
    # I have done some research and I am almost certain calling where repeatedly in this way works
    # there is something more seriously wrong with our data/database which is causing queries not to work
    # single, hard-coded calls to where are returning everything in the database
    # it is not a problem with this code, its something worse
    for (field, op, value) in conditions:
        # paper over the minor asymmetries in query language and real field names
	field = translate_fieldname(field)
        # add support for "is", which is just an alias for "=="
        op = translate_op(op)
        # apply condition
        doc_ref.where(field, op, value)

    # assign query results to a DocumentSnapshot generator with stream
    results = doc_ref.stream()
    # convert snapshot results to Car objects
    cars = [Car.from_dict(doc.to_dict()) for doc in results]
    
    for snapshot in results:
        print(snapshot.to_dict())
    # print results
    if cars:
        Car.print_cars(cars)
    else:
        print("No cars found")        

def print_help_menu():
    print("Queries must be in the form: <field> <operator> <value>\n"
          "Multiple conditions can be queried by joining them with \"and\"\n"
          "Ex. make is toyota and price <= 30000 and awd is true\n"
	  "Multiword values must be placed in \" \"\n"
	  "Ex. make is \"mini cooper\" and price >= 10000\n"
	  "Supported operators: ==(aka \"is\"), !=, >, <, >=, <=\n"
          "Supported fields: make, model, price, msrp, horsepower, awd\n"
          
	  "For help: type 'help' to see this menu again \n"
          "To exit: type 'quit' ")

if __name__ == "__main__":
    #auth()

    while True:
        query_string = input('> ')
        if query_string == "":
            continue
        if query_string.lower() == 'help':
            print_help_menu()
            continue  # restart while loop
        if query_string.lower() == 'quit':
            break
        # otherwise call parse
        try:
            parsed_query = parse(query_string)
            
            make_query(parsed_query)
        except Exception as e:
            print("Error: ", e, "try again, for help making a query, type 'help'")
            continue
    
