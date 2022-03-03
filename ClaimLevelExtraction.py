import re
import common


def read_claims(read_file):
    with open(read_file, 'r') as f:
        text = f.read()
        return text


def find_tables_ref(text):
    # find all the appearances of the word "table" followed by a space and an integer regardless of the case
    count_of_tables_pattern_1 = len(re.findall('table [0-9]+', text, flags=re.IGNORECASE))
    table_ref_with_long_dash = re.findall('tables [0-9]+–[0-9]+', text, flags=re.IGNORECASE)
    table_ref_with_small_dash = re.findall('tables [0-9]+-[0-9]+', text, flags=re.IGNORECASE)
    table_ref_with_and = re.findall('tables [0-9]+ and [0-9]+', text, flags=re.IGNORECASE)
    count_of_tables_pattern_2, count_of_tables_pattern_3, count_of_tables_pattern_4 = 0, 0, 0

    if len(table_ref_with_long_dash) != 0:
        for table_ref in table_ref_with_long_dash:
            table_num = table_ref.split(" ")[1]
            table_num_list = table_num.split("–")
            count_of_tables_pattern_2 = int(table_num_list[1]) - int(table_num_list[0])

    if len(table_ref_with_small_dash) != 0:
        for table_ref in table_ref_with_small_dash:
            table_num = table_ref.split(" ")[1]
            table_num_list = table_num.split("-")
            count_of_tables_pattern_3 = int(table_num_list[1]) - int(table_num_list[0])

    if len(table_ref_with_and) != 0:
        for table_ref in table_ref_with_and:
            count_of_tables_pattern_4 += 2

    return (count_of_tables_pattern_1 + count_of_tables_pattern_2
            + count_of_tables_pattern_3 + count_of_tables_pattern_4)


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


def get_display_items_from_claim_text(claim):
    number_of_table_ref_in_the_claim = find_tables_ref(claim)
    number_of_figure_ref_in_the_claim = find_figures_ref(claim)
    return number_of_table_ref_in_the_claim, number_of_figure_ref_in_the_claim


def get_display_items_from_claim(filename):
    text = read_claims(filename)
    number_of_table_ref_in_the_claim, number_of_figure_ref_in_the_claim = get_display_items_from_claim_text(text)
    return number_of_table_ref_in_the_claim, number_of_figure_ref_in_the_claim


if __name__ == "__main__":
    # input the claim in a text file
    input_file = "./input/claims/FromGROBID/Alcacer_AmJournSocio_2013_kZgG.txt"
    output_file = "./output/claim_level/output.json"
    number_of_tables, number_of_figures = get_display_items_from_claim(input_file)
    common.write_to_json(number_of_tables, number_of_figures, output_file)
