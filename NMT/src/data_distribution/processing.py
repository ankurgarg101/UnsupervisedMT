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
	symbols_dict['#SLASH#'] = '\\'
	return symbols_dict

def get_ast_ignore_list():
	ast_class_list = ["Module", "Expr", "Num", "Str", "FormattedValue", "JoinedStr", "Bytes", "NameConstant", "Ellipsis", "Constant", "Attribute", "Subscript", "Starred", "Name", "List", "Tuple", "Load", "Store", "Del", "AugLoad", "AugStore", "Param"] 
	return ast_class_list

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


def get_distribution(code_string, ignore_list, dist):
	symbol_dict = get_symbols_dict()
	code_string = remove_unknown(code_string)
	code_string = remove_expanded_symbols(code_string, symbol_dict)
	if check_valid_syntax(code_string):
		node = ast.parse(code_string)
		for child in ast.walk(node):
			ast_type = str(type(child)).split("'")[1][5:]
			if ast_type in ignore_list:
				continue
			elif ast_type == "Call":
				dump = str(ast.dump(child))
				#hard coded
				if "func=Name(id=" in dump:
					func_name = dump.split("func=Name(id=")[1].split(",")[0][1:-1]
					ast_type += ("_"+func_name)
				elif "Attribute" in dump:
					func_name = dump.split("attr=")[1].split(",")[0][1:-1]
					ast_type += ("_"+func_name)
				else:
					pass
			dist[ast_type] += 1
	return dist

import collections

# histogram = collections.defaultdict(int)
# f = get_distribution("input ( s )", get_ast_ignore_list(),histogram)
# print (f)

# f = get_distribution("for i in range(x):\n\tprint(i,x)", get_ast_ignore_list(), histogram)
# print (f)

# f = get_distribution("for i in range(x):\n\tprint(i,x)", get_ast_ignore_list(), histogram)
# print (f)