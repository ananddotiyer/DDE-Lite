#############################################################################################################################################
__filename__ = "functions.py"
__description__ = """All (builtin and user-defined function definitions go here.

"""

__author__ = "Anand Iyer"
__copyright__ = "Copyright 2016-17, Anand Iyer"
__credits__ = ["Anand Iyer"]
__version__ = "2.6"
__maintainer__ = "Anand Iyer"
__email__ = "anand.iyer@moolya.com"
__status__ = "Testing" #Upgrade to Production once tested to function.
#############################################################################################################################################
import ast
import re
import traceback
import support
import rstr
import random
import math
from scrapy.crawler import CrawlerProcess
from decimal import Decimal
from fractions import Fraction

current_module = __import__(__name__)

###########################################built-in functions################################################
def CHOICE (function_args):
    """
    Makes a random choice from a list of many items.
    Parameters: list of values separated by comma.
    """
    function_args = support.remove_slashes (function_args)

    try:
        return_value = random.choice (function_args)
    except:
        support.log ("!!Exception in function CHOICE!!", True)
        return_value = ""
        
    return return_value

def CHOICE_RANGE (function_args):
    """
    Makes a random choice from within a range of numbers, and
    optionally round it to the nearest multiple of given number
    Parameters: start, stop, [round]
    """
    function_args = support.remove_slashes (function_args)

    if len (function_args) == 2:
        round_to = 1
    elif len (function_args) == 3: #round
        round_to = function_args[2]
    
    try:
        return_value = support.roundup (random.randint (int (float (function_args[0])), int (float (function_args[1]))), round_to)
    except:
        support.log ("!!Exception in function CHOICE_RANGE!!", True)
        return_value = ""
    
    return return_value

def INDIRECT (function_args):
    """
    Makes a random choice from one of the many lists, depending on another value.
    Parameters: reference, dictionary.
    """
    args_dict = {}
    
    function_args = support.remove_slashes (function_args)

    key_arg = function_args[0].replace ("'","")
    args_dict = ast.literal_eval((function_args[1]))
    
    try:
        return_value = CHOICE (['%s' %(each) for each in args_dict[key_arg]])
    except:
        support.log ("!!Exception in function INDIRECT!!", True)
        return_value = ""
    
    return return_value

def DATE_RANDOM (function_args):
    """
    Returns a random date between the given start and end dates.
    Parameters: start date, end date.
    """
    function_args = support.remove_slashes (function_args)

    start = function_args[0]
    end = function_args[1]
    
    try:
        return_value = support.strTimeProp(start, end, '%m-%d-%Y')
    except:
        support.log ("!!Exception in function DATE_RANDOM!!", True)
        return_value = ""
        
    return return_value

def IF (function_args):
    """
    Returns return_true, if actual matches expected, else returns return_false.
    Parameters: actual, expected, return_true,  [return_false]
    """
    function_args = support.remove_slashes (function_args)

    if len (function_args) == 3: #no else parameter
        function_args.append ("")
        
    try:
        if function_args[0] == function_args[1]:
            return_value = function_args[2]
        else:
            return_value = function_args[3]
    except:
        support.log ("!!Exception in function IF!!", True)
        return_value = ""
        
    return return_value

def FAKE (function_args):
    """
    Generate fake data for multiple categories, including name, company, address etc.
    Data can be generated in 35 different languages.
    Refer https://faker.readthedocs.io/en/master/ for more information.
    Parameters: category, [language]
    """
    function_args = support.remove_slashes (function_args)

    faker = support.my_import ("faker.Factory.create")
    try:
        fake = faker(function_args[1]) #languages, include en_US, hi_IN etc
    except IndexError:
        fake = faker ('en_US')

    try:    
        return_value = getattr (fake, function_args[0])()
    except:
        support.log ("!!Exception in function FAKE!!", True)
        return_value = ""
        
    return return_value

def XEGER (function_args):
    """
    Generate data according to specified regex patterns.
    Refer https://pypi.python.org/pypi/rstr/2.2.5 for more information.
    Parameters: regex pattern
    """
    function_args = support.remove_slashes (function_args)

    try:
        return_value = rstr.xeger(function_args[0])
    except:
        support.log ("!!Exception in function XEGER!!", True)
        return_value = ""
        
    return return_value

def STR_LENGTH (function_args):
    """
    Length of the specified string, formatted as a string.
    Parameters: original_string
    """
    function_args = support.remove_slashes (function_args)
    
    try:
        return_value = str (len (function_args[0]))
    except:
        support.log ("!!Exception in function STR_LENGTH!!", True)
        return_value = ""
        
    return return_value

def STR_SPLIT (function_args):
    """
    Splits string by single space, and returns the string indexed by given number.
    Parameters: string_to_split, index
    """
    function_args = support.remove_slashes (function_args)

    try:
        return_value = str.split (function_args[0])[int(function_args[1])]
    except:
        support.log ("!!Exception in function STR_SPLIT!!", True)
        return_value = ""
        
    return return_value

def STR_REPLACE (function_args):
    """
    Replace part of a string by another, according to specified regex patterns.
    Parameters: pattern, replace_with, original_string
    """
    function_args = support.remove_slashes (function_args)

    try:
        return_value = re.sub (function_args[0], function_args[1], function_args[2])
    except:
        support.log ("!!Exception in function STR_REPLACE!!", True)
        return_value = ""
        
    return return_value

def STR_SUB (function_args):
    """
    Extract sub-string from given string.
    Works in forward/reverse mode, depending on sign of start_index.
    Parameters: string_to_search, start, stop
    """
    function_args = support.remove_slashes (function_args)

    function_args[1] = int (function_args[1])
    function_args[2] = int(function_args[2])
    length = len (function_args[0])
    
    #function_args[1] is the start index, function_args[2] is the number of characters to sub.
    #in the method used below, function_args[2] is transformed to the end index
    if int(function_args[1]) >= 0:
        function_args[1] = function_args[1]
        function_args[2] = function_args[1] + function_args[2]
        step = 1
    else:
        function_args[1] = length + function_args[1]
        if length == function_args[2]: #so as to display the full string in reverse.
            function_args[2] = None
        else:
            function_args[2] = function_args[1] - function_args[2]
        step = -1
        
    return function_args[0][function_args[1]:function_args[2]:step]

def STR_CONCAT (function_args):
    """
    Concatenates multiple strings provided as its arguments.
    Parameters: list of strings to concatenate, separated by comma.
    """
    function_args = support.remove_slashes (function_args)

    result = ""
    for each in function_args:
        result += each
    return result

def LIST (function_args):
    """
    Creates a list, with specified string values.
    Parameters: list of strings to populate returned list.
    """
    function_args = support.remove_slashes (function_args)

    result = []
    
    for each in function_args:
        yield each
        
def NEXT (function_args): #function_args must be iterator object
    """
    Gets next item from a list.  Supports only list of strings.
    Parameters: $variable
    """
    function_args = support.remove_slashes (function_args)

    try:
        next_in_list = getattr (current_module, function_args[0][1:]).next() #remove the $
    except:
        next_in_list = ""
    
    return next_in_list

def LIST_FILES (function_args):
    """
    Generates a list of files (with absolute file path),
    by way of recursive search, from specified folder.
    Parameters: folder in system, to list files from.
    """
    function_args = support.remove_slashes (function_args)

    files_list = []
    
    import os
    for (root, subFolders, files) in os.walk(function_args[0]):
        for each_file in files:
            yield (os.path.join(root,each_file))

def LIST_FILES_WITH_LINKS (function_args):
    """
    Generates a list of files (with absolute file path) with hyperlinks,
    by way of recursive search, from specified folder.
    Parameters: folder in system, to list files from.
    """
    function_args = support.remove_slashes (function_args)

    files_list = []
    
    import os
    for (root, subFolders, files) in os.walk(function_args[0]):
        for each_file in files:
            yield ('=HYPERLINK("' + os.path.join(root,each_file) + '","' + each_file + '")')

def LIST_FROM_DICT (function_args):
    """
    Generates separate lists from dictionaries, by its keys.
    Parameters: original_dictionary, key
    """
    function_args = support.remove_slashes (function_args)

    result = []
    
    for each in list (getattr (current_module, function_args[0][1:])):
        yield (each[function_args[1]])
    
def LIST_SERIAL (function_args):
    """
    Generates a list of serial numbers, in a given range.
    Parameters: prefix (use None for no prefix), start, stop, [skip]
    """
    function_args = support.remove_slashes (function_args)

    result = []
    if len (function_args) == 2:
        result = range (int(function_args[1])) #next () works only on iterator object
    elif len (function_args) == 3:
        result = range (int(function_args[1]),int(function_args[2])) #next () works only on iterator object
    elif len(function_args) == 4:
        result = range (int(function_args[1]),int(function_args[2]),int(function_args[3])) #next () works only on iterator object

    #handle prefix.  Use None for no prefix.
    if function_args[0] != "None":
        result = iter ([function_args[0] + '%04d' %(each) for each in result])
    else:
        result = iter (['%04d' %(each) for each in result])
    
    return result

def EVAL_IN_PYTHON (function_args):
    """
    Evaluates basic python function calls.  Support references.
    Parameters: python function to evaluate.
    """
    function_args = support.remove_slashes (function_args)
    result = ""
    try:
        result = eval (function_args)
        if type(result) == list:
            result = iter(result)
        elif type(result) == int:
            result = str (result)
    except:
        support.log ("!!Exception: cannot evaluate python code!!", True)
        #traceback.print_exc(file=sys.stdout)
        
    return result

def VIDEO_SEARCH (function_args):
    """
    Generates a list of Youtube videos containing specified keywords.
    Refer https://developers.google.com/youtube/v3/docs/search/list for more information.
    Parameters: filter terms (use '|' to separate multiple)
    """
    import YoutubeSearch
    function_args = support.remove_slashes (function_args)

    videos_list = YoutubeSearch.video_search (function_args[0])

    return videos_list #iter

def VIDEO_SIMILAR (function_args):
    """
    Generates list of similar/recommended Youtube videos.
    Refer https://developers.google.com/youtube/v3/docs/search/list for more information.
    Parameters: video_id
    """
    import YoutubeSearch
    function_args = support.remove_slashes (function_args)

    videos_list = YoutubeSearch.video_similar (function_args[0])

    return videos_list #iter

def LIST_EXTRACT_HTML (function_args):
    """
    Extracts data using given XPATH, from an HTML page.
    Parameters: url, xpath
    """
    import Crawler
    
    process = CrawlerProcess()
    
    process.crawl (Crawler.HTMLSpider, url=function_args[0], xpath=support.remove_slashes (function_args[1]), parse_function="parse_xpath")
    process.start() # the script will block here until the crawling is finished
    process.stop()
    
    return iter (Crawler.return_parse_xpath) #because reactor cannot be restarted, return a list and use next.

def LIST_LINKS_HTML (function_args):
    """
    Extracts embedded links from within the article, in HTML page.
    Parameters: url, [xpath]
    """
    import Crawler
    
    process = CrawlerProcess()
    
    xpath = ""
    if len (function_args) == 2:
        xpath = support.remove_slashes (function_args[1])
        
    process.crawl (Crawler.HTMLSpider, url=function_args[0], xpath=xpath, parse_function="parse_links")
    process.start() # the script will block here until the crawling is finished
    process.stop()
    
    return iter(Crawler.return_parse_links)

def EXTRACT_AMAZON (function_args):
    """
    Extracts multiple attributes (name, manufacturer, price) from amazon search result page.
    Parameters: url
    """
    import Crawler
    
    process = CrawlerProcess()
    
    process.crawl (Crawler.HTMLSpider, url=function_args[0], xpath="", parse_function="parse_amazon_pages")
    process.start() # the script will block here until the crawling is finished
    process.stop()
    
    return Crawler.return_parse_amazon_pages

#########################################user-defined functions##############################################

def APPLY_PERCENT (function_args):
    function_args = support.remove_slashes (function_args)

    try:
        return_value = str (float (function_args[0]) * int (function_args[1]) /100)
    except:
        support.log ("!!Exception in function APPLY_PERCENT!!", True)
        return_value = ""
        
    return return_value

def SAYHELLO (function_args):
    function_args = support.remove_slashes (function_args)

    try:
        return_value = "Hello, " + function_args[0]
    except:
        support.log ("!!Exception in function SAYHELLO!!", True)
        return_value = ""
        
    return return_value

def FRACTION (function_args):
    function_args = support.remove_slashes (function_args)

    try:
        value = str (function_args[0])
        dec = Decimal(value)
        power_of_10 = math.pow (10, -dec.as_tuple().exponent)
        
        frac = Fraction (*float.as_integer_ratio(float (dec))).limit_denominator (int(power_of_10))
        return (str (frac.numerator) + "/" + str (frac.denominator))
    except:
        support.log ("!!Exception in function FRACTION!!", True)
        return_value = ""
        
    return return_value