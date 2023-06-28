# CATS: A Tool for Customised Alignment of Text Simplification Corpora in Python 

We adapted CATS for alignment of German Text Simplification Corpora.


## Usage
For WAVG and CWASA, please download Word Embeddings, e.g., from here https://fasttext.cc/docs/en/crawl-vectors.html. 
For the German adaptation, please download German word embeddings and store them in ./data/de-word2vec
```
main.py -i inFolder -o outFolder  -l language -s similarityStrategy -a alignmentLevel -t alignmentStrategy {-u SubLevelalignmentStrategy} {-e embeddingsTxtFile}
```

See also [example/deplain.py](./example/deplain.py) for example code to align the DEplain corpus.


## Contributions / Changes
- to reproduce the results reported in our paper, please copy the [DEplain data](https://github.com/rstodden/DEPlain/tree/main/C__Alignment_Algorithms/documents) to [data/deplain/](./data/deplain)
- see [example/deplain.py](./example/deplain.py) for example code to align the DEplain corpus
- see DatasetAlignment/AlignAnyDataset.py for alignment of datasets with only one simplification (no references)
- bugfixes for alignment with embeddings. For our experiments we used German [FastText embeddings](https://fasttext.cc/docs/en/crawl-vectors.html) with 300 dimensions. 


## Problems
- some issue with target and source. Therefore, in AlignAnyDataset the target and source file are reversed. If it is not reversed the content of simple is saved in complex and vice versa. But then it is n:1 alignment and not 1:n as proposed in the CATS paper.
- may be due to wrong order of texts in Representations.TextAlignment.getAlignmentsUsingClosestCosSim()


## Citation
If you use this code, please cite the original CATS paper and our DEplain paper.

**Our Paper:**
```
@inproceedings{stodden-etal-2023-deplain,
    title = "{DE}-plain: A German Parallel Corpus with Intralingual Translations into Plain Language for Sentence and Document Simplification",
    author = "Stodden, Regina  and
      Momen, Omar  and
      Kallmeyer, Laura",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
}

```

**Original Paper**
The original code (in JAVA) is available at https://github.com/neosyon/SimpTextAlign.
```
@inproceedings{StajnerACL17,
  author    = {Sanja Stajner and
               Marc Franco{-}Salvador and
               Simone Paolo Ponzetto and
               Paolo Rosso and
               Heiner Stuckenschmidt},
  title     = {Sentence Alignment Methods for Improving Text Simplification Systems},
  booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2017, Vancouver, Canada, July 30 - August 4, Volume
               2: Short Papers},
  pages     = {97--102},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-2016},
  doi       = {10.18653/v1/P17-2016},
  timestamp = {Fri, 04 Aug 2017 16:38:24 +0200},
  biburl    = {https://dblp.org/rec/bib/conf/acl/StajnerFPRS17}
}
```
