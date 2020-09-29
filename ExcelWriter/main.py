#############################################################################################################################################
__filename__ = "main.py"
__description__ = """Represents main program.

"""

__author__ = "Anand Iyer"
__copyright__ = "Copyright 2016-17, Anand Iyer"
__credits__ = ["Anand Iyer"]
__version__ = "2.6"
__maintainer__ = "Anand Iyer"
__email__ = "anand.iyer@moolya.com"
__status__ = "Testing" #Upgrade to Production once tested to function.
#############################################################################################################################################
import re
import random
import sys
import os
import argparse
import support

from importlib import import_module

from excelfunctions import *

default_module = __import__("functions") #functions.py
    
def store (line_counter, variable, fp, function_args):
    return_value = call_function (line_counter, fp, function_args)
    setattr (default_module, variable, return_value)
    return "Stored return value in $%s" %(variable)

def handle_reference (pattern, each, each_row, replace=False):
    m = re.search (pattern, each)
    if m is not None:
        try:
            return_value = readfromexcelmap (excel_map, each_row, int (m.groups(1)[0]))
            if replace:
                if type (return_value) == str and not support.isdigit (return_value):
                    return_value = "'" + return_value + "'"
                return_value = re.sub (pattern, return_value, each)
        except:
            pass
    else:
        return_value = each
        
    return return_value
            
def call_function (each_row, fp, function_args):
    global excel_map
    
    all_args = []
    
    if fp == None:
        function_args = list(support.lexer_setup(function_args)) #function_args is now a list of arguments, with commas ignored between two forward slashes
        for each in function_args:
            all_args.append (handle_reference ("C(\d+)$", each, each_row))
        return_value = ''.join (all_args) #populate with plain strings.  No function calls.
    elif "EVAL_IN_PYTHON" in str (fp):
        #Need to first split the arguments, so we can use the references.  Now, join appropriately to form the function call syntax.
        function, function_args = extract_function_with_args (pattern_eval, function_args) #function_args[0]
        function_args = list(support.lexer_setup(function_args)) #function_args is now a list of arguments, with commas ignored between two forward slashes
        for each in function_args:
            arg = handle_reference ("C(\d+)$", each, each_row)
            if type(arg) == str and not support.isdigit(arg):
                arg = "'" + arg + "'"
            all_args.append (arg)
        
        all_args = function + "(" + ','.join(str(x) for x in all_args) + ")"
        all_args = support.remove_slashes (all_args)
        
        return_value = fp (all_args) #internal calls the function with appropriate arguments
    elif callable (fp):
        function_args = list(support.lexer_setup(function_args)) #function_args is now a list of arguments, with commas ignored between two forward slashes
        for each in function_args:
            all_args.append (handle_reference ("C(\d+)$", each, each_row))
        return_value = fp (all_args) #internal calls the function with appropriate arguments

    return return_value

#Call function once for each row to fill
#If there are column references, use it along with current row, and fill in actual value
#Same function is used with fp and function_args passed as None and empty string respectively, to populate plain strings.
def construct_result_dict (start_row, col, end_row, fp, function_args):
    return_list = []

    for each_row in range (start_row, end_row):
        return_list.append (call_function (each_row, fp, function_args))
    
    #construct tuple for row, col number, in order construct the result dictionary.
    all_cells = []
    for each_row in range (start_row, end_row):
        all_cells.append ((each_row, col))
    
    #and return all results as part of a single dictionary.
    return dict(zip(all_cells, return_list))

def extract_function_with_args (pattern, function_to_call):
    function = ""
    function_args = ""
    
    function_object = pattern.search (function_to_call)
    if function_object:
        function = function_object.groups(1)[0]
        function_args = str (function_object.groups(1)[1]).strip ()
    
    return function, function_args

