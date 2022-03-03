import common
import bs4
from bs4 import BeautifulSoup
import re


def find_number_of_figures_in_paper(text):
    # find the number of figures in the paper (get the largest figure number referred in the text)
    figure_refs = re.findall('fig [0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('fig. [0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('fig.[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figure [0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs. [0-9]+ and [0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs [0-9]+ and [0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figures [0-9]+ and [0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figures [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs. [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figures [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs. [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                  + re.findall('figs [0-9]+-[0-9]+', text, flags=re.IGNORECASE)

    figure_numbers = []

    print(figure_refs)

    for figure_ref in figure_refs:
        if 'figs' in figure_ref.lower() or 'figures' in figure_ref.lower():
            figure = figure_ref.split(" ")
            # check for 'and'
            if "and" in figure:
                figure_numbers.extend([figure[1], figure[3]])
            # check for the long dash
            elif "–" in figure[1]:
                figure_numbers.extend(figure[1].split("–"))
            # check for the small dash
            elif "-" in figure[1]:
                figure_numbers.extend(figure[1].split("-"))
        else:
            figure_numbers.append(figure_ref.split(" ")[1])

    if len(figure_numbers) == 0:
        return 0
    else:
        return max(figure_numbers)


def find_number_of_tables_in_paper(text):
    # find the number of tables in the paper (get the largest table number referred in the text)
    table_refs = re.findall('table [0-9]+', text, flags=re.IGNORECASE) \
                 + re.findall('tables [0-9]+–[0-9]+', text, flags=re.IGNORECASE) \
                 + re.findall('tables [0-9]+-[0-9]+', text, flags=re.IGNORECASE) \
                 + re.findall('tables [0-9]+ and [0-9]+', text, flags=re.IGNORECASE)
    # tables 1, 2, and 4

    table_numbers = []

    print(table_refs)

    for table_ref in table_refs:
        table = table_ref.split(" ")
        if table[0].lower() == "table":
            table_numbers.append(table[1])
        elif table[0].lower() == "tables":
            # check for 'and'
            if "and" in table:
                table_numbers.extend([table[1], table[3]])
            # check for the long dash
            elif "–" in table[1]:
                table_numbers.extend(table[1].split("–"))
            # check for the small dash
            elif "-" in table[1]:
                table_numbers.extend(table[1].split("-"))

    if len(table_numbers) == 0:
        return 0
    else:
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
    file_type = "ctf"
    input_file = "./input/papers/XMLFileIntersection/Zhu_JournMarketRes_2009_8w97.xml"
    # file_type = "grobid"
    # input_file = "./input/papers/grobid-tei-xml/Yeatman_Demography_2013_pGDj.xml"
    output_file = "./output/paper_level/output.json"

    print("Processing " + input_file)

    if file_type == "ctf":
        number_of_tables, number_of_figures = get_display_items_from_ctf_file(input_file)
    else:
        number_of_tables, number_of_figures = get_display_items_from_grobid_file(input_file)
    common.write_to_json(number_of_tables, number_of_figures, output_file)
