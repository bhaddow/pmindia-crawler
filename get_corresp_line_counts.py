#!/usr/bin/env python3

#
# Compare line counts of indic languages with English, in sentence split files
#

import argparse
import glob
import logging
import os
import os.path
import sys


LOG = logging.getLogger(__name__)
LANGS = ["hi", "gu"]

def get_length(filename):
  count = 0
  with open(filename) as fh:
    for line in fh:
      count += 1
  return count
    

def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
  parser = argparse.ArgumentParser()
  args = parser.parse_args()

  print("\t".join(("language", "name", "length", "en_length", "diff")))

  # Lengths of English articles
  en_lens = {}
  for en_file in glob.glob("working/en/split/*"):
    name = os.path.basename(en_file)
    length = get_length(en_file)
    en_lens[name] = length

  for lang in LANGS:
    LOG.info("Counting lines in all {} files".format(lang))
    for in_file in glob.glob("working/{}/split/*".format(lang)):
      name = os.path.basename(in_file)
      if not name in en_lens:
        continue
      length = get_length(in_file)
      print ("{}\t{}\t{}\t{}\t{}".format(lang, name, en_lens[name], length, en_lens[name] - length))


if __name__ == "__main__":
  main()