def get_function (line):
    function = ""
    function_args = ""
    mod = None
    
    #some defaults
    variable = ""
    start_row = 1
    col = 0
    
    try:
        #Identify start_row and col
        pattern_row_col = re.compile ("R(\d+)C(\d+)")
        row_col_object = pattern_row_col.search (line)
        if row_col_object:
            start_row = int (row_col_object.groups(1)[0])
            col = int (row_col_object.groups(0)[1])

        #Identify variable
        pattern_variable = re.compile ("(.*?)\|(.*?)\|(.*?)\|(.*)")
        variable_object = pattern_variable.search (line)
        if variable_object:
            if variable_object.groups(0)[0][0] == "$":
                variable = variable_object.groups(0)[0][1:] #remove the $
            function_to_call = variable_object.groups(0)[3]

        function, function_args = extract_function_with_args (pattern, function_to_call)
    except:
        pass

    end_row = start_row + rows_to_fill

    return start_row, col, end_row, mod, variable, function, function_args

#main program
support.log ("####ExcelWriter version %s.  %s####" %(__version__, __copyright__))
support.log ()

pattern = re.compile ("\((.*?):(.*)\)")
pattern_eval = re.compile ("(.*)\((.*)\)")

#"parser" is an "argparse" object that defaults to certain values for each of the command line arguments
#Following command line arguments are supported = config, rowcount, colcount, startrow.
#Use with appropriate switches, when calling from command line.
parser = argparse.ArgumentParser(prog='python main.py', conflict_handler='resolve')
parser.add_argument("--config", help="Configuration file", default="..\\Template.txt")
parser.add_argument("--output", help="Output excel", default="..\\Template_latest.xls")
parser.add_argument("--rowcount", help="Number of rows to fill in Excel template", default=5)
parser.add_argument("--colcount", help="Number of columns in Excel template", default=10)
parser.add_argument("--startrow", help="Starting row number (to generate excel map)", default=1)
args = parser.parse_args()

config_file = args.config

f = open  (config_file) #input config file

book, sheet = openexcel (os.path.splitext(config_file)[0] + ".xls", 0) #0 is the first sheet

rows_to_fill = int (args.rowcount)
start_row = int (args.startrow)
end_row = start_row + rows_to_fill
colcount = int (args.colcount)

excel_map = {}
excel_map = map_excel (sheet, start_row, end_row, colcount)

line_counter = 0
for line in f:
    line_counter += 1
    
    if len (line) == 1 or line[0] == '#': #only newline or line has been commented
        continue
    
    start_row, col, end_row, mod, variable, function, function_args = get_function (line) #in case of plain string, function and function_args are empty.

    if mod is None:
        mod = default_module

    if function == "":
        plain_string = line.split ('|')[3].strip('\n')
        return_dict = construct_result_dict (start_row, col, end_row, None, plain_string)
        
        excel_map.update (return_dict)
        
        support.log (str.format ("%d. ," %(line_counter))) # the comma at the end ensures newline is NOT printed.
        support.log (str.format ("========>%s printed %d times" %(plain_string, rows_to_fill)))
        support.log ()
        continue

    try:
        fp = getattr (mod, function) #getting function pointer
    
        support.log (str.format ("%d. ," %(line_counter))) # the comma at the end ensures newline is NOT printed.
        if variable != "":
            support.log (store (line_counter, variable, fp, function_args))
            support.log ()
            continue

        return_dict = construct_result_dict (start_row, col, end_row, fp, function_args)
        
        excel_map.update (return_dict)
        
        #support.log (return_dict)
        support.log (str.format ("========>%s called %d times" %(function, rows_to_fill)))
        support.log ()
    except:
        support.log (str.format ("%s may not exist." %(function)), True)

closeexcel (book)

#write excel_map to excel
book, copybook, sheet = openexcel (os.path.splitext(config_file)[0] + ".xls", 0,"w") #0 is the first sheet
for each in excel_map:
    writetoexcel (sheet, each[0], each[1], excel_map[each])
    
copybook.save(args.output)
support.log (str.format ("Saved to " + args.output + ".  Please rename the file to avoid overwriting during the next iteration."))

closeexcel (book)