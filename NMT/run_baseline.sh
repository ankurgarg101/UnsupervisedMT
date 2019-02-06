#!/bin/bash

# Extract all arguments 
BASE_DIR=$1
ANNOT_PPCT=$2
ANNOT_UPPCT=$3
MINED_PPCT=$4
MINED_UPPCT=$5
BATCH_SIZE=$6
EPOCH=$7
USE_BPE=$8
USE_CUDNN=$9
USE_AUX=${10}

CONFIG="t_${ANNOT_PPCT}_${ANNOT_UPPCT}_m_${MINED_PPCT}_${MINED_UPPCT}"
DATA_PATH=$2/$CONFIG/data

set -e

CODES=600      # number of BPE codes

# main paths
UMT_PATH=$PWD
TOOLS_PATH=$PWD/tools

if [ $USE_BPE -eq 1 ]; then
	BPE=".${CODES}"
else
	BPE=""
fi

if [ $ANNOT_UPPCT -eq 0 -a $MINED_UPPCT -eq 0 ]; then
	echo "IN"
	python3 main.py --exp_name $CONFIG --exp_id "results_baseline_${USE_AUX}${BPE}" --dump_path $BASE_DIR --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb True --share_output_emb True --langs 'x,y' --n_mono -1  --mono_dataset "x:${BASE_DIR}/${CONFIG}/data/para.x${BPE}.full.pth,,;y:${BASE_DIR}/${CONFIG}/data/para.y${BPE}.full.pth,," --n_para -1 --para_dataset "x-y:${BASE_DIR}/${CONFIG}/data/para.XX${BPE}.full.pth,${BASE_DIR}/${CONFIG}/data/conala-dev.XX${BPE}.full.pth,${BASE_DIR}/${CONFIG}/data/conala-test.XX${BPE}.full.pth" --para_directions 'x-y,y-x' --pivo_directions 'x-y-x,y-x-y' --pretrained_emb '${BASE_DIR}/${CONFIG}/data/concat${BPE}.full.vec'  --pretrained_out True --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --lambda_lm 0 --lambda_dis 1 --n_dis 1 --dis_hidden_dim 1024 --dis_smooth 0.1 --otf_num_processes 10 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.00001 --epoch_size -1 --stopping_criterion bleu_x_y_valid,25 --cudnn_enabled $USE_CUDNN --batch_size 32  --max_epoch $EPOCH --dis_aux 0
else
	echo "OUT"
	python3 main.py --exp_name $CONFIG --exp_id "results_baseline_${USE_AUX}${BPE}" --dump_path $BASE_DIR --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb True --share_output_emb True --langs 'x,y' --n_mono -1  --mono_dataset "x:${BASE_DIR}/${CONFIG}/data/mono.x${BPE}.full.pth,,;y:${BASE_DIR}/${CONFIG}/data/mono.y${BPE}.full.pth,," --n_para -1 --para_dataset "x-y:${BASE_DIR}/${CONFIG}/data/para.XX${BPE}.full.pth,${BASE_DIR}/${CONFIG}/data/conala-dev.XX${BPE}.full.pth,${BASE_DIR}/${CONFIG}/data/conala-test.XX${BPE}.full.pth" --para_directions 'x-y,y-x' --pivo_directions 'x-y-x,y-x-y' --mono_directions 'x,y' --word_shuffle 3 --word_dropout 0.1 --word_blank 0.2  --pretrained_emb '${BASE_DIR}/${CONFIG}/data/concat${BPE}.full.vec' --pretrained_out True --lambda_xe_mono '0:1,100000:0.1,300000:0'  --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --lambda_lm 0 --lambda_dis 1 --n_dis 1 --dis_hidden_dim 1024 --dis_smooth 0.1 --otf_num_processes 10 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.00001 --epoch_size -1 --stopping_criterion bleu_x_y_valid,25 --cudnn_enabled $USE_CUDNN --batch_size 32  --max_epoch $EPOCH --dis_aux 0
fi


# Remember to lower case everything before applying bpe and fasttext
# Fast text embedding dimension should be 512, with window size of 5 and 10 neg samples
