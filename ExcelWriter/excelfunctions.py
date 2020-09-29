#############################################################################################################################################
__filename__ = "excelfunctions.py"
__description__ = """All excel related functions used by main program

"""

__author__ = "Anand Iyer"
__copyright__ = "Copyright 2016-17, Anand Iyer"
__credits__ = ["Anand Iyer"]
__version__ = "2.6"
__maintainer__ = "Anand Iyer"
__email__ = "anand.iyer@moolya.com"
__status__ = "Testing" #Upgrade to Production once tested to function.
#############################################################################################################################################
from xlutils.copy import copy
#from xlrd import open_workbook, book
from xlrd import *

def openexcel (filename, sheetindex, mode="r"):
	mybook = mycopybook = mysheet = None
	
	if mode == "r":
		mybook = open_workbook(filename)
		mysheet = mybook.sheet_by_index (sheetindex)
		return mybook, mysheet
	else:
		mybook = open_workbook(filename, formatting_info=True, on_demand=True)
		mycopybook = copy(mybook)
		#sheet = get_sheet_by_name (copybook, sheetname)
		mysheet = mycopybook.get_sheet (sheetindex)
		return mybook, mycopybook, mysheet
		
def closeexcel (mybook):
	mybook.release_resources()
	
def get_sheet_by_name(book, name):
	idx = 0
	try:
		while True:
			sheet = book.get_sheet(idx)
			if sheet.name == name:
				return sheet
			idx += 1
	except IndexError:
		return None

def readfromexcelmap (excel_map, row, col):
	return excel_map[(row, col)]
	#return sheet.cell(row, col).value

def readfromexcel (sheet, row, col):
	try:
		cell_value = sheet.cell(row, col).value
	except:
		cell_value = ""
	return cell_value

def writetoexcel (sheet, row, col, text):
	sheet.write (row, col - 1, text)

#unused function
def writetoexcel_old (sheet, row, col, text):
	rb = open_workbook("NSPBU_Template_New.xls", formatting_info=True, on_demand=True)
	wb = copy(rb)
	wb.get_sheet(0).write(0,0,'changed!')
	sheet.save("output.xls")
	
def map_excel (sheet, start_row, end_row, colcount):
	excel_map = {}
	
	for each_row in range (start_row, end_row):
		for each_col in range (colcount):
			excel_map[(each_row, each_col + 1)] = readfromexcel (sheet, each_row, each_col)
			
	return excel_map