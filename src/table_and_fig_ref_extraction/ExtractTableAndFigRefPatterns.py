import re

regex_alphanumeric_table_patterns = [
    (r'table [0-9]+[a-z]*', True),
    (r'tables [0-9]+–[0-9]+', True),
    (r'tables [0-9]+-[0-9]+', True),
    (r'tables [0-9]+[a-z]* and [0-9]+[a-z]*', True),
    (r'table\xa0[0-9]+[a-z]*', True),
    (r'tables\xa0[0-9]+[a-z]* and\xa0[0-9]+[a-z]*', True)
]
regex_roman_number_table_patterns = [
    (r'Table (M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', False),
    (r'table (M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', False),
    (r'TABLE (M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', False)
]
regex_alphanumeric_fig_patterns = [
    (r'(fig(ure) ?|fig.( )?)([0-9]+[a-z]*)', True),
    (r'(fig(ure)?s |figs. )([0-9]+–[0-9]+)', True),
    (r'(fig(ure)?s |figs. )([0-9]+-[0-9]+)', True),
    (r'(fig(ure)?s |figs. )([0-9]+[a-z]* and [0-9]+[a-z]*)', True),
    (r'(fig(ure)\xa0?|fig.(\xa0)?)([0-9]+[a-z]*)', True),
    (r'(fig(ure)?s\xa0|figs.\xa0)([0-9]+[a-z]* and\xa0[0-9]+[a-z]*)', True)
]
regex_roman_number_fig_patterns = [
    (r'(fig(ure) ?|fig.( )?)(M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', False),
    (r'(Fig(ure) ?|Fig.( )?)(M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', False),
    (r'(FIG(URE) ?|FIG.( )?)(M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', False)
]


def addNewTablePattern(isAlphanumericType, pattern, ignoreCase=True):
    """
    Add a new pattern to the pre-defined list of Table patterns
    :param isAlphanumericType: True if the new pattern represents a pattern with alphanumeric
                               False if the new pattern represents a pattern with roman numbers
    :param pattern: The new pattern
    :param ignoreCase: True if the pattern is case-insensitive
                       False if the pattern is case-sensitive
    """
    if isAlphanumericType:
        regex_alphanumeric_table_patterns.append((pattern, ignoreCase))
    else:
        regex_roman_number_table_patterns.append((pattern, ignoreCase))


def addNewFigPattern(isAlphanumericType, pattern, ignoreCase=True):
    """
    Add a new pattern to the pre-defined list of Figure patterns
    :param isAlphanumericType: True if the new pattern represents a pattern with alphanumeric
                               False if the new pattern represents a pattern with roman numbers
    :param pattern: The new pattern
    :param ignoreCase: True if the pattern is case-insensitive
                       False if the pattern is case-sensitive
    """
    if isAlphanumericType:
        regex_alphanumeric_fig_patterns.append((pattern, ignoreCase))
    else:
        regex_roman_number_fig_patterns.append((pattern, ignoreCase))


def findTableRefs(text):
    """
    Return the table references that match the defined regex patterns in the text
    :param text: the document text extracted from scholarly papers
    :return:
        alphanumeric_table_refs: the table references with alphanumeric numbers that are found in the text
        roman_number_table_refs: the table references with roman numbers that are found in the text
    """

    # Find the table references numbered with alphanumeric numbers
    alphanumeric_table_refs = []

    for pattern in regex_alphanumeric_table_patterns:
        if pattern[1]:
            table_refs = re.findall(pattern[0], text, flags=re.IGNORECASE)
        else:
            table_refs = re.findall(pattern[0], text)
        if table_refs:
            alphanumeric_table_refs.append(table_refs)

    # Find the table references numbered with roman numbers
    roman_number_table_refs = []

    for pattern in regex_roman_number_table_patterns:
        if pattern[1]:
            table_refs = re.findall(pattern[0], text, flags=re.IGNORECASE)
        else:
            table_refs = re.findall(pattern[0], text)

        for ref_pattern in table_refs:
            if str(ref_pattern[0] + ref_pattern[1] + ref_pattern[2] + ref_pattern[3]) != '':
                roman_number_table_refs.append('table ' + str(ref_pattern[0] + ref_pattern[1] + ref_pattern[2] +
                                                              ref_pattern[3]))

    return alphanumeric_table_refs, roman_number_table_refs


def findFigRefs(text):
    """
    Return the figure references that match the defined regex patterns in the text
    :param text: the document text extracted from scholarly papers
    :return:
        alphanumeric_fig_refs: the figure references with alphanumeric numbers that are found in the text
        roman_number_fig_refs: the figure references with roman numbers that are found in the text
    """

    # Find the figure references numbered with alphanumeric numbers
    alphanumeric_fig_refs = []

    for pattern in regex_alphanumeric_fig_patterns:
        if pattern[1]:
            fig_refs = re.findall(pattern[0], text, flags=re.IGNORECASE)
        else:
            fig_refs = re.findall(pattern[0], text)
        if fig_refs:
            alphanumeric_fig_refs.extend([(ref_pattern[0] + ref_pattern[3]) for ref_pattern in fig_refs])

    # Find the figure references numbered with roman numbers
    roman_number_fig_refs = []

    for pattern in regex_roman_number_fig_patterns:
        if pattern[1]:
            fig_refs = re.findall(pattern[0], text, flags=re.IGNORECASE)
        else:
            fig_refs = re.findall(pattern[0], text)

        for ref_pattern in fig_refs:
            if str(ref_pattern[3] + ref_pattern[4] + ref_pattern[5] + ref_pattern[6]) != '':
                roman_number_fig_refs.append('figure ' + str(ref_pattern[3] + ref_pattern[4] + ref_pattern[5] +
                                                             ref_pattern[6]))

    return alphanumeric_fig_refs, roman_number_fig_refs
