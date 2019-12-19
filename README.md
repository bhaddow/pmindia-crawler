# PMIndia Crawler

## Overview
This repository contains the code for creating a parallel corpus from the website of the Indian Prime Minister (www.pmindia.gov.in). It contains code for crawling, document and sentence alignment and language-code based filtering.

The latest releases of the corpus can be found at http://data.statmt.org/pmindia

## Usage
The following dependencies are required:
* [Snakemake](https://snakemake.readthedocs.io) A Python-based workflow management system, similar to `make`
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) A html scraping toolkit
* [Alcazar](https://github.com/saintamh/alcazar/) For extraction of text from html.
* [pycld2](https://github.com/abosamoor/pycld2) For language detection.
* [hunalign](http://mokk.bme.hu/en/resources/hunalign/) A heuristic sentence aligner.
* [vecalign](https://github.com/thompsonb/vecalign) A recent sentence aligner based on sentence embedding (optional)
* [The Pavlick Dictionaries](https://cs.brown.edu/people/epavlick/data.html) Crowd-sourced dictionaries available in many languages.
* [Moses](https://github.com/moses-smt/mosesdecoder) We use the Moses sentence splitter.

To run the crawling/alignment, you use snakemake, with the targets listed at the top of the Snakefile. Assuming the configuration variables are set correctly, and the dependencies are installed, you can crawl with:
```
snakemake crawl_all
```
To run the full pipeline, including all alignment:
```
snakemake release_all
```




## Reference

If you use the code or corpus, then please cite:

```
@article{pmindia,
  author = "Barry Haddow and Faheem Kirefu",
  title = "TBD",
  year = "2020"
}
```

