from pyparsing import *
from query_test import make_query
from auth import auth

def parse(query_string: str):
    # remove newline from whitespace characters, because newline terminates queries
    ParserElement.set_default_whitespace_chars(' \t')
    
	# The operator set is small enough that they can be written explicitely
    # Every operator has a negative, which paired with 'or' and the demorgan laws would allow any
    # logical expression to be representable, but oh well.
    op = (  Keyword("==") | Keyword("!=") | Keyword("is") | 
            Keyword(">") | Keyword(">=") | 
            Keyword("<") | Keyword("<="))

    numeric_field      = CaselessKeyword("price") | CaselessKeyword("msrp") | CaselessKeyword("horsepower")
    alphabetic_field   = CaselessKeyword("make") | CaselessKeyword("model") | CaselessKeyword("name")
    boolean_field      = CaselessKeyword("awd")
	
    multiword = Suppress("\"") + Combine(Word(alphas) + ZeroOrMore(" " + Word(alphas))) + Suppress("\"")
    numeric_value      = Combine(Word(nums) + Optional("." + Word(nums)))
    alphabetic_value   = Word(alphas) | multiword 
    boolean_value      = CaselessKeyword("true") | CaselessKeyword("false")

    numeric_triplet    = numeric_field    + op + numeric_value
    alphabetic_triplet = alphabetic_field + op + alphabetic_value
    boolean_triplet    = boolean_field    + op + boolean_value

    query_triplet      = numeric_triplet | alphabetic_triplet | boolean_triplet

    additional_condition = Suppress(CaselessKeyword("and")) + query_triplet
    
    # we have one (fieldname op value) triplet, then 0 or more (and fieldname op value) quads
    # restricting the ql to a single 'and' is lazy and we're not doing it. I will fix the query function if that's a problem.
    query = query_triplet + ZeroOrMore(additional_condition)
    parsed_query = query.parseString(query_string)
    
    
    #TODO: return parsed query as a list of lists
    rtn = [parsed_query[i:i + 3] for i in range(0, len(parsed_query), 3)]
    print(rtn, "THIS IS RTN IN PARSER")
    return rtn

def interface():
    auth()
    usr_query = ''
    print_help_menu()
    # begin while loop polling for using input

    #this works 
    #make_query([["msrp", ">", 30000]])
    while usr_query.lower() != 'quit':
        usr_query = input('> ')
        if usr_query.lower() == 'help':
            print_help_menu()
            continue  # restart while loop
        if usr_query.lower() == 'quit':
            exit()
        # otherwise call parse
        try:
            query_elems = parse(usr_query)
            
            make_query(query_elems)
        except Exception as e:
            print("Error: ", e, "try again, for help making a query, type 'help'")
            continue

def print_help_menu():
    print("Query should be in the form: <field> <operator> <delimiter>\n"
          "The language supports the following operators: \n == \n >= \n <= \n < \n > \n "
          "The language supports the following fields: \n Make \n Model \n Price \n MSRP \n Horsepower \n AWD (boolean)"
          "To make a compound query, do so in the form: <field 1> <operator 1> <delimiter 1> 'and' <field 2> <operator 2> <delimiter 2 \n"
          "To search for a field longer than one word, wrap the field with double quotes \n"
          "For help: type 'help' to see this menu again \n"
          "To exit: type 'quit' ")
    
interface()


#for testing 
#parse("make is toyota")


#TODO: parser gets rid of "Cooper" in "Mini Cooper"
#parse("make == \"Mini Cooper\"")
#make_query([["msrp", ">", 30000]])
#parsed_str = parse("msrp > 30000")
#make_query(parsed_str)

#make_query([["msrp", ">", 30000], ["horsepower", ">", 300]])

#TODO: parser returns ['msrp', '>', '30000', 'and', 'horsepower', '>', '300'] instead of [['msrp', '>', '30000'], ['horsepower', '>', '300']]
#parsed_str = parse("msrp > 30000 and horsepower > 300")
#make_query(parsed_str)
