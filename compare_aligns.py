#!/usr/bin/env python3

#
# Compare two different alignment methods
#

import argparse
import glob
import logging
import os
import os.path
import sys


LOG = logging.getLogger(__name__)

def get_pairs(tsv_file):
  pairs = []
  with open(tsv_file) as tfh:
    for line in tfh:
      fields = line[:-1].split("\t")
      if fields[0] and fields[1]:
        pairs.append((fields[0], fields[1]))
  return pairs

def get_prf(tp, fp, fn):
  if tp + fp:
    p = float(tp) / (tp + fp)
  else:
    p = 0.0
  if tp + fn:
    r = float(tp) / (tp + fn)
  else:
    r = 0.0
  if (tp + fp + fn):
    f1 = 2*float(tp) / (2*tp + fp + fn)
  else:
    f1 = 0
  return (p,r,f1)

def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
  parser = argparse.ArgumentParser()
  parser.add_argument("-l", "--language", required=True)
  args = parser.parse_args()

  # Take vecalign as the gold, hunalign as the hypothesis, but this should be configurable.
  gold_file = "working/corpus/align.vecalign.filtered.{}-en.tsv".format(args.language)
  hypo_file = "working/corpus/align.hunalign.filtered.{0}-en.tsv".format(args.language)

  gold_pairs = set(get_pairs(gold_file))
  hypo_pairs = set(get_pairs(hypo_file))
  LOG.info("Unique Gold pairs: {}; Unique Hypo pairs: {}".format(len(gold_pairs), len(hypo_pairs)))
  tp = len(gold_pairs.intersection(hypo_pairs))
  fp = len(hypo_pairs.difference(gold_pairs))
  fn = len(gold_pairs.difference(hypo_pairs))
  p,r,f1 = get_prf(tp,fp,fn)
  print("tp = {}; p = {:.2f}; r = {:.2f}; f1 = {:.2f}".format(tp, p, r, f1))

  LOG.debug("Processing individual aligned files (unfiltered)")
  if not os.path.exists("compare_aligns"):
    os.makedirs("compare_aligns")
  gold = "vecaligned"
  hypo = "hunaligned"
  tsv_file = "compare_aligns/{}-{}-{}.tsv".format(args.language, gold, hypo)
  with open(tsv_file, "w") as tfh:
    print("file\ttp\tfp\tfn\tp\tr\tf1", file=tfh)
    gold_dir = "working/{}/{}".format(args.language, gold)
    hypo_dir = "working/{}/{}".format(args.language, hypo)
    for gold_file in glob.glob(gold_dir + "/*tsv"):
      hypo_file = hypo_dir + "/" + os.path.basename(gold_file)

      gold_pairs = set(get_pairs(gold_file))
      hypo_pairs = set(get_pairs(hypo_file))
      
      tp = len(gold_pairs.intersection(hypo_pairs))
      fp = len(hypo_pairs.difference(gold_pairs))
      fn = len(gold_pairs.difference(hypo_pairs))
      p,r,f1 = get_prf(tp, fp, fn)
      filename = os.path.basename(gold_file)
      print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(filename, tp, fp, fn, p, r, f1), file=tfh)

if __name__ == "__main__":
  main()
