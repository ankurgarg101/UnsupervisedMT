#!/bin/bash

# Extract all arguments 
ORG_DATA_DIR=$1
BASE_DIR=$2
USE_BPE=$3

ANNOT_PPCT=$4
ANNOT_UPPCT=$5
MINED_PPCT=$6
MINED_UPPCT=$7
CONFIG="t_${ANNOT_PPCT}_${ANNOT_UPPCT}_m_${MINED_PPCT}_${MINED_UPPCT}"

DATA_PATH=$2/$CONFIG/data

set -e

CODES=600      # number of BPE codes

# main paths
UMT_PATH=$PWD
TOOLS_PATH=$PWD/tools

# fastBPE
FASTBPE_DIR=$TOOLS_PATH/fastBPE
FASTBPE=$FASTBPE_DIR/fast

# files full paths
SRC_BPE_CODES=$DATA_PATH/src.bpe
TGT_BPE_CODES=$DATA_PATH/tgt.bpe

MONO_SRC=$DATA_PATH/mono.x
PARA_SRC=$DATA_PATH/para.x

MONO_TGT=$DATA_PATH/mono.y
PARA_TGT=$DATA_PATH/para.y

SRC_DEV=$ORG_DATA_DIR/conala-dev.x
TGT_DEV=$ORG_DATA_DIR/conala-dev.y
SRC_TEST=$ORG_DATA_DIR/conala-test.x
TGT_TEST=$ORG_DATA_DIR/conala-test.y

SRC_VOCAB=$DATA_PATH/vocab.x.$CODES
TGT_VOCAB=$DATA_PATH/vocab.y.$CODES

# Delete all .pth files
rm -f $DATA_PATH/*.pth

# Create the data splits
python3 splitter.py --data-dir $ORG_DATA_DIR --out-dir $BASE_DIR --name $CONFIG --file-info "conala-trainnodev,$ANNOT_PPCT,$ANNOT_UPPCT,conala-mined,$MINED_PPCT,$MINED_UPPCT"

if [ $USE_BPE -eq 1 ]; then
	echo "Learning BPE codes..."
	$FASTBPE learnbpe $CODES $MONO_SRC $PARA_SRC > $SRC_BPE_CODES
	$FASTBPE learnbpe $CODES $MONO_TGT $PARA_TGT > $TGT_BPE_CODES
	echo "BPE learned in $BPE_CODES"

	# # apply BPE codes
	echo "Applying BPE codes..."
	if [[ -s $MONO_SRC ]]; then
		$FASTBPE applybpe $MONO_SRC.$CODES $MONO_SRC $SRC_BPE_CODES;
	else
		touch $MONO_SRC.$CODES
	fi
	$FASTBPE applybpe $PARA_SRC.$CODES $PARA_SRC $SRC_BPE_CODES
	$FASTBPE applybpe $SRC_DEV.$CODES $SRC_DEV $SRC_BPE_CODES
	$FASTBPE applybpe $SRC_TEST.$CODES $SRC_TEST $SRC_BPE_CODES
	echo "BPE codes applied to SRC"

	if [[ -s $MONO_TGT ]]; then
		$FASTBPE applybpe $MONO_TGT.$CODES $MONO_TGT $TGT_BPE_CODES
	else
		touch $MONO_TGT.$CODES
	fi
	$FASTBPE applybpe $PARA_TGT.$CODES $PARA_TGT $TGT_BPE_CODES
	$FASTBPE applybpe $TGT_DEV.$CODES $TGT_DEV $TGT_BPE_CODES
	$FASTBPE applybpe $TGT_TEST.$CODES $TGT_TEST $TGT_BPE_CODES
	echo "BPE codes applied to TGT"

	# # extract vocabulary
	echo "Extracting vocabulary..."
	if [[ -s $MONO_TGT ]]; then
		$FASTBPE getvocab $MONO_SRC.$CODES $PARA_SRC.$CODES > $SRC_VOCAB
		$FASTBPE getvocab $MONO_TGT.$CODES $PARA_TGT.$CODES > $TGT_VOCAB
	else
		$FASTBPE getvocab $PARA_SRC.$CODES > $SRC_VOCAB
		$FASTBPE getvocab $PARA_TGT.$CODES > $TGT_VOCAB
	fi

	python3 preprocess.py --data-dir $ORG_DATA_DIR --out-dir $BASE_DIR --name $CONFIG --dev conala-dev --test conala-test --use_bpe --bpe_codes $CODES
else
	python3 preprocess.py --data-dir $ORG_DATA_DIR --out-dir $BASE_DIR --name $CONFIG --dev conala-dev --test conala-test
fi
