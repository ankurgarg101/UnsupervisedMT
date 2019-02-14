" Module that specifies the Model for a discriminator that uses sequential data "

import torch
import torch.nn as nn
import torch.nn.functional as F

from ..modules.layer_norm import LayerNorm
from ..modules.multihead_attention import MultiheadAttention
from ..modules.sinusoidal_positional_embedding import SinusoidalPositionalEmbedding

class SeqDiscriminator(nn.Module):

	SEQ_DIS_ATTR = ['dropout', 'padding_idx', 'n_words', 'n_langs']

	def __init__(self, args):
		super().__init__()
		
		self.dropout = args.dropout
		self.n_langs = args.n_langs
		# This is a set
		self.n_words = args.n_words
		
		self.padding_idx = args.pad_index
		embed_positions = [ SeqPositionalEmbedding(	1024, n_words, self.padding_idx, left_pad=args.left_pad_source) for n_words in self.n_words]

		self.embed_positions = nn.ModuleList(embed_positions)

		self.layers = nn.ModuleList()
		for k in range(args.encoder_layers):
			# create transformer layer for each language
			self.layers[k] = nn.ModuleList()
			for i in range(0, self.n_langs):
				self.layers[k].append(SeqTransformerEncoderLayer(args, self.n_words[i]))

		self.lin_layers = nn.ModuleList()
		for i in range(0, self.n_langs):
			if args.wgan:
				self.lin_layers.append(nn.Linear(self.n_words[i], 1))
			else:
				self.lin_layers.append(nn.Linear(self.n_words[i], 2))


	def forward(self, src_tokens, src_lengths, lang_id):
		assert type(lang_id) is int

		x = src_tokens
		max_seq_len, batch_size, nw = src_tokens.size()

		dummy_src = (torch.arange(max_seq_len, dtype=torch.long).cuda().expand(batch_size, max_seq_len) < src_lengths.unsqueeze(1)) + self.padding_idx

		dummy_src = dummy_src.permute(1,0).long().cuda().detach()
		
		
		x =  torch.add(x,self.embed_positions[lang_id](dummy_src))
		
		x = F.dropout(x, p=self.dropout, training=self.training)

		# compute padding mask
		encoder_padding_mask = dummy_src.t().eq(self.padding_idx)

		# encoder layers
		for layer in self.layers:
			x = layer[lang_id](x, encoder_padding_mask)

		batch_idx = torch.arange(src_tokens.size()[1], dtype=torch.long).cuda()

		x = self.lin_layers[lang_id]( x[src_lengths-1, batch_idx, :])  # B x 2

		return x

	def max_positions(self):
		"""Maximum input length supported by the encoder."""
		return self.embed_positions.max_positions()

class SeqTransformerEncoderLayer(nn.Module):
	"""Encoder layer block.

	In the original paper each operation (multi-head attention or FFN) is
	postprocessed with: dropout -> add residual -> layernorm.
	In the tensor2tensor code they suggest that learning is more robust when
	preprocessing each layer with layernorm and postprocessing with:
	dropout -> add residual.
	We default to the approach in the paper, but the tensor2tensor approach can
	be enabled by setting `normalize_before=True`.
	"""
	def __init__(self, args, enc_dim):
		super().__init__()
		self.embed_dim = enc_dim
		self.self_attn = MultiheadAttention(
			self.embed_dim, 1,
			dropout=args.attention_dropout,
		)
		self.dropout = args.dropout
		self.relu_dropout = args.relu_dropout
		self.normalize_before = args.encoder_normalize_before
		self.fc1 = SeqLinear(self.embed_dim, args.encoder_ffn_embed_dim)
		self.fc2 = SeqLinear(args.encoder_ffn_embed_dim, self.embed_dim)
		self.layer_norms = nn.ModuleList([LayerNorm(self.embed_dim) for i in range(2)])

	def forward(self, x, encoder_padding_mask):
		residual = x
		x = self.maybe_layer_norm(0, x, before=True)
		x, _ = self.self_attn(query=x, key=x, value=x, key_padding_mask=encoder_padding_mask)
		x = F.dropout(x, p=self.dropout, training=self.training)
		x = residual + x
		x = self.maybe_layer_norm(0, x, after=True)

		residual = x
		x = self.maybe_layer_norm(1, x, before=True)
		x = F.relu(self.fc1(x))
		x = F.dropout(x, p=self.relu_dropout, training=self.training)
		x = self.fc2(x)
		x = F.dropout(x, p=self.dropout, training=self.training)
		x = residual + x
		x = self.maybe_layer_norm(1, x, after=True)
		return x

	def maybe_layer_norm(self, i, x, before=False, after=False):
		assert before ^ after
		if after ^ self.normalize_before:
			return self.layer_norms[i](x)
		else:
			return x

def SeqPositionalEmbedding(num_embeddings, embedding_dim, padding_idx, left_pad):
	m = SinusoidalPositionalEmbedding(embedding_dim, padding_idx, left_pad, init_size=num_embeddings)
	return m


def SeqLinear(in_features, out_features, bias=True):
	m = nn.Linear(in_features, out_features, bias)
	nn.init.xavier_uniform_(m.weight)
	nn.init.constant_(m.bias, 0.)
	return m