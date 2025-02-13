from pyparsing import *

def parse(query_string: str):
    # remove newline from whitespace characters, because newline terminates queries
    ParserElement.set_default_whitespace_chars(' \t')

    # mark the end of the query string with a newline
    query_string += "\n"
    
    # The operator set is small enough that they can be written explicitely
    # Every operator has a negative, which paired with 'or' and the demorgan laws would allow any
    # logical expression to be representable, but oh well.
    op = (  Keyword("==") | Keyword("!=") | Keyword("is") | 
            Keyword(">") | Keyword(">=") | 
            Keyword("<") | Keyword("<="))

    numeric_field      = CaselessKeyword("price") | CaselessKeyword("msrp") | CaselessKeyword("horsepower")
    alphabetic_field   = CaselessKeyword("make") | CaselessKeyword("model")
    boolean_field      = CaselessKeyword("awd")
	
    multiword = Suppress("\"") + Combine(Word(alphas) + ZeroOrMore(" " + Word(alphas))) + Suppress("\"")
    numeric_value      = Combine(Word(nums) + Optional("." + Word(nums)))
    alphabetic_value   = Word(alphas) | multiword 
    boolean_value      = CaselessKeyword("true") | CaselessKeyword("false")

    numeric_triplet    = Group(numeric_field    + op + numeric_value)
    alphabetic_triplet = Group(alphabetic_field + op + alphabetic_value)
    boolean_triplet    = Group(boolean_field    + op + boolean_value)

    query_triplet      = numeric_triplet | alphabetic_triplet | boolean_triplet

    additional_condition = Suppress(CaselessKeyword("and")) + query_triplet

    # we have one (fieldname op value) triplet, then 0 or more (and fieldname op value) quads
    # testing for newline prevents partially valid queries from being matched
    query = query_triplet + ZeroOrMore(additional_condition) + Suppress("\n")

    # subject the query string to the parser contraints layed out
    # this is notably the only call to parseString
    parsed_query = query.parseString(query_string)	
    return parsed_query
