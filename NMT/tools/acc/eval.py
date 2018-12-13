import os
import sys
import argparse
from os import path
import post_processing as pp

def parse_args(parser):
	parser.add_argument('-ref', dest='ref', type=str, required=True, help="Reference file path")
	parser.add_argument('-hyp', dest='hyp', type=str, required=True, help="Hypothesis file path")
	return vars(parser.parse_args())

def calculate_metrics(ref_file, hyp_file):
	"""
	Calculates all the metrics on y
	"""

	correct_tags = 0.0
    total_tags = 0.0
    complete_match = 0.0
    total_lines = 0.0

	with open(hyp_file, 'r') as hyp, open(ref_file, 'r') as ref:
		
		for hyp_line, ref_line in zip(hyp.readlines(), ref.readlines()):

			total_lines += 1
			
			hyp_line = hyp_line.strip()
			ref_line = ref_line.strip()

			if hyp_line == ref_line:
				complete_match += 1

			hyp_tags = hyp_line.split()
			ref_tags = ref_line.split()

			for ht, rt in zip(hyp_tags, ref_tags):

				total_tags += 1

				if ht == rt:
					correct_tags += 1

	print ("TACC: %.5f"%(correct_tags/total_tags))
	print ("CACC: %.5f"%(complete_match/total_lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    params = parse_args(parser)

	calculate_metrics(params['ref'], params['hyp'])