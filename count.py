#!/usr/bin/env python

import logging
import glob
import os.path

LOG = logging.getLogger(__name__)

def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
  root_dir = "working"
  for lang_dir in glob.glob(root_dir + "/*"):
    LOG.info("Examining directory " + lang_dir)
    base,lang = os.path.split(lang_dir)
    count = 0
    for html_file in glob.glob(lang_dir + "/html/*"):
      if lang_dir.endswith("en") or "%" in html_file:
        count += 1
    print(lang,count) 


if __name__ == "__main__":
  main()
