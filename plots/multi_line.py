"""
Module that plots the multi-line plot using matplotlib
"""

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import os
import csv

metric_names = {
	
	'bleu': 'BLEU Scores',
	'tok': 'Token Accuracy',
	'ast': 'AST Metric',
	'brack': 'Brackets Metric'
}

c = ['dev', 'test']

def get_data(params):

	fp = os.path.join(params['in_dir'], '{}_{}.csv'.format(params['metric'], params['mode']))

	col_data = {}
	col_map = {}

	with open(fp, 'r') as f:
		reader = csv.reader(f)

		l = 0
		rl = 0
		for row in reader:
			
			
			if l == 0:
				rl = len(row[1:])

				for k in range(rl):

					if k//2:
						col_data['{}-{}'.format(c[k%2], params['set'])] = {
							'xv': [],
							'yv': []
						}
						col_map[k] = '{}-{}'.format(c[k%2], params['set'])
					else:
						col_data['{}'.format(c[k%2])] = {
							'xv': [],
							'yv': []
						}
						col_map[k] = '{}'.format(c[k%2])
			if l < 2:
				l += 1
				continue

			print(col_data.keys())
			print(col_map)
			xv = float(row[0])
			for k in range(rl):

				if str(row[1+k]) == '-':
					continue 

				col_data[col_map[k]]['xv'].append(xv)
				col_data[col_map[k]]['yv'].append(float(row[1+k]))

	# Dummy data for now
	data = []

	# add all information regarding data here. Currently, assumes 4 line charts to be plotted but can be extended easily
	l = 0
	i=0

	print(len(col_data))
	for dk in col_data:
		
		dj = col_data[dk]

		di = {}
		
		# The x value labels and corresponding data needs to be filled here
		# NOTE: Ensure the ylabel is set correctly.

		di['x'] = [ str(j) + 'x' for j in dj['xv'] ] 
		di[dk] = dj['yv']
		
		di['xlabel'] = 'x'
		di['ylabel'] = dk

		# Set the color schema, linestyle, and label
		di['color'] = 'blue' if i%2 else 'red'
		di['linestyle'] = 'solid' if i < 2 else 'dashed'
		di['label'] = di['ylabel']
		print(dk)

		data.append(di)
		i+=1

	print(data)
	return data

def plot_line_chart(data, params):
	
	# multiple line plot
	
	for di in data:
		plt.plot( di['xlabel'], di['ylabel'], data=di, color=di['color'], linestyle=di['linestyle'], label=di['label'])

	# Parameterize the xlabel if needed
	plt.xlabel("Ratio of Unpaired Data to Paired Data", fontsize='large')
	plt.ylabel(metric_names[params['metric']], fontsize='large')
	plt.legend()
	plt.xticks(fontsize='medium', rotation='vertical')
	plt.tight_layout()
	op = os.path.join(params['out_dir'], '{}_{}.eps'.format(params['metric'], params['mode']))
	plt.savefig(op, format='eps')
	plt.close()

	return

if __name__ == "__main__":

	# Parse the arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--out_dir', type=str, default="/home/marauder/ut/nlp_cs388/final_proj/fp_plots/", help="Path of output plots")
	parser.add_argument('--in_dir', type=str, default="/home/marauder/ut/nlp_cs388/final_proj/fp_res/", help="Path of res csv files")
	parser.add_argument('--metric', required=True, help="Name of the metric to show in the plot")
	parser.add_argument('--mode', required=True)
	parser.add_argument('--set', required=True)
	params = vars(parser.parse_args())
	
	print(params)
	if not os.path.exists(params['out_dir']):
		os.makedirs(params['out_dir'])

	# Write the data fetching logic in this function
	data = get_data(params)
	plot_line_chart(data, params)