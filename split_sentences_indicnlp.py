#!/usr/bin/env python3

import argparse
import logging
import os
import os.path
import sys

from indicnlp.tokenize import sentence_tokenize

LOG = logging.getLogger(__name__)

class IndicNLPSplitter:
  def __init__(self, language):
    self.language = language

  def split(self, line):
    lines = sentence_tokenize.sentence_split(line, self.language)
    return lines


def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
  parser = argparse.ArgumentParser()
  parser.add_argument("-l", "--language", required=True)
  args = parser.parse_args()

  splitter = IndicNLPSplitter(args.language)
  for line in sys.stdin:
    lines = splitter.split(line)
    for split_line in lines:
      print(split_line)


if __name__ == "__main__":
  main()
