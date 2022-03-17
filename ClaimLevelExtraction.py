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

    # Extract the tables numbered with numbers (Table 1, Table 1a, Tables 1-3, Tables 1 and 2)
    count_of_tables_pattern_1 = len(re.findall('table [0-9]+[a-z]*', text, flags=re.IGNORECASE))
    count_of_tables_pattern_2 = len(re.findall('table\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE))
    table_ref_with_long_dash = re.findall('tables [0-9]+–[0-9]+', text, flags=re.IGNORECASE)
    table_ref_with_small_dash = re.findall('tables [0-9]+-[0-9]+', text, flags=re.IGNORECASE)
    table_ref_with_and = re.findall('tables [0-9]+[a-z]* and [0-9]+[a-z]*', text, flags=re.IGNORECASE)
    table_ref_with_and_with_nbsp = re.findall('tables\xa0[0-9]+ and\xa0[0-9]+[a-z]*', text, flags=re.IGNORECASE)
    count_of_tables_pattern_3, count_of_tables_pattern_4, count_of_tables_pattern_5, count_of_tables_pattern_6 = 0, 0, 0, 0

    # Extract the tables numbered with roman numbers (Table II)
    tables_with_roman_numbers = re.findall('Table (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('table (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \
                                + re.findall('TABLE (X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text)

    count_of_tables_with_roman_numbers = 0

    # Convert the roman numbers to integers
    for roman_number_tuple in tables_with_roman_numbers:
        count_of_tables_with_roman_numbers += 1

    if len(table_ref_with_long_dash) != 0:
        for table_ref in table_ref_with_long_dash:
            table_num = table_ref.split(" ")[1]
            table_num_list = table_num.split("–")
            count_of_tables_pattern_3 = int(table_num_list[1]) - int(table_num_list[0])

    if len(table_ref_with_small_dash) != 0:
        for table_ref in table_ref_with_small_dash:
            table_num = table_ref.split(" ")[1]
            table_num_list = table_num.split("-")
            count_of_tables_pattern_4 = int(table_num_list[1]) - int(table_num_list[0])

    if len(table_ref_with_and) != 0:
        for table_ref in table_ref_with_and:
            count_of_tables_pattern_5 += 2

    if len(table_ref_with_and_with_nbsp) != 0:
        for table_ref in table_ref_with_and_with_nbsp:
            count_of_tables_pattern_6 += 2

    return (count_of_tables_pattern_1 + count_of_tables_pattern_2
            + count_of_tables_pattern_3 + count_of_tables_pattern_4
            + count_of_tables_pattern_5 + count_of_tables_pattern_6
            + count_of_tables_with_roman_numbers)


def find_figures_ref(text):
    # find all the appearances of the word "fig" and/or "fig." and/or "figures" followed by a space and/or
    # an integer regardless of the case
    count_of_figures_pattern_1 = len(re.findall('fig [0-9]+', text, flags=re.IGNORECASE))
    count_of_figures_pattern_2 = len(re.findall('fig. [0-9]+', text, flags=re.IGNORECASE))
    count_of_figures_pattern_3 = len(re.findall('fig.[0-9]+', text, flags=re.IGNORECASE))
    count_of_figures_pattern_4 = len(re.findall('figure [0-9]+', text, flags=re.IGNORECASE))
    count_of_figures_pattern_5, count_of_figures_pattern_6, count_of_figures_pattern_7 = 0, 0, 0

    figure_ref_with_long_dash = re.findall('figures [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                                + re.findall('figs. [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                                + re.findall('figs [0-9]+–[0-9]+', text, flags=re.IGNORECASE)

    figures_ref_with_small_dash = re.findall('figures [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                                  + re.findall('figs. [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                                  + re.findall('figs [0-9]+-[0-9]+', text, flags=re.IGNORECASE)

    figures_ref_with_and = re.findall('figs. [0-9]+ and [0-9]+', text, flags=re.IGNORECASE) \
                           + re.findall('figs [0-9]+ and [0-9]+', text, flags=re.IGNORECASE) \
                           + re.findall('figures [0-9]+ and [0-9]+', text, flags=re.IGNORECASE)

    if len(figure_ref_with_long_dash) != 0:
        for fig_ref in figure_ref_with_long_dash:
            fig_num = fig_ref.split(" ")[1]
            fig_num_list = fig_num.split("–")
            count_of_figures_pattern_5 = int(fig_num_list[1]) - int(fig_num_list[0])

    if len(figures_ref_with_small_dash) != 0:
        for fig_ref in figures_ref_with_small_dash:
            fig_num = fig_ref.split(" ")[1]
            fig_num_list = fig_num.split("-")
            count_of_figures_pattern_6 = int(fig_num_list[1]) - int(fig_num_list[0])

    if len(figures_ref_with_and) != 0:
        for fig_ref in figures_ref_with_and:
            count_of_figures_pattern_7 += 2

    return (count_of_figures_pattern_1 + count_of_figures_pattern_2
            + count_of_figures_pattern_3 + count_of_figures_pattern_4
            + count_of_figures_pattern_5 + count_of_figures_pattern_6
            + count_of_figures_pattern_7)


def get_total_mentions_of_display_items_from_claim_text(claim):
    number_of_table_ref_in_the_claim = find_tables_ref(claim)
    number_of_figure_ref_in_the_claim = find_figures_ref(claim)
    return number_of_table_ref_in_the_claim, number_of_figure_ref_in_the_claim


def get_display_items_from_claim(filename):
    text = read_claims(filename)
    total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim = \
        get_total_mentions_of_display_items_from_claim_text(text)
    return total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim


if __name__ == "__main__":
    # input the claim in a text file
    input_file = "./input/claims/FromGROBID/Fujiwara_Econometrica_2015_BbLg.txt"
    output_file = "./output/claim_level/output.json"
    total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim = \
        get_display_items_from_claim(input_file)
    print(total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim)
    # total_mentions_of_tables_and_figures_json = \
    #     common.create_json(total_mentions_of_table_ref_in_the_claim, total_mentions_of_figure_ref_in_the_claim)
    # json_output = common.create_claim_output_json(total_mentions_of_tables_and_figures_json)
    # common.write_to_json(json_output, output_file)
