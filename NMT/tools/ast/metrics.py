import os
import sys
import argparse
from os import path
import post_processing as pp

def parse_args(parser):
	parser.add_argument('-ref', dest='ref', type=str, required=True, help="Reference file path")
	parser.add_argument('-hyp', dest='hyp', type=str, required=True, help="Hypothesis file path")
	parser.add_argument('-mode', dest='mode', type=str, nargs='?', default='y', help="Metrics of x or y", choices=['x','y'])
	return vars(parser.parse_args())



def calculate_y_metrics(ref_file, hyp_file):
	"""
	Calculates all the metrics on y
	"""
	symbol_dict = pp.get_symbols_dict()
	ast = 0
	brackets = 0
	total_lines = 0
	with open(hyp_file, 'r') as hyp:
		for line in hyp:
			total_lines += 1
			hyp_line = line.strip()
			hyp_line = pp.remove_unknown(hyp_line)
			hyp_line = pp.remove_expanded_symbols(hyp_line, symbol_dict)
			if pp.check_valid_syntax(hyp_line):
				ast += 1.0
			if pp.check_valid_bracket_structure(hyp_line):
				brackets += 1.0
	ast /= total_lines
	brackets /= total_lines
	print ("AST: %f"%ast)
	print ("Brackets: %f"%brackets)


def calculate_x_metrics(ref_file, hyp_file):
	return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    params = parse_args(parser)
    if params['mode'] == 'y':
    	calculate_y_metrics(params['ref'], params['hyp'])
    else:
    	calculate_x_metrics(params['ref'], params['hyp'])