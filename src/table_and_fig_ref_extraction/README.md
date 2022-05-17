# Table and Figure Reference Extraction Using RegEx 

This library provides the functionalities to extract the table and figure references from the text in scientific papers using Regular Expressions(RegEx). This library has a predefined lists of RegEx patterns which represent different styles that the authors can use to refer tables and figures in scientific papers.

### RegEx Pattern Alphanumeric Numbered Table References

| Style                | RegEx Pattern 	 	| Ignore Case	 | 
|----------------------|---	|--------------|
| Table 1 /  Table 1A  | `r'table [0-9]+[a-z]*'`                                                                             | 	     True   |
| Tables 1–4 (em dash) | `r'tables [0-9]+–[0-9]+'`                                                                              | True	        |
| Tables 1-4 (en dash) | `r'tables [0-9]+-[0-9]+]'`                                                                             | True   	     |
| Tables 1A and 2A     | `r'tables [0-9]+[a-z]* and [0-9]+[a-z]*'`          | True |

### RegEx Pattern Roman Numbered Table References

| Style    | RegEx Pattern 	 	                                                                                                                     | Ignore Case	 | 
|----------|---------------------------------------------------------------------------------------------------------------------------------------|--------------|
| Table IV | `r'Table (M{0,4})(CM `&#124;` CD  `           &#124;` D?C{0,3})(XC` &#124; `XL` &#124;` L?X{0,3})(IX` &#124;` IV` &#124;`V?I{0,3})' ` | False        |
| table IV | `r'table (M{0,4})(CM `&#124;` CD  `           &#124;` D?C{0,3})(XC` &#124; `XL` &#124;` L?X{0,3})(IX` &#124;` IV` &#124;`V?I{0,3})' ` | False        |
| TABLE IV | `r'TABLE (M{0,4})(CM `&#124;` CD  `           &#124;` D?C{0,3})(XC` &#124; `XL` &#124;` L?X{0,3})(IX` &#124;` IV` &#124;`V?I{0,3})' ` | False        |

### RegEx Pattern Alphanumeric Numbered Figure References

| Style                                                                                                   | RegEx Pattern 	 	                               | Ignore Case	 | 
|---------------------------------------------------------------------------------------------------------|-------------------------------------------------|------|
| Fig 1 / Fig. 1 / Fig.1 / Figure 1 / Fig 1A / Fig. 1A / Fig.1A / Figure 1A                               | `r'(fig(ure) ?`&#124;`fig.( )?)([0-9]+[a-z]*)'` | True |
| Figs 1–4 / Figs. 1–4 / Figures 1–4 (em dash)                                                            | `r'(fig(ure)?s `&#124;`figs. )([0-9]+–[0-9]+)'` | True |
| Figs 1-4 / Figs. 1-4 / Figures 1-4 (en dash)	                                                           | `r'(fig(ure)?s `&#124;`figs. )([0-9]+-[0-9]+)'`    | True   	 |
| Figs 1 and 2 / Figs. 1 and 2 / Figures 1 and 2  / Figs 1A and 1B / Figs. 1A and 1B / Figures 1A and 1B	 | `r'(fig(ure)?s` &#124;`figs. )([0-9]+[a-z]* and [0-9]+[a-z]*)'`      | True |


### RegEx Pattern Roman Numbered Table References

| Style                                       | RegEx Pattern 	 	                                                                                                                               | Ignore Case	 | 
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| Fig IV  /  Fig. IV  /  Fig.IV  /  Figure IV | `r'(Fig(ure) ?`&#124;`Fig.( )?)(M{0,4})(CM` &#124; `CD` &#124; `D?C{0,3})(XC` &#124; `XL` &#124; `L?X{0,3})(IX` &#124; `IV` &#124; `V?I{0,3})'` | False        |
| fig IV  /  fig. IV  /  fig.IV  /  figure IV | `r'(fig(ure) ?`&#124;`fig.( )?)(M{0,4})(CM` &#124; `CD` &#124; `D?C{0,3})(XC` &#124; `XL` &#124; `L?X{0,3})(IX` &#124; `IV` &#124; `V?I{0,3})'` | False        |
| FIG IV  /  FIG. IV  /  FIG.IV  /  FIGURE IV | `r'(FIG(URE) ?`&#124;`FIG.( )?)(M{0,4})(CM` &#124; `CD` &#124; `D?C{0,3})(XC` &#124; `XL` &#124; `L?X{0,3})(IX` &#124; `IV` &#124; `V?I{0,3})'` | False        |

## Instructions

### Setup
* **Python Version: 3.9**

### Install
Run the below command to install the TableAndFigureReferenceExtractor library into your code.
```
pip3 install -e git+https://github.com/lamps-lab/TableAndFigureReferenceExtractor#egg=table_and_fig_ref_extraction  
```

Optionally, upgrade pip to avoid getting warnings.
```
python3 -m pip install --upgrade pip 
```


### Run code

#### 1. Import methods of this library into your code
```
from table_and_fig_ref_extraction.ExtractTableAndFigRefPatterns import *
```

#### 2. Extract Table References from the Text
```
alphanumeric_table_refs, roman_number_table_refs = findTableRefs(text)
```
`findTableRefs()` method will take the `text` extracted from the document, find the table references by using the predefined RegEx patterns (including both alphanumeric numbers and roman numbers), and return two lists containing the table references with alphanumeric numbers and roman numbers.

#### 2. Extract Figure References from the Text
```
alphanumeric_fig_refs, roman_number_fig_refs = findFigRefs(text)
```
`findFigRefs()` method will take the `text` extracted from the document, find the figure references by using the predefined RegEx patterns (including both alphanumeric numbers and roman numbers), and return two lists containing the figure references with alphanumeric numbers and roman numbers.

#### 3. Add new RegEx patterns
 If any new RegEx pattern emerge, that could be added to the library.

```
addNewTablePattern(isAlphanumericType, pattern, ignoreCase)

addNewFigPattern(isAlphanumericType, pattern, ignoreCase)
```

These two methods can be used to add new table and figure patterns to the pre-defined list of patterns. 

* If the new pattern represents a pattern with alphanumeric, set _isAlphanumericType_ **True**, and if the new pattern represents a pattern with roman numbers, set it to **False**.
* Pass the new pattern using the _pattern_ parameter.
* Set **ignoreCase** as **True** if the pattern is case-insensitive, **False** if the pattern is case-sensitive. _The default is True._
 