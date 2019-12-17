#!/usr/bin/env python3

#
# Extract text from html
#

import alcazar.bodytext
import argparse
import glob
import logging
import os
import os.path
import sys
import time

from bs4 import BeautifulSoup, UnicodeDammit
from make_index import get_lang_url

LOG = logging.getLogger(__name__)

def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--from-dir", required=True)
  parser.add_argument("-t", "--to-dir", required=True)
  parser.add_argument("-i", "--index-file", required=True)
  args = parser.parse_args()

  if not os.path.exists(args.from_dir):
    LOG.error("Does not exist: " + args.from_dir)
    sys.exit(1)


  if not os.path.exists(args.to_dir):
    os.makedirs(args.to_dir)

  lang = os.path.basename(os.path.dirname(args.from_dir))

  enurl_to_name = {}
  with open(args.index_file) as ifh:
    for line in ifh:
      name, enurl = line[:-1].split()
      enurl_to_name[enurl] = name

  for html_file in glob.glob(args.from_dir + "/*"):
    if not lang == "en" and not "%" in html_file:
      continue

    LOG.info("Reading html from {}".format(html_file))
    html = open(html_file, "rb").read()
    dammit = UnicodeDammit(html)
    soup = BeautifulSoup(dammit.unicode_markup, "html.parser")
    tweets = soup.find_all("blockquote", attrs={"class": "twitter-tweet"})
    for t in tweets:
      t.clear()
    btext = alcazar.bodytext.parse_article(dammit.unicode_markup)
    btext = alcazar.bodytext.parse_article(str(soup))
    if btext.body_text:
      enurl = get_lang_url(dammit.unicode_markup, "en")
      if not enurl in enurl_to_name:
        LOG.warn("Could not identify link to en article in " + html_file)
        continue
      out_file = "{}/{}.txt".format(args.to_dir, enurl_to_name[enurl])
      LOG.info("Writing text to {}".format(out_file))
      with open(out_file, "w") as ofh:
        print(btext.body_text, file=ofh, end="")


  


if __name__ == "__main__":
  main()
