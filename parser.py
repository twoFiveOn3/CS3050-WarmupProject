from pyparsing import *
from query import make_query

def parse(querystring: str):
    # remove newline from whitespace characters, because newline terminates queries
    ParserElement.set_default_whitespace_chars(' \t')

    # fieldname is a string of letters identifying a field within the database
    fieldname = Word(alphas)
    
    # The operator set is small enough that they can be written explicitely
    # Every operator has a negative, which paired with 'or' and the demorgan laws would allow any
    # logical expression to be representable, but oh well.
    op = (  Keyword("==") | Keyword("!=") | Keyword("is") | 
            Keyword(">") | Keyword(">=") | 
            Keyword("<") | Keyword("<="))

    # all fields in the db are alphabetic string or integer valued
    value = Word(alphas) | Word(nums)

    querytriplet = fieldname + op + value
    additionalcondition = Keyword("and") + querytriplet
    
    # we have one (fieldname op value) triplet, then 0 or more (and fieldname op value) quads
    # restricting the ql to a single 'and' is lazy and we're not doing it. I will fix the query function if that's a problem.
    query = querytriplet + ZeroOrMore(additionalcondition)
    parsedquery = query.parseString(querystring)
    
    #TODO: return parsed query as a list of lists
    print(parsedquery)

    


#for testing 
parse("make is toyota")


#TODO: parser gets rid of "Cooper" in "Mini Cooper"
parse("name == Mini Cooper")
#make_query([["msrp", ">", 30000]])
parsed_str = parse("msrp > 30000")
make_query(parsed_str)

#make_query([["msrp", ">", 30000], ["horsepower", ">", 300]])

#TODO: parser returns ['msrp', '>', '30000', 'and', 'horsepower', '>', '300'] instead of [['msrp', '>', '30000'], ['horsepower', '>', '300']]
parsed_str = parse("msrp > 30000 and horsepower > 300")
make_query(parsed_str)
