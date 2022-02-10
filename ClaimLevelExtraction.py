import re
import common


def read_claims(read_file):
    with open(read_file, 'r') as f:
        text = f.read()
        return text


def find_tables_ref(text):
    # find all the appearances of the word "table" followed by a space and an integer regardless of the case
    return len(re.findall('table [0-9]', text, flags=re.IGNORECASE))


def find_figures_ref(text):
    # find all the appearances of the word "fig" and/or "figures" followed by a space and an integer regardless
    # of the case
    count_of_fig = len(re.findall('fig [0-9]', text, flags=re.IGNORECASE))
    count_of_figures = len(re.findall('figure [0-9]', text, flags=re.IGNORECASE))
    return count_of_fig + count_of_figures


def get_display_items_from_claim(filename):
    text = read_claims(filename)
    number_of_table_ref_in_the_claim = find_tables_ref(text)
    number_of_figure_ref_in_the_claim = find_figures_ref(text)
    return number_of_table_ref_in_the_claim, number_of_figure_ref_in_the_claim


if __name__ == "__main__":
    # input the claim in a text file
    input_file = "./input/claims/FromGROBID/Alcacer_AmJournSocio_2013_kZgG.txt"
    output_file = "./output/claim_level/output.json"
    number_of_tables, number_of_figures = get_display_items_from_claim(input_file)
    common.write_to_json(number_of_tables, number_of_figures, output_file)
