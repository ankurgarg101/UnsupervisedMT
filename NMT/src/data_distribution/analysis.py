import sys
import json
import os
import numpy as np
import argparse

def parse_args(parser):
	
	parser.add_argument('-f1', dest='f1_file', type=str, required=True, help="intent file1")
	parser.add_argument('-f2', dest='f2_file', type=str, required=True, help="snippet file2")
	
	return vars(parser.parse_args())

def read(fp):

	with open(fp, 'r') as f:
		return [ l.strip().split() for l in f.readlines()]

def gen_bins(x, y):

	minv = min([ len(l) for l in x ])
	maxv = max([ len(l) for l in x ])
	print(minv, maxv)
	bins = {}

	for i, l in enumerate(y):

		bin_id = (len(x[i]) - minv) // 5

		if bin_id not in bins:
			bins[bin_id] = []

		bins[bin_id].append(len(l))

		#if len(l) > 1000:
		#	print(i, x[i], l)

	print ('---printing max vals-----')

	for bin_id in bins:
		print (bin_id*5, max(bins[bin_id]), min(bins[bin_id]), len(bins[bin_id]), np.mean(bins[bin_id]), np.median(bins[bin_id]), np.percentile(bins[bin_id], 75), np.percentile(bins[bin_id], 95), np.percentile(bins[bin_id], 99) )

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	params = parse_args(parser)
	x = read(params['f1_file'])
	y = read(params['f2_file'])
	gen_bins(x, y)