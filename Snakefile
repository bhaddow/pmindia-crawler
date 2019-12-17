import sys
import glob

ILANGS = ["hi", "as", "bn", "kn", "ml", "mni", "mr", "or", "pa", "ta", "te", "ur", "gu"]
LLANGS = ["hi", "ta", "bn", "ml", "mr", "te", "ur"] # supported by laser
LANGS = ILANGS + ["en"]

MOSES_SCRIPTS = "/home/bhaddow/moses.new/scripts"
INDIC_NLP = "/home/bhaddow/code/indic_nlp_library/bhaddow"
HUNALIGN = "/home/bhaddow/tools/hunalign/src/hunalign/hunalign"
VECALIGN = "/home/bhaddow/code/vecalign"
LASER = "/home/bhaddow/code/LASER"
PAVLICK_DICTS = "/home/bhaddow/data/pavlick-dicts"
MAX_URLS = 0
VERSION = "v1"

workdir: "working"


def get_pairs(tsv_file):
  pairs = []
  with open(tsv_file) as tfh:
    for line in tfh:
      fields = line[:-1].split("\t")
      if fields[0] and fields[1]:
        pairs.append((fields[0], fields[1]))
  return pairs


# BEGIN entry-point rules

rule release_all:
  input:
    expand("release/parallel/pmindia." + VERSION + ".{language}-en.tsv", language = ILANGS) + \
      expand("release/monolingual/pmindia." + VERSION + ".{language}.tgz", language = LANGS)

rule crawl_all:
  input:
    expand("{language}/html", language = LANGS)

rule extract_all:
  input:
    expand("{language}/txt", language = LANGS)

rule split_all:
  input:
    expand("{language}/split", language = LANGS)

rule hunalign_all:
  input:
    expand("corpus/align.hunalign.filtered.{language}-en.tsv", language = ILANGS)

rule vecalign_all:
  input:
    expand("corpus/align.vecalign.filtered.{language}-en.tsv", language = LLANGS)

# Compute interects and diffs of both alignments
rule intersect_align_all:
  input:
    expand("corpus/align.{intersect}.{language}-en.tsv", language = LLANGS, intersect=["intersect", "onlyhunalign", "onlyvecalign"])

# END entry-point rules

# Copy the intersection alignments to release directory
rule release_intersect:
  input:
    "corpus/align.intersect.{language}-en.tsv"

  output:
    "release/parallel/pmindia." + VERSION + ".{language}-en.tsv"
  
  wildcard_constraints:
    language = "|".join(["(" + l + ")" for l in LLANGS])

  shell:
    "mkdir -p `dirname {output}`; cp {input} {output}" 

# Copy the hunalign alignments to release directory
rule release_hunalign:
  input:
    "corpus/align.hunalign.filtered.{language}-en.tsv"

  output:
    "release/parallel/pmindia." + VERSION + ".{language}-en.tsv"
  
  # Only for languages with no laser embeddings
  wildcard_constraints:
    language = "|".join(["(" + l + ")" for l in ILANGS if l not in LLANGS])

  run:
    # copy and unique
    lines = set()
    with open(output[0], "w") as ofh, open(input[0]) as ifh:
      for line in ifh:
        if line in lines:
          continue
        lines.add(line)
        print (line, file=ofh, end="")

  #shell:
    #"mkdir -p `dirname {output}`;  LC_ALL=C sort {input} | uniq | shuf >  {output}" 


rule release_mono:
  input:
    "{language}/split"

  output:
    "release/monolingual/pmindia." + VERSION + ".{language}.tgz"

  shell:
    """
      mkdir -p `dirname {output}`
      cd {wildcards[language]}
      tar cfz ../{output} split
      cd ..
    """

rule intersect_align:
  input:
    vecalign = "corpus/align.vecalign.filtered.{language}-en.tsv",
    hunalign =  "corpus/align.hunalign.filtered.{language}-en.tsv"

  output:
    intersect = "corpus/align.intersect.{language}-en.tsv",
    onlyvec = "corpus/align.onlyvecalign.{language}-en.tsv",
    onlyhun = "corpus/align.onlyhunalign.{language}-en.tsv"

  run:
    vecaligns = set(open(input["vecalign"]).readlines())
    hunaligns = set(open(input["hunalign"]).readlines())
    
    # Keep the sentences in order
    lines = set()
    with open(input["vecalign"]) as vfh, open(output["intersect"], "w") as ifh, open(output["onlyvec"], "w") as ofh:
      for line in vfh:
        if line in lines:
          continue
        lines.add(line)
        if line in hunaligns:
          print(line, file=ifh, end="")
        else:
          print(line, file=ofh, end="")

    lines = set()
    with open(input["hunalign"]) as hfh, open(output["onlyhun"], "w") as ofh:
      for line in hfh:
        if line in lines:
          continue
        lines.add(line)
        if not line in vecaligns:
          print(line, file=ofh, end="")

    #with open(output["intersect"], "w") as ifh:
    #  for pair in vecalign_pairs.intersection(hunalign_pairs):
    #    print("\t".join(pair), file=ifh)
    #with open(output["onlyvec"], "w") as ofh:
    #  for pair in vecalign_pairs.difference(hunalign_pairs):
    #    print("\t".join(pair), file=ofh)
    #with open(output["onlyhun"], "w") as ofh:
    #  for pair in hunalign_pairs.difference(vecalign_pairs):
    #    print("\t".join(pair), file=ofh)


rule filter:
  input:
    "corpus/align.{method}.raw.{language}-en.tsv"

  output:
    "corpus/align.{method}.filtered.{language}-en.tsv"

  shell:
    sys.path[0] + "/filter.py -f {wildcards[language]} < {input} > {output} 2> {output}.err"

rule crawl:
  input:
    "{language}/urls"

  output:
    "{language}/html"

  shell:
    "wget -i {input} -P {output} --user-agent=\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0\"  --restrict-file-names=ascii ; mkdir -p {output}; touch {output}/dummy"

rule collate_hunalign:
  input:
    "{language}/hunaligned"

  output:
    "corpus/align.hunalign.raw.{language}-en.tsv"

  run:
    with open(str(output), "w") as ofh:
      for ifile in glob.glob(str(input) + "/*"):
        with open(ifile) as ifh:
          for line in ifh:
            fields = line[:-1].split("\t")
            len_f = len(fields[0].split())
            len_e = len(fields[1].split())
            print("\t".join(fields + [str(len_f), str(len_e)]), file=ofh)


rule collate_vecalign:
  input:
    "{language}/vecaligned"

  output:
    "corpus/align.vecalign.raw.{language}-en.tsv"

  run:
    with open(str(output), "w") as ofh:
      for ifile in glob.glob(str(input) + "/*tsv"):
        with open(ifile) as ifh:
          for line in ifh:
            fields = line[:-1].split("\t")
            len_f = len(fields[0].split())
            len_e = len(fields[1].split())
            print("\t".join(fields + [str(len_f), str(len_e)]), file=ofh)



rule run_hunalign:
  input:
    "en/split", "{language}/split" , "{language}/pavlick.dict"

  output:
    directory("{language}/hunaligned")

  shell:
    """
    mkdir -p {output[0]};
    for src_file in {input[0]}/*; do 
      tgt_file={input[1]}/`basename $src_file`
      if [ -e $tgt_file ] ; then
        align_file={output}/`basename $src_file`.tsv
        {HUNALIGN}  -utf -text -bisent {input[2]} $src_file $tgt_file > $align_file
      fi
    done
   """

rule get_dict:
  output:
    "{language}/pavlick.dict"

  shell:
    "if [ -e {PAVLICK_DICTS}/dict.{wildcards[language]} ] ; then  {sys.path[0]}/get_pavlick_dict.py -d {PAVLICK_DICTS}/dict.{wildcards[language]} > {output}; else touch {output}; fi"
    
rule run_vecalign:
  input:
    s_text = "en/split",
    t_text =  "{language}/split",
    s_overlap = "en/overlaps",
    t_overlap = "{language}/overlaps",
    s_overlap_embeds = "en/overlap_embeds",
    t_overlap_embeds = "{language}/overlap_embeds"

  output:
    directory("{language}/vecaligned")

  shell:
    """
      mkdir -p {output[0]};
      for src_file in {input.s_text}/*; do
        filename=`basename $src_file`
        if  [ -e {input.t_text}/$filename ]; then
          {VECALIGN}/vecalign.py --alignment_max_size 8 --src $src_file --tgt  {input.t_text}/$filename --src_embed {input.s_overlap}/$filename  {input.s_overlap_embeds}/$filename --tgt_embed {input.t_overlap}/$filename  {input.t_overlap_embeds}/$filename > {output[0]}/$filename.aln
          {sys.path[0]}/vecalign_to_tsv.py -s $src_file -t {input.t_text}/$filename -a {output[0]}/$filename.aln > {output[0]}/$filename.tsv
        fi
      done
    """

rule embed_overlap:
  input: 
    "{language}/overlaps"

  output:
    directory("{language}/overlap_embeds")

  resources:
    gpu=1

  shell:
     """
    mkdir -p  {output[0]}
    export LASER={LASER}
    find {input[0]} | parallel -j 2 "{LASER}/tasks/embed/embed.sh {{}} {wildcards[language]} {output[0]}/{{/}}" 
    """

rule make_overlap:
  input: 
    "{language}/split"

  output:
    directory("{language}/overlaps")


  shell:
    """
    mkdir -p  {output[0]}
    for src_file in {input[0]}/*; do
      filename=`basename $src_file`
      {VECALIGN}/overlap.py -i $src_file -o {output[0]}/$filename -n 10
    done
    """

rule split:
  input:
    "{language}/txt"

  output:
    directory("{language}/split")

  shell:
    """
    mkdir -p {output[0]};
    for txt_file in {input[0]}/*; do
       split_file={output[0]}/`basename $txt_file`;
       {MOSES_SCRIPTS}/ems/support/split-sentences.perl -i  -l {wildcards.language}  < $txt_file |  sed '/^<P>$/d'> $split_file;
    done
    """
       #PYTHONPATH={INDIC_NLP}/src:$PYTHONPATH python3 {INDIC_NLP}/src/indicnlp/tokenize/sentence_tokenize.py  $txt_file - {wildcards.language} | sed '/^$/d' > $split_file ;

rule extract:
  input:
    "{language}/html", "index"

  output:
    directory("{language}/txt")

  shell:
    sys.path[0] + "/extract.py -f {input[0]} -i {input[1]} -t {output}"

rule make_index:
  input:
    "en/html"

  output:
    "index"

  shell:
    sys.path[0] + "/make_index.py -l en -d {input} > {output}"

rule urls:
  output:
    "{language}/urls"


  shell:
    sys.path[0] + "/get_urls.py -l {wildcards.language} -m {MAX_URLS} > {output}"
