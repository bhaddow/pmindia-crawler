#!/usr/bin/env python3

#
# Get list of news URLs from pmindia
#

import argparse
import logging
import os
import os.path
import sys
import time

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse


LOG = logging.getLogger(__name__)

def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
  parser = argparse.ArgumentParser()
  parser.add_argument("-l", "--language", required=True)
  parser.add_argument("-m", "--max-urls", type=int, default=10)
  batch_size = 10
  timeout = 300
  sleep = 10
  max_retries = 5
  args = parser.parse_args()

  LOG.info("Obtaining URLS for  " + args.language)
  lang = args.language
  # non-standard abbrevs. used by pmindia
  if lang == "or": lang = "ory"
  if lang == "as": lang = "asm"
  page = 1
  url_count = 0
  old_url_count = 0
  retries = 0
  while True:
    url = "https://www.pmindia.gov.in/wp-admin/admin-ajax.php?action=infinite_scroll&sort_type=latest%20&page_no={}&query=&loop_file=10&language={}".format(page, args.language)
    LOG.debug(url)
    req = Request(url)
    req.add_header("User-Agent" , "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
    req.add_header("Connection", "keep-alive")
    req.add_header("Accept-Encoding", "gzip")
    req.add_header("Accept", "text/html")
    #req.add_header("Cookie", "pll_language=ur; _ga=GA1.3.221623570.1552922035; kanni_user_lang=en%7Cen; PHPSESSID=k5gestr3gbd5c0gr5vek7191u1; _gid=GA1.3.404982932.1557482981")
    html = None
    try:
      html = urlopen(req, timeout=timeout).read().decode('utf8')
      retries = 0
    except :
      LOG.error("Error retrieving URL")
      retries += 1
      if retries > max_retries:
         LOG.warn("Maximum number of retries")
         break
      LOG.warn("retrying")
      time.sleep(120*retries)
      continue
       
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
      if link.parent.name == "div":
        continue
      url = link.get('href')
      if url:
        path = urlparse(url).path
        if path[1:3] == "en" and args.language != "en":
          LOG.warn("URL unexpectedly English " + url)
        url_count += 1
        if url.endswith("?comment=disable"):
          url = url[:-16]
        if url.endswith("/"):
          url = url[:-1]
        print (url)

    page += 1
    if url_count == old_url_count:
      LOG.info("No new URLs found, exiting")
      break
    else:
      old_url_count = url_count
    LOG.debug(url_count)
    if args.max_urls and url_count >= args.max_urls: break
    time.sleep(sleep)

  LOG.debug("Obtained {} URLS".format(url_count))

  


if __name__ == "__main__":
  main()
