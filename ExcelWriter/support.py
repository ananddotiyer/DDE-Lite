#############################################################################################################################################
__filename__ = "support.py"
__description__ = """All support functions used by main program.

"""

__author__ = "Anand Iyer"
__copyright__ = "Copyright 2016-17, Anand Iyer"
__credits__ = ["Anand Iyer"]
__version__ = "2.6"
__maintainer__ = "Anand Iyer"
__email__ = "anand.iyer@moolya.com"
__status__ = "Testing" #Upgrade to Production once tested to function.
#############################################################################################################################################
import traceback
import sys
import re
import shlex
import time
import random
import math

flog = open ("log.txt", "w")
fkeys = open ("api_keys.txt")

def roundup(to_round, round_to=1):
    return int(math.ceil(to_round / float (round_to))) * int (round_to)

def extract_xpath (selector, xpath, url=False):
    extracted = selector.xpath(xpath).extract()
    if type(extracted) == list:
        return_value = ''.join (extracted)
    
    if not url:
        return_value = return_value.replace ('"', '')[0:100] #remove all quotes and truncate to 100 characters

    return return_value
    
def get_key (service):
    key = ""
    pattern_key = re.compile ("(.*):(.*)")
    for line in fkeys:
        key_object = pattern_key.search (line)
        if key_object:
            if service == key_object.groups(1)[0]:
                key = key_object.groups(1)[1]
                break
    
    if key != "":
        return key
    else:
        log ("API key for youtube service is missing from api_keys file!")
        log()

def isdigit(arg):
    try:
        int(arg)
        is_digit = True
    except ValueError:
        is_digit = False

    return is_digit

def strTimeProp(start, end, format):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + random.random() * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

#remove starting/trailing slash from a every element in a list or string.
def remove_slashes (input_value):
    return_value = input_value
    
    if type (input_value) == list:
        return_value = []
        for each in input_value:
            each = str (each) #new
            if each != "" and each[0] == '/' and each[-1] == '/':
                return_value.append (each[1:-1])
            else:
                return_value.append (each)
    else:
        if input_value != "" and input_value[0] == '/' and input_value[-1] == '/':
            return_value = input_value[1:-1]

    return return_value

def lexer_setup (function_args):
    lexer = shlex.shlex(function_args)
    lexer.quotes = '/'
    lexer.whitespace = ', '
    lexer.wordchars += '\''
    lexer.whitespace_split = True
    return lexer

def log (statement="", exception=False):
    if statement != "" and statement[-1] == ",":
        print (statement[:-1],end='')
        flog.write (statement[:-1])
    else:
        print (statement)
        flog.write (statement + "\n")
    
    if exception:
        traceback.print_exc(file=flog)
        flog.write ("\n")
        #traceback.print_exc(sys.stdout)
        print()