"""
Module that plots the multi-line plot using matplotlib
"""

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

def get_data():

	# Dummy data for now

	data = []

	# add all information regarding data here. Currently, assumes 4 line charts to be plotted but can be extended easily
	for i in range(4):
		
		di = {}
		
		# The x value labels and corresponding data needs to be filled here
		# NOTE: Ensure the ylabel is set correctly.

		di['x'] = [ '{}x'.format(i) for i in range(1,11) ] 
		di['y{}'.format(i+1)] = np.random.randn(10)+range(10*(i-1)+1,10*(i)+1)
		
		di['xlabel'] = 'x'
		di['ylabel'] = 'y{}'.format(i+1)

		# Set the color schema, linestyle, and label
		di['color'] = 'blue' if i%2 else 'red'
		di['linestyle'] = 'solid' if i < 2 else 'dashed'
		di['label'] = di['ylabel']

		data.append(di)

	return data

def plot_line_chart(data, params):
	
	# multiple line plot
	
	for di in data:
		plt.plot( di['xlabel'], di['ylabel'], data=di, color=di['color'], linestyle=di['linestyle'], label=di['label'])

	# Parameterize the xlabel if needed
	plt.xlabel("Ratio of Unsupervised Data to Supervised Data", fontsize='large')
	plt.ylabel(params['metric'], fontsize='large')
	plt.legend()
	plt.tight_layout()
	plt.savefig(params['out'], format='eps')
	plt.close()

	return

if __name__ == "__main__":

	# Parse the arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--out', default="/home/marauder/ut/nlp_cs388/final_proj/line_chart.eps", help="Path of output plot")
	parser.add_argument('--metric', default="BLEU Score", help="Name of the metric to show in the plot")
	params = vars(parser.parse_args())
	
	# Write the data fetching logic in this function
	data = get_data()
	plot_line_chart(data, params)