#!/usr/bin/env python3

#
# Convert vecalign output to tsv file
#

import argparse
import sys

def get_indexes(index_str):
  index_str = index_str[1:-1]
  if index_str == "":
    return []
  indexes = index_str.split(",")
  return [int(i.strip()) for i in indexes]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--source-file", required=True)
  parser.add_argument("-t", "--target-file", required=True)
  parser.add_argument("-a", "--align-file", required=True)
  args = parser.parse_args()

  aligns_nm = 0
  aligns_11 = 0 
  with open(args.source_file) as sfh,\
    open(args.target_file) as tfh,\
    open(args.align_file) as afh:
    slines = sfh.readlines()
    tlines = tfh.readlines()
    for aline in afh:
      sindex,tindex,score = aline[:-1].split(":")
      sindex = get_indexes(sindex)
      tindex = get_indexes(tindex)
      if len(sindex) != 1 or len(tindex) !=1:
        aligns_nm += 1
        continue
      print("{}\t{}".format(slines[sindex[0]][:-1], tlines[tindex[0]][:-1]))
      aligns_11 += 1
    print("Alignments: 1-1 {}; n-m {}".format(aligns_11, aligns_nm), file=sys.stderr)

if __name__ == "__main__":
  main()

