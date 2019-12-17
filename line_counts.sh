#!/bin/bash

echo -e "language\tlines"
for l in `ls working`; do 
  if [ $l != "index" ]; then
    echo "Counting for $l" >> /dev/stderr
    count=`cat working/$l/split/* | LC_ALL=C sort -u | wc -l`
    echo -e "$l\t$count"
  fi
done
