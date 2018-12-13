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
python3 main.py --exp_name $CONFIG --exp_id "results${BPE}" --dump_path $BASE_DIR --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb False --share_output_emb False --langs 'x,y' --n_mono -1  --mono_dataset "x:${BASE_DIR}/${CONFIG}/data/para.x${BPE}.pth,,;y:${BASE_DIR}/${CONFIG}/data/para.y${BPE}.pth,," --n_para -1 --para_dataset "x-y:${BASE_DIR}/${CONFIG}/data/para.XX${BPE}.pth,${BASE_DIR}/${CONFIG}/data/conala-dev.XX${BPE}.pth,${BASE_DIR}/${CONFIG}/data/conala-test.XX${BPE}.pth" --para_directions 'x-y,y-x' --pivo_directions 'x-y-x,y-x-y' --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --lambda_dis 0.1 --n_dis 2 --otf_num_processes 10 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size -1 --stopping_criterion bleu_x_y_valid,25 --cudnn_enabled $USE_CUDNN --batch_size $BATCH_SIZE  --max_epoch $EPOCH
else
	python3 main.py --exp_name $CONFIG --exp_id "results${BPE}" --dump_path $BASE_DIR --transformer True --n_enc_layers 4 --n_dec_layers 4 --share_enc 3 --share_dec 3 --share_lang_emb False --share_output_emb False --langs 'x,y' --n_mono -1  --mono_dataset "x:${BASE_DIR}/${CONFIG}/data/mono.x${BPE}.pth,,;y:${BASE_DIR}/${CONFIG}/data/mono.y${BPE}.pth,," --n_para -1 --para_dataset "x-y:${BASE_DIR}/${CONFIG}/data/para.XX${BPE}.pth,${BASE_DIR}/${CONFIG}/data/conala-dev.XX${BPE}.pth,${BASE_DIR}/${CONFIG}/data/conala-test.XX${BPE}.pth" --para_directions 'x-y,y-x' --pivo_directions 'x-y-x,y-x-y' --mono_directions 'x,y' --word_shuffle 3 --word_dropout 0.1 --word_blank 0.2   --lambda_xe_mono '0:1,100000:0.1,300000:0'  --lambda_xe_para '0:1,100000:0.1,300000:0'  --lambda_xe_otfd 1 --lambda_dis 0.1 --n_dis 2 --otf_num_processes 10 --otf_sync_params_every 1000 --enc_optimizer adam,lr=0.0001 --epoch_size -1 --stopping_criterion bleu_x_y_valid,25 --cudnn_enabled $USE_CUDNN --batch_size $BATCH_SIZE  --max_epoch $EPOCH
fi
