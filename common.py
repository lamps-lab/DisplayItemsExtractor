import json


def create_json(number_of_tables, number_of_figures):
    json_output = {
        "tables": number_of_tables,
        "figures": number_of_figures
    }

    # Serializing json
    json_object = json.dumps(json_output, indent=4)

    return json_object


def create_claim_output_json(total_mentions_of_tables_and_figures_json,
                             number_of_unique_figures_and_tables_in_claim_json):
    json_output = {
        "total mentions of tables and figures": total_mentions_of_tables_and_figures_json,
        "number of unique figures and tables in claim": number_of_unique_figures_and_tables_in_claim_json
    }

    # Serializing json
    json_object = json.dumps(json_output, indent=4)

    return json_object


def write_to_json(json_object, output_filename):
    # Writing to sample.json
    with open(output_filename, "w") as outfile:
        outfile.write(json_object)
