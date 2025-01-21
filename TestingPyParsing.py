import pyparsing as pparse
# basic example of pyparsing module
# correct syntax defined here
testSyntax = pparse.Word(pparse.alphas) + ',' + pparse.Word(pparse.alphas) + '!'

userInput = input('Enter a word followed by a comma, another word, then an exclamation point for correct syntax\n\n')

# try to parse, exception on parsing error return the error string. basically the string entered needs to match the
# syntax defined in testSyntax or else it'll error out.
try:
    output = testSyntax.parseString(userInput)
    print(output)
except pparse.exceptions.ParseException:
    print('Parse exception, please use the correct syntax')



