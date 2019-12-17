#!/bin/bash


. `dirname $0`/vars

# train
$marian_bin/marian \
    -d $devices \
    -c $working_dir/scripts/config.yml \
    -m $working_dir/model.npz \
    --mini-batch-fit -w 5000  --mini-batch 1000 --maxi-batch 1000 \
    --train-sets $working_dir/train.bpe.$src $working_dir/train.bpe.$tgt \
    --vocabs $working_dir/vocab.$src.yml $working_dir/vocab.$tgt.yml \
    --valid-sets $working_dir/dev.bpe.$src $working_dir/dev.bpe.$tgt \
    --valid-script-path $working_dir/scripts/validate.sh \
    --valid-log $working_dir/logs/valid.log \
    --log $working_dir/logs//train.log \
    --sqlite


test -e $working_dir/model.npz || exit 1

# eval best
bash $working_dir/scripts/eval-best.sh "$devices" $working_dir > $working_dir/logs/eval.log
