#!/bin/bash

# Extract all arguments 
ORG_DATA_DIR=$1
BASE_DIR=$2
ANNOT_PPCT=$3
ANNOT_UPPCT=$4
MINED_PPCT=$5
MINED_UPPCT=$6

CONFIG="t_${ANNOT_PPCT}_${ANNOT_UPPCT}_m_${MINED_PPCT}_${MINED_UPPCT}"

DATA_PATH=$2/$CONFIG/data

set -e

CODES=600      # number of BPE codes
FULL="full"

# main paths
UMT_PATH=$PWD
TOOLS_PATH=$PWD/tools

# fastBPE
FASTBPE_DIR=$TOOLS_PATH/fastBPE
FASTBPE=$FASTBPE_DIR/fast

# fastText
FASTTEXT_DIR=$TOOLS_PATH/fastText
FASTTEXT=${FASTTEXT_DIR}/fasttext

# files full paths
SRC_BPE_CODES=$DATA_PATH/src.bpe
TGT_BPE_CODES=$DATA_PATH/tgt.bpe
FULL_BPE_CODES=$DATA_PATH/full.bpe

MONO_SRC=$DATA_PATH/mono.x
PARA_SRC=$DATA_PATH/para.x
FULL_SRC=$DATA_PATH/merged.x

MONO_TGT=$DATA_PATH/mono.y
PARA_TGT=$DATA_PATH/para.y
FULL_TGT=$DATA_PATH/merged.y

SRC_DEV=$ORG_DATA_DIR/conala-dev.x
TGT_DEV=$ORG_DATA_DIR/conala-dev.y
SRC_TEST=$ORG_DATA_DIR/conala-test.x
TGT_TEST=$ORG_DATA_DIR/conala-test.y

SRC_DEV_BPE=$DATA_PATH/conala-dev.x.$CODES
TGT_DEV_BPE=$DATA_PATH/conala-dev.y.$CODES
SRC_TEST_BPE=$DATA_PATH/conala-test.x.$CODES
TGT_TEST_BPE=$DATA_PATH/conala-test.y.$CODES

FULL_SRC_DEV_BPE=$DATA_PATH/conala-dev.x.$CODES.$FULL
FULL_TGT_DEV_BPE=$DATA_PATH/conala-dev.y.$CODES.$FULL
FULL_SRC_TEST_BPE=$DATA_PATH/conala-test.x.$CODES.$FULL
FULL_TGT_TEST_BPE=$DATA_PATH/conala-test.y.$CODES.$FULL

SRC_VOCAB=$DATA_PATH/vocab.x.$CODES
TGT_VOCAB=$DATA_PATH/vocab.y.$CODES
FULL_VOCAB=$DATA_PATH/vocab.z.$CODES

CONCAT_BPE=$DATA_PATH/"concat".$CODES.$FULL

