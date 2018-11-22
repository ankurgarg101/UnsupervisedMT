"""
Module that is used as an interface by other external modules to load the dataset
"""

from os import path
import numpy as np
import os

def fetch_raw(params):

	"""
	Functions that fetches the raw data from all the files mentioned in the file_info list
	"""

	paired = []
	unpaired_x = []
	unpaired_y = []
	
	data_dir = params['data_dir']
	file_info = params['file_info'].split(',')
	
	assert len(file_info) % 3 == 0

	idx = 0
	while (idx < len(file_info)):

		# Compute the number of samples to be selected for each split
		# NOTE: Currently, assuming that the corresponding paired samples will go in unpaired_x and unpaired_y.
		file_name, paired_pct, unpaired_pct = file_info[idx], float(file_info[idx+1]), float(file_info[idx+2])
		idx += 3
		with open(path.join(data_dir, '{}.intent'.format(file_name)), 'r') as data_file:

			intent_data = [ l.strip('\n\r') for l in data_file.readlines() ]

		with open(path.join(data_dir, '{}.snippet'.format(file_name)), 'r') as data_file:

			snippet_data = [ l.strip('\n\r') for l in data_file.readlines() ]

		assert len(intent_data) == len(snippet_data)

		data_sz = len(intent_data)

		paired_sz = int(paired_pct*data_sz/100.0)
		unpaired_sz = int(unpaired_pct*data_sz/100.0)

		# Generate a random permutation of the dataset.
		permutation = np.random.permutation(data_sz)

		paired += [ [intent_data[idx], snippet_data[idx]] for idx in permutation[:paired_sz] ]
		unpaired_x += [ intent_data[idx] for idx in permutation[paired_sz:paired_sz+unpaired_sz] ]
		unpaired_y += [ snippet_data[idx] for idx in permutation[paired_sz:paired_sz+unpaired_sz] ]

	return paired, unpaired_x, unpaired_y

def get_word_sets(paired, unpaired_x, unpaired_y):

	xset = {}
	yset = {}

	for pd in paired:

		for xwrd in pd[0].split():

			if xwrd not in xset:
				xset[xwrd] = 0
			
			xset[xwrd] += 1

		for ywrd in pd[1].split():

			if ywrd not in yset:
				yset[ywrd] = 0
			
			yset[ywrd] += 1

	for up_x in unpaired_x:
		for xwrd in up_x.split():

			if xwrd not in xset:
				xset[xwrd] = 0
			
			xset[xwrd] += 1

	for up_y in unpaired_y:
		for ywrd in up_y.split():

			if ywrd not in yset:
				yset[ywrd] = 0
			
			yset[ywrd] += 1

	return xset, yset

def dump_indexer(wset, vocab_path):

	with open(vocab_path, 'w') as vf:

		for wrd in wset:
			print(wrd + ' ' + str(wset[wrd]), file=vf)

def dump_paired(dataset, paired_path):

	with open(paired_path.format('x'), 'w') as xf, open(paired_path.format('y'), 'w') as yf:
		for d in dataset:
			print(d[0], file=xf)
			print(d[1], file=yf)

def dump_unpaired(unpaired_dataset, unpaired_path):

	with open(unpaired_path, 'w') as uf:
		for d in unpaired_dataset:
			print(d, file=uf) 

def create_data_splits(params):

	"""
	@param params: Parameters needed for creating the splits. Must contain file_info key that has the List of file names with split percentages for paired and unpaired dataset. [(f1, p1, up1), (f2, p2, up2), ..]. p_i is percentage b/w 0-100.
	@return None
	"""

	paired, unpaired_x, unpaired_y = fetch_raw(params)

	xset, yset = get_word_sets(paired, unpaired_x, unpaired_y)
	
	out_dir = path.join(params['out_dir'], params['name'], 'data')

	if not path.exists(out_dir):
		os.makedirs(out_dir)

	vocab_path = path.join(out_dir, 'vocab.{}')
	paired_path = path.join(out_dir, 'para.{}')
	unpaired_path = path.join(out_dir, 'mono.{}')

	# Dump Files

	dump_indexer(xset, vocab_path.format('x'))
	dump_indexer(yset, vocab_path.format('y'))

	dump_paired(paired, paired_path)
	dump_unpaired(unpaired_x, unpaired_path.format('x'))
	dump_unpaired(unpaired_y, unpaired_path.format('y'))