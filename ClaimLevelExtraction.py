import json
import re


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


# input the claim in a text file
text = read_claims("input/claims/FromGROBID/Alcacer_AmJournSocio_2013_kZgG.txt")
number_of_table_ref_in_the_claim = find_tables_ref(text)
number_of_figure_ref_in_the_claim = find_figures_ref(text)

json_output = {
    "tables": number_of_table_ref_in_the_claim,
    "figures": number_of_figure_ref_in_the_claim
}

# Serializing json
json_object = json.dumps(json_output, indent=4)

# Writing to sample.json
with open("./output/claim_level/output.json", "w") as outfile:
    outfile.write(json_object)

