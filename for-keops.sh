#!/bin/bash

mkdir -p working/for-keops
SENTS=100

for segment in onlyhunalign onlyvecalign intersect; do
  shuf working/corpus/align.$segment.ta-en.tsv > working/for-keops/$segment.ta-en.tsv
  head -n $SENTS  working/for-keops/$segment.ta-en.tsv >  working/for-keops/$segment.selected.ta-en.tsv
done

cd working
tar czvf for-keops.tgz for-keops/*select*
cd ..
