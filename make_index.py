#!/usr/bin/env python3

#
# Create a unique cross-lingual identifier for each article, but extracting 
# the links to a common language (default: English) from the html.
#

import argparse
import glob
import logging
import os
import os.path
import sys
import time

from bs4 import BeautifulSoup, UnicodeDammit

def get_lang_url(html, lang):

  soup = BeautifulSoup(html, features="lxml")

  # Look for the translated link
  lang_url = None
  for link_el in soup.find_all("link"):
    if link_el.get("hreflang") == lang:
      lang_url = link_el.get("href")
      if lang_url: return lang_url
  return None

def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--dir", default="working/en/html")
  parser.add_argument("-l", "--lang", default="en")
  args = parser.parse_args()

  for idx, html_file in enumerate(glob.glob(args.dir + "/*")):
    html = open(html_file, "rb").read()
    dammit = UnicodeDammit(html)
    lang_url = get_lang_url(dammit.unicode_markup, args.lang)
    if not lang_url:
      LOG.warn("Could not find link for lang {} in {}".format(args.lang, html_file))
    else:
      print("{}\t{}".format(os.path.basename(html_file),lang_url))


if __name__ == "__main__":
  main()
