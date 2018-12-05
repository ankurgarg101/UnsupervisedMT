import os
import sys
import argparse
from os import path
import processing
import collections
def parse_args(parser):
	parser.add_argument('-f1', dest='f1_file', type=str, required=True, help="snippet file1")
	parser.add_argument('-f2', dest='f2_file', type=str, required=True, help="snippet file2")
	parser.add_argument('-mode', dest='mode', type=str, nargs='?', default='y', help="Metrics of x or y", choices=['x','y'])
	return vars(parser.parse_args())



def compare_distribution(x, y):
	"""
	Compares x and y distribution
	"""
	x_dist, x_avg, x_t = get_all(x)
	y_dist, y_avg, y_t = get_all(y)
	print (len(x_dist), x_avg, x_t)
	print (len(y_dist), y_avg, y_t)
	
def get_all(x_file):
	"""
	Returns dictionary, avg length and total lines
	"""
	total_lines = 0
	total_length = 0
	histogram = collections.defaultdict(int)
	ignore_list = processing.get_ast_ignore_list()
	with open(x_file, 'r') as f:
		for line in f:
			total_lines += 1
			total_length += len(line.strip())
			histogram = processing.get_distribution(line.strip(), ignore_list, histogram)
	return histogram, float(total_length)/total_lines, total_lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    params = parse_args(parser)
    compare_distribution(params['f1_file'], params['f2_file'])
    