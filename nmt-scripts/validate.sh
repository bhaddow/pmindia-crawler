#!/bin/bash

. `dirname $0`/vars

cat $1 | tee $working_dir/dev.bpe.in \
    | perl -pe 's/@@ //g' 2>/dev/null \
    | $moses_scripts/recaser/detruecase.perl 2>/dev/null \
    | $moses_scripts/tokenizer/detokenizer.perl -q -l $tgt 2>/dev/null > $working_dir/dev.out

$moses_scripts/generic/multi-bleu.perl -lc $working_dir/dev.tok.$tgt < $working_dir/dev.out 2>/dev/null | sed -r 's/BLEU = ([0-9.]+),.*/\1/'
