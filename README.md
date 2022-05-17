# Table and Figure Reference Extractor

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
  1. Go to the `src/PaperLevelExtraction.py`
  2. Add "ctf" or "grobid" as the `file_type`
  3. Add the xml file path as the `input_file`, similar to
     1. `./input/papers/grobid-tei-xml/FILENAME` (eg: `./input/papers/grobid-tei-xml/Aakvik_SocSciMed_2010_5lxl.xml`)
     2. `./input/papers/XMLFileIntersection/FILENAME` (eg: `./input/papers/XMLFileIntersection/Abendroth_AmSocioRev_2014_G8Lr.xml`)
  4. Output json file can be found at `./output/paper_level/output.json`
  5. output.json should look like
       ```
     {
          "tables": 5,
          "figures": 0
     }


* For claim level extractions:
  1. Go to the `src/ClaimLevelExtraction.py`
  2. Add the file path which contains the claim text as the `input_file`
     1. `./input/claims/FILENAME` (eg: `./input/claims/AALTONEN_Criminology_2013_weJ4.txt`)
  3. Output json file can be found at `./output/claim_level/output.json`
  4. output.json should look like
     ```
     {
        "total mentions of tables and figures": {
             "tables": 14,
             "figures": 7
        },
        "number of unique figures and tables in claim": {
             "tables": 5,
             "figures": 4
        }
     }