#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import sys
import argparse
from os import path

from src.logger import create_logger
from src.data.dictionary import Dictionary

def parse_args(parser):

	parser.add_argument('--data-dir', dest='data_dir', type=str, required=True, help="Data directory of input data")
	parser.add_argument('--out-dir', dest='out_dir', type=str, required=True, help="Output data directory path")
	parser.add_argument('--name', type=str, required=True, help="Name of the configuration")

	parser.add_argument('--dev', type=str, required=True, help="Name of Dev Dataset")

	parser.add_argument('--test', type=str, required=True, help="Name of Test Dataset")
	parser.add_argument('--use_bpe', default=False, action="store_true", help="Check to use BPE")
	parser.add_argument('--bpe_codes', type=int, help="No of BPE Codes")

	return vars(parser.parse_args())

def create_binary(txt_path, bin_path, dico):

	data = Dictionary.index_data(txt_path, bin_path, dico)
	logger.info("%i words (%i unique) in %i sentences." % (
		len(data['sentences']) - len(data['positions']),
		len(data['dico']),
		len(data['positions'])
	))

	if len(data['unk_words']) > 0:
		logger.info("%i unknown words (%i unique), covering %.2f%% of the data." % (
			sum(data['unk_words'].values()),
			len(data['unk_words']),
			sum(data['unk_words'].values()) * 100. / (len(data['sentences']) - len(data['positions']))
		))
		if len(data['unk_words']) < 30:
			for w, c in sorted(data['unk_words'].items(), key=lambda x: x[1])[::-1]:
				logger.info("%s: %i" % (w, c))
	else:
		logger.info("0 unknown word.")

if __name__ == '__main__':

	logger = create_logger(None)
	parser = argparse.ArgumentParser()
	params = parse_args(parser)
	print(params['out_dir'])
	langs = ['x', 'y']
	if params['use_bpe']:
		langs = [ l + '.{}'.format(params['bpe_codes']) for l in langs ]

	split = ['para', 'mono']

	for lang in langs:
		
		voc_path = path.join(params['out_dir'], params['name'], 'data', 'vocab.{}'.format(lang))

		dico = Dictionary.read_vocab(voc_path)
		logger.info("")
		assert os.path.isfile(voc_path)

		for spl in split:
			
			txt_path = path.join(params['out_dir'], params['name'], 'data', '{}.{}'.format(spl, lang))
			bin_path = txt_path + '.pth'
			assert os.path.isfile(txt_path)       

			create_binary(txt_path, bin_path, dico)


		txt_path = path.join(params['data_dir'], '{}.{}'.format(params['dev'], lang))
		bin_path = path.join(params['out_dir'], params['name'], 'data', '{}.{}'.format(params['dev'], lang))
		bin_path = bin_path + '.pth'
		assert os.path.isfile(txt_path)

		create_binary(txt_path, bin_path, dico)

		txt_path = path.join(params['data_dir'], '{}.{}'.format(params['test'], lang))
		bin_path = path.join(params['out_dir'], params['name'], 'data', '{}.{}'.format(params['test'], lang))
		bin_path = bin_path + '.pth'
		assert os.path.isfile(txt_path)

		create_binary(txt_path, bin_path, dico)