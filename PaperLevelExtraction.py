import common
import bs4
from bs4 import BeautifulSoup
import re


def find_number_of_figures_in_paper(text):
    # find the number of figures in the paper (get the largest figure number referred in the text)
    figure_refs = re.findall('fig [0-9]', text, flags=re.IGNORECASE) + \
                   re.findall('figure [0-9]', text, flags=re.IGNORECASE)
    figure_numbers = []
    for figure_ref in figure_refs:
        figure_numbers.append(figure_ref.split(" ")[1])

    return max(figure_numbers)


def find_number_of_tables_in_paper(text):
    # find the number of tables in the paper (get the largest table number referred in the text)
    table_refs = re.findall('table [0-9]', text, flags=re.IGNORECASE)
    table_numbers = []
    for table_ref in table_refs:
        table_numbers.append(table_ref.split(" ")[1])

    return max(table_numbers)


def extract_text_from_ctf_file(read_file):
    text = ''

    with open(read_file, 'r') as f:
        try:
            soup = BeautifulSoup(f.read(), "lxml")

            for line in soup.find_all('p'):
                if (type(line.previous_element)) is not bs4.element.Tag:
                    text = text + str(line.text)

        except UnicodeDecodeError:
            raise Exception

    return text


def extract_text_from_grobid_file(read_file):
    text = ''

    with open(read_file, 'r') as tei:
        soup = BeautifulSoup(tei, 'lxml')

        for p in soup.find_all("p"):
            text = text + str(p.getText())

    return text


def get_display_items_from_ctf_file(filename):
    text = extract_text_from_ctf_file(filename)
    number_of_tables_in_ctf = find_number_of_tables_in_paper(text)
    number_of_figures_in_ctf = find_number_of_figures_in_paper(text)
    return number_of_tables_in_ctf, number_of_figures_in_ctf


def get_display_items_from_grobid_file(filename):
    text = extract_text_from_grobid_file(filename)
    number_of_tables_in_grobid = find_number_of_tables_in_paper(text)
    number_of_figures_in_grobid = find_number_of_figures_in_paper(text)
    return number_of_tables_in_grobid, number_of_figures_in_grobid


if __name__ == "__main__":
    # input the xml file
    file_type = "grobid"
    input_file = "./input/papers/grobid-tei-xml/Alcacer_AmJournSocio_2013_kZgG.xml"
    output_file = "./output/paper_level/output.json"

    if file_type == "ctf":
        number_of_tables, number_of_figures = get_display_items_from_ctf_file(input_file)
    else:
        number_of_tables, number_of_figures = get_display_items_from_grobid_file(input_file)
    common.write_to_json(number_of_tables, number_of_figures, output_file)
