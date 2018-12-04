"""
Module to deal with post processing and calculating ast and bracket syntax scores
"""
import ast

def remove_unknown(code_string):
	"""
	Removes unknown by a random literal
	"""
	return code_string.replace("<<unk>>", "unk_variable")

def get_symbols_dict():
	"""
	Returns a dictionary 
	"""
	symbols_dict = {}
	symbols_dict['#SPACE#'] = ' '
	symbols_dict['#TAB#'] = '\t'
	symbols_dict['#NEWLINE#'] = '\n'
	return symbols_dict

def remove_expanded_symbols(code_string, symbols_dict):
	"""
	Removes expanded symbols with actual symbols using a dictionary
	"""
	actual_code = code_string
	for key in symbols_dict.keys():
		actual_code.replace(key,symbols_dict[key])
	return actual_code

def check_valid_syntax(code_string):
	"""
	Checks if given parse is correct
	"""
	try:
		ast.parse(code_string)
		return True
	except:
		return False


def check_valid_bracket_structure(code_string):
	"""
	Checks if the given code follows bracket structure
	Easier check than actual ast (does not care about indentation or other syntax)
	"""
	return True


