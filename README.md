# Table and Figure Mentions Extractor

The display items of a scholarly document are the figures and tables in that document. This code repository contains libraries and applications of Python programs that extract figures and tables mentions. 

The extraction of figure and table mentions will be done at two levels. 
1. Paper-level extraction:
   * Input: XML file of papers in two forms; CTF and GROBID
   * Output: A JSON file that indicates the number of figures and tables in the paper 
2. Claim-level extraction:
   * Input: Claim Text
   * Output: A JSON file that indicates the number of figures and tables that are referred in that claim

## Instructions

### Setup
* **Python Version: 3.9**

* **Install:**
```pip3 install beautifulsoup4 ```

### Sample Inputs

The sample input can be found at input directory.

* input/claims -> claim text file
* input/papers
  * /grobid-tei-xml -> papers in xml file (grobid format)
  * /XMLFileIntersection ->  papers in xml file (CTF format)


### Run Code
* For paper level extractions:
  1. Run `PaperLevelExtraction.py` file
  2. Output json file can be found at 'output/paper_level/output.json'

* For claim level extractions:
  1. Run `ClaimLevelExtraction.py` file
  2. Output json file can be found at 'output/claim_level/output.json'
