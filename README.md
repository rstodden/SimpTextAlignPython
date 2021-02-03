# CATS: A Tool for Customised Alignment of Text Simplification Corpora in Python
The java version available at https://github.com/neosyon/SimpTextAlign
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

## Usage

```
main.py -i inFolder -o outFolder  -l language -s similarityStrategy -a alignmentLevel -t alignmentStrategy {-u SubLevelalignmentStrategy} {-e embeddingsTxtFile}