# Delete all .pth files
rm -f $DATA_PATH/*.pth

# Create the data splits
python3 splitter.py --data-dir $ORG_DATA_DIR --out-dir $BASE_DIR --name $CONFIG --file-info "conala-trainnodev,$ANNOT_PPCT,$ANNOT_UPPCT,conala-mined,$MINED_PPCT,$MINED_UPPCT"

# Create a merged file for easier operations for full vocab
cat $MONO_SRC $PARA_SRC > $FULL_SRC
cat $MONO_TGT $PARA_TGT > $FULL_TGT

echo "Learning BPE codes..."
$FASTBPE learnbpe $CODES $MONO_SRC $PARA_SRC > $SRC_BPE_CODES
$FASTBPE learnbpe $CODES $MONO_TGT $PARA_TGT > $TGT_BPE_CODES
# Learning Common BPE
$FASTBPE learnbpe $CODES $FULL_SRC $FULL_TGT > $FULL_BPE_CODES
echo "BPE learned in $BPE_CODES"

# # apply BPE codes
echo "Applying BPE codes..."
if [[ -s $MONO_SRC ]]; then
	$FASTBPE applybpe $MONO_SRC.$CODES $MONO_SRC $SRC_BPE_CODES;
	$FASTBPE applybpe $MONO_SRC.$CODES.$FULL $MONO_SRC $FULL_BPE_CODES;
else
	touch $MONO_SRC.$CODES
	touch $MONO_SRC.$CODES.$FULL
fi

$FASTBPE applybpe $PARA_SRC.$CODES $PARA_SRC $SRC_BPE_CODES
$FASTBPE applybpe $SRC_DEV_BPE $SRC_DEV $SRC_BPE_CODES
$FASTBPE applybpe $SRC_TEST_BPE $SRC_TEST $SRC_BPE_CODES

$FASTBPE applybpe $PARA_SRC.$CODES.$FULL $PARA_SRC $FULL_BPE_CODES
$FASTBPE applybpe $FULL_SRC_DEV_BPE $SRC_DEV $FULL_BPE_CODES
$FASTBPE applybpe $FULL_SRC_TEST_BPE $SRC_TEST $FULL_BPE_CODES

echo "BPE codes applied to SRC"

if [[ -s $MONO_TGT ]]; then
	$FASTBPE applybpe $MONO_TGT.$CODES $MONO_TGT $TGT_BPE_CODES
	$FASTBPE applybpe $MONO_TGT.$CODES.$FULL $MONO_TGT $FULL_BPE_CODES
else
	touch $MONO_TGT.$CODES
	touch $MONO_TGT.$CODES.$FULL
fi
$FASTBPE applybpe $PARA_TGT.$CODES $PARA_TGT $TGT_BPE_CODES
$FASTBPE applybpe $TGT_DEV_BPE $TGT_DEV $TGT_BPE_CODES
$FASTBPE applybpe $TGT_TEST_BPE $TGT_TEST $TGT_BPE_CODES

$FASTBPE applybpe $PARA_TGT.$CODES.$FULL $PARA_TGT $FULL_BPE_CODES
$FASTBPE applybpe $FULL_TGT_DEV_BPE $TGT_DEV $FULL_BPE_CODES
$FASTBPE applybpe $FULL_TGT_TEST_BPE $TGT_TEST $FULL_BPE_CODES
echo "BPE codes applied to TGT"

$FASTBPE applybpe $FULL_SRC.$CODES.$FULL $FULL_SRC $FULL_BPE_CODES
$FASTBPE applybpe $FULL_TGT.$CODES.$FULL $FULL_TGT $FULL_BPE_CODES

# # extract vocabulary
echo "Extracting vocabulary..."
if [[ -s $MONO_TGT ]]; then
	$FASTBPE getvocab $MONO_SRC.$CODES $PARA_SRC.$CODES > $SRC_VOCAB
	$FASTBPE getvocab $MONO_TGT.$CODES $PARA_TGT.$CODES > $TGT_VOCAB
else
	$FASTBPE getvocab $PARA_SRC.$CODES > $SRC_VOCAB
	$FASTBPE getvocab $PARA_TGT.$CODES > $TGT_VOCAB
fi

$FASTBPE getvocab $FULL_SRC.$CODES.$FULL $FULL_TGT.$CODES.$FULL > $FULL_VOCAB

ln -sf $SRC_DEV $DATA_PATH
ln -sf $TGT_DEV $DATA_PATH
ln -sf $SRC_TEST $DATA_PATH
ln -sf $TGT_TEST $DATA_PATH

python3 preprocess.py --data-dir $DATA_PATH --out-dir $BASE_DIR --name $CONFIG --dev conala-dev --test conala-test --use_bpe --bpe_codes $CODES --use_full
python3 preprocess.py --data-dir $DATA_PATH --out-dir $BASE_DIR --name $CONFIG --dev conala-dev --test conala-test

cat $FULL_SRC.$CODES.$FULL $FULL_TGT.$CODES.$FULL | shuf > $CONCAT_BPE
$FASTTEXT skipgram -epoch 10 -minCount 0 -dim 512 -thread 10 -ws 5 -neg 10 -input $CONCAT_BPE -output $CONCAT_BPE