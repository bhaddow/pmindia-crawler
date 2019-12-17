#!/usr/bin/env python3

#
# Convert Pavlick's dictionary to hunalign
#

import argparse
import re

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--dict", default="/home/bhaddow/data/pavlick-dicts/dict.hi")
  args = parser.parse_args()
  brackets = re.compile("\[[^\]]*\]")
  delim = re.compile("[\t,/]")
  with open(args.dict) as ifh:
    for line in ifh:
      line  = brackets.sub("", line[:-1])
      fields = delim.split(line)
      for e in fields[1:]:
        e = e.strip()
        if e and fields[0]:
          if e == "fullstop": e = "."
          print("{} @ {}".format(fields[0],e))


if __name__ == "__main__":
  main()
