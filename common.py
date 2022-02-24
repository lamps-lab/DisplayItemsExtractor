import json


def write_to_json(number_of_tables, number_of_figures, output_filename):
    json_output = {
        "tables": number_of_tables,
        "figures": number_of_figures
    }

    # Serializing json
    json_object = json.dumps(json_output, indent=4)

    # Writing to sample.json
    with open(output_filename, "w") as outfile:
        outfile.write(json_object)