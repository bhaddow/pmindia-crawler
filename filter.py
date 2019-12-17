#!/usr/bin/env python3

#
# Final filtering of the tsv file
#
import argparse
import pycld2
import sys


def check_language(line,expected):
  # Manipuri unsupported by cld2, but normally detected as Bengali
  if expected == "mni" : expected = "bn"
  try:
    _,_,details = pycld2.detect(line, hintLanguage=expected)
    if expected != details[0][1]:
      print("WRONG {} != {} {}".format(details[0][1], expected, line), file=sys.stderr)
    return expected == details[0][1]
  except pycld2.error:
    print("pycld2.error",file=sys.stderr)
    return False



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--flang", default="hi")
  args = parser.parse_args()

  total = 0
  wrong_lang = 0

  for line in sys.stdin:
    #print("LINE {} {}".format(total, line))
    fields  = line[:-1].split("\t")
    en,fr = fields[0],fields[1]
    total += 1
    if not check_language(fr, args.flang) or not check_language(en,"en"):
      wrong_lang += 1
      continue
    print("{}\t{}".format(en,fr))


  print("Total: {}; Retained: {}, Wrong language: {}".format(total, total - wrong_lang, wrong_lang), file=sys.stderr)

if __name__ == "__main__":
  main()
