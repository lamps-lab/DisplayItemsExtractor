import re
import common


def read_claims(read_file):
    with open(read_file, 'r') as f:
        text = f.read()
        return text


def find_tables_ref(text):
    """
            Given the claim text, this method will find the number of tables mentioned in the text and return
    """
    table_numbers = []
    additional_table_numbers_with_alpha_chars = []

    # Extract the tables numbered with numbers (Table 1, Table 1a, Tables 1-3, Tables 1 and 2)
    table_refs = re.findall('table [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                 + re.findall('tables [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                 + re.findall('tables [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                 + re.findall('tables [0-9]+[a-z]* and [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                 + re.findall('table\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                 + re.findall('tables\xa0[0-9]+[a-z]* and\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE)

    # Extract the tables numbered with roman numbers (Table II)
    tables_with_roman_numbers = re.findall('Table (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('table (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('TABLE (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text)

    # Convert the roman numbers to integers
    for roman_number_tuple in tables_with_roman_numbers:
        roman_number = roman_number_tuple[0] + roman_number_tuple[1]
        roman = {'I': 1, 'V': 5, 'X': 10, 'IV': 4, 'IX': 9}
        i = 0
        num = 0
        while i < len(roman_number):
            if i + 1 < len(roman_number) and roman_number[i:i + 2] in roman:
                num += roman[roman_number[i:i + 2]]
                i += 2
            else:
                num += roman[roman_number[i]]
                i += 1
        table_numbers.append(str(num))

    for table_ref in table_refs:
        if '\xa0' in table_ref:
            table = table_ref.split("\xa0")
        else:
            table = table_ref.split(" ")
        if table[0].lower() == "table":
            contains_alpha_char = False
            for character in table[1]:
                if character.isalpha():
                    contains_alpha_char = True
            if contains_alpha_char:
                additional_table_numbers_with_alpha_chars.append(table[1])
            else:
                table_numbers.append(table[1])
        elif table[0].lower() == "tables":
            # check for 'and'
            if "and" in table:
                contains_alpha_char = False
                for table_num in [table[1], table[3]]:
                    for character in table_num:
                        if character.isalpha():
                            contains_alpha_char = True
                    if contains_alpha_char:
                        additional_table_numbers_with_alpha_chars.append(table_num)
                    else:
                        table_numbers.append(table_num)
            # check for the long dash
            elif "–" in table[1]:
                table_numbers.extend(table[1].split("–"))
            # check for the small dash
            elif "-" in table[1]:
                table_numbers.extend(table[1].split("-"))

    return table_numbers, additional_table_numbers_with_alpha_chars


def find_figures_ref(text):
    """
            Given the text extracted from the paper, this method will find the number of figures in the text and return
        """
    # Extract the figures numbered with numbers (Fig. 1, Fig.1, Fig 1, Figure 1,
    #                                            Fig. 1a, Fig.1a, Fig 1a, Figure 1a,
    #                                            Figs. 1-3, Figs 1-3, Figures 1-3,
    #                                            Figs. 1 and 2, Figs 1 and 2, Figures 1 and 2)
    figure_refs = re.findall('fig [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('fig. [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('fig.[0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figure [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figs. [0-9]+[a-z]* and [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figs [0-9]+[a-z]* and [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figures [0-9]+[a-z]* and [0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figures [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs. [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figures [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs. [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('fig\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('fig.\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figure\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figs.\xa0[0-9]+[a-z]* and\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figs\xa0[0-9]+[a-z]* and\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE) \
                  + re.findall('figures\xa0[0-9]+[a-z]* and\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE)

    # Extract the figures numbered with roman numbers (Fig. II, Fig II, Figure II)
    tables_with_roman_numbers = re.findall('Figure (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('figure (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('FIGURE (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('Fig (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('fig (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('FIG (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('Fig. (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('fig. (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('FIG. (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('Fig.(X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('fig.(X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('FIG.(X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text)

    figure_numbers = []
    additional_figures_numbers_with_alpha_chars = []

    # Convert the roman numbers to integers
    for roman_number_tuple in tables_with_roman_numbers:
        roman_number = roman_number_tuple[0] + roman_number_tuple[1]
        roman = {'I': 1, 'V': 5, 'X': 10, 'IV': 4, 'IX': 9}
        i = 0
        num = 0
        while i < len(roman_number):
            if i + 1 < len(roman_number) and roman_number[i:i + 2] in roman:
                num += roman[roman_number[i:i + 2]]
                i += 2
            else:
                num += roman[roman_number[i]]
                i += 1

        figure_numbers.append(str(num))

    for figure_ref in figure_refs:
        if 'figs' in figure_ref.lower() or 'figures' in figure_ref.lower():
            if '\xa0' in figure_ref:
                figure = figure_ref.split("\xa0")
            else:
                figure = figure_ref.split(" ")
            # check for 'and'
            if "and" in figure:
                contains_alpha_char = False
                for fig_num in [figure[1], figure[3]]:
                    for character in fig_num:
                        if character.isalpha():
                            contains_alpha_char = True
                    if contains_alpha_char:
                        additional_figures_numbers_with_alpha_chars.append(fig_num)
                    else:
                        figure_numbers.append(fig_num)
            # check for the long dash
            elif "–" in figure[1]:
                figure_numbers.extend(figure[1].split("–"))
            # check for the small dash
            elif "-" in figure[1]:
                figure_numbers.extend(figure[1].split("-"))
        else:
            if '\xa0' in figure_ref:
                figure = figure_ref.split("\xa0")
            else:
                figure = figure_ref.split(" ")
            contains_alpha_char = False
            for character in figure[1]:
                if character.isalpha():
                    contains_alpha_char = True
            if contains_alpha_char:
                additional_figures_numbers_with_alpha_chars.append(figure[1])
            else:
                figure_numbers.append(figure[1])

    return figure_numbers, additional_figures_numbers_with_alpha_chars


def get_total_mentions_of_display_items_from_claim_text(display_item_numbers, additional_display_items_with_alpha_chars):

    if len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) == 0:
        return 0
    elif len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(additional_display_items_with_alpha_chars)
    elif len(display_item_numbers) != 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(display_item_numbers) + len(additional_display_items_with_alpha_chars)
    else:
        return len(display_item_numbers)


def get_unique_mentions_of_display_items_from_claim_text(display_item_numbers,
                                                        additional_display_items_with_alpha_chars):
    if len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) == 0:
        return 0
    elif len(display_item_numbers) == 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(set(additional_display_items_with_alpha_chars))
    elif len(display_item_numbers) != 0 and len(additional_display_items_with_alpha_chars) != 0:
        return len(set(display_item_numbers)) + len(set(additional_display_items_with_alpha_chars))
    else:
        return len(set(display_item_numbers))


def get_display_items_from_claim(filename):
    text = read_claims(filename)
    table_numbers, additional_table_numbers_with_alpha_chars = find_tables_ref(text)
    figure_numbers, additional_figures_numbers_with_alpha_chars = find_figures_ref(text)

    total_mentions_of_table_ref_in_the_claim = \
        get_total_mentions_of_display_items_from_claim_text(table_numbers, additional_table_numbers_with_alpha_chars)
    total_mentions_of_figure_ref_in_the_claim = \
        get_total_mentions_of_display_items_from_claim_text(figure_numbers, additional_figures_numbers_with_alpha_chars)

    unique_mentions_of_table_ref_in_the_claim = \
        get_unique_mentions_of_display_items_from_claim_text(table_numbers, additional_table_numbers_with_alpha_chars)
    unique_mentions_of_figure_ref_in_the_claim = \
        get_unique_mentions_of_display_items_from_claim_text(figure_numbers, additional_figures_numbers_with_alpha_chars)

    return (total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim,
            unique_mentions_of_table_ref_in_the_claim, unique_mentions_of_figure_ref_in_the_claim)


if __name__ == "__main__":
    # input the claim in a text file
    input_file = "./input/claims/FromGROBID/Fujiwara_Econometrica_2015_BbLg.txt"
    output_file = "./output/claim_level/output.json"
    total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim, \
    unique_mentions_of_table_ref_in_the_claim, unique_mentions_of_figure_ref_in_the_claim = \
        get_display_items_from_claim(input_file)

    total_mentions_of_tables_and_figures_json = \
        common.create_json(total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim)
    unique_mentions_of_tables_and_figures_json = \
        common.create_json(unique_mentions_of_table_ref_in_the_claim, unique_mentions_of_figure_ref_in_the_claim)
    json_output = common.create_claim_output_json(total_mentions_of_tables_and_figures_json,
                                                  unique_mentions_of_tables_and_figures_json)
    common.write_to_json(json_output, output_file)
