"""
Module to deal with post processing and calculating ast and bracket syntax scores
"""
import ast


def remove_bpe(code_string, bpe='@@'):
	"""
	Merges bpe litereal
	"""
	code_array = code_string.strip().split()
	new_string = ""
	new_code_array = []
	prev_bpe = False
	for code in code_array:
		if code.endswith(bpe):
			new_code_array.append((code[:-(len(bpe))],prev_bpe))
			prev_bpe = True
		else:
			new_code_array.append((code,prev_bpe))
			prev_bpe = False

	new_string = ""
	for c,b in new_code_array:
		if b:
			new_string += c
		else:
			new_string += " " + c
	new_string = new_string.strip()
	
	return new_string

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

	Finds out how balanced an expression is.
	With a string containing only brackets.

	>>> is_matched('[]()()(((([])))')
	False
	>>> is_matched('[](){{{[]}}}')
	True
	"""
	opening = tuple('({[')
	closing = tuple(')}]')
	mapping = dict(zip(opening, closing))
	queue = []
	for letter in code_string:
		if letter in opening:
			queue.append(mapping[letter])
		elif letter in closing:
			if not queue or letter != queue.pop():
				return False
	return not queue



