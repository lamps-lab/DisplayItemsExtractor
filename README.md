# Display Items Extractor

The display items of a scholarly document are the figures and tables in that document. This code repository contains libraries and applications of Python programs that extract figures and tables. 

The extraction of figures and tables will be done at two levels. 
1. Paper-level extraction:
   * Input: XML file of papers in two forms; CTF and GROBID
   * Output: A JSON file that indicates the number of figures and tables in the paper 
2. Claim-level extraction:
   * Input: Claim Text
   * Output: A JSON file that indicates the number of figures and tables that are referred in that claim
