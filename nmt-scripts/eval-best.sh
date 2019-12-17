#!/bin/bash

gpus=$1
shift

for model in ${@}; do
    echo $model
    echo "Evaluating best translation model in $model" 1>&2

    source $model/scripts/vars

   test -s $model/dev.out || cat $working_dir/dev.bpe.$src \
       | $marian_bin/marian-decoder -c $model/model.npz.best-translation.npz.decoder.yml -d $gpus --quiet \
       | perl -pe 's/@@ //g' \
       | $moses_scripts/recaser/detruecase.perl \
       | $moses_scripts/tokenizer/detokenizer.perl -q -l en > $model/dev.out

    $moses_scripts/generic/multi-bleu.perl -lc $working_dir/dev.tok.$tgt < $model/dev.out > $model/dev.bleu
    bleu_dev=$(cat $model/dev.bleu | sed -r 's/BLEU = ([0-9.]+),.*/\1/')

    test -s $model/test.out || cat $working_dir/test.bpe.$src \
        | $marian_bin/marian-decoder -c $model/model.npz.best-translation.npz.decoder.yml -d $gpus --quiet \
        | perl -pe 's/@@ //g' \
        | $moses_scripts/recaser/detruecase.perl \
        | $moses_scripts/tokenizer/detokenizer.perl -q -l en 2>/dev/null > $model/test.out

    $moses_scripts/generic/multi-bleu.perl -lc $working_dir/test.tok.$tgt < $model/test.out > $model/test.bleu
    bleu_test=$(cat $model/test.bleu | sed -r 's/BLEU = ([0-9.]+),.*/\1/')

    echo "dev= $bleu_dev test= $bleu_test"
done
