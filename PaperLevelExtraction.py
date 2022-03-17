import common
import bs4
from bs4 import BeautifulSoup
import re


def find_number_of_tables_in_paper(text):
    """
        Given the text extracted from the paper, this method will find the number of tables in the text and return
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

    if len(table_numbers) == 0 and len(additional_table_numbers_with_alpha_chars) == 0:
        return 0
    elif len(table_numbers) == 0 and len(additional_table_numbers_with_alpha_chars) != 0:
        return len(set(additional_table_numbers_with_alpha_chars))
    elif len(table_numbers) != 0 and len(additional_table_numbers_with_alpha_chars) != 0:
        return int(max(table_numbers)) + len(set(additional_table_numbers_with_alpha_chars))
    else:
        return int(max(table_numbers))


def find_number_of_figures_in_paper(text):
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
                                + re.findall('FIG.(X{0,3})(X|IX|VIII|VII|VI|V|IV|III|II|I)', text) \

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
    if len(figure_numbers) == 0 and len(additional_figures_numbers_with_alpha_chars) == 0:
        return 0
    elif len(figure_numbers) == 0 and len(additional_figures_numbers_with_alpha_chars) != 0:
        return len(set(additional_figures_numbers_with_alpha_chars))
    elif len(figure_numbers) != 0 and len(additional_figures_numbers_with_alpha_chars) != 0:
        return int(max(figure_numbers)) + len(set(additional_figures_numbers_with_alpha_chars))
    else:
        return int(max(figure_numbers))


def find_table_references_in_links(links):
    """
        Given the links extracted from the paper, this method will find the number of table in the text and return
    """
    table_numbers = []
    for link in links:
        link_href = link.attrs['href']
        if "tbl" in link_href:
            table_numbers.append(link_href.split("-tbl-")[1].lstrip('0'))
    if len(table_numbers) == 0:
        return 0
    else:
        return int(max(table_numbers))


def find_figure_references_in_links(links):
    figure_numbers = []
    for link in links:
        link_href = link.attrs['href']
        if "fig" in link_href:
            figure_numbers.append(link_href.split("-fig-")[1].lstrip('0'))

    if len(figure_numbers) == 0:
        return 0
    else:
        return int(max(figure_numbers))


def extract_text_from_ctf_file(read_file):
    text = ''
    links = []

    with open(read_file, 'r') as f:
        try:
            soup = BeautifulSoup(f.read(), "lxml")

            for line in soup.find_all('p'):
                if (type(line.previous_element)) is not bs4.element.Tag:
                    text = text + str(line.text)
            for link in soup.find_all("link"):
                links.append(link)

        except UnicodeDecodeError:
            raise Exception

    return text, links


def extract_text_from_grobid_file(read_file):
    text = ''

    with open(read_file, 'r') as tei:
        soup = BeautifulSoup(tei, 'lxml')

        for p in soup.find_all("p"):
            text = text + str(p.getText())

    return text


def get_display_items_from_ctf_file(filename):
    text, links = extract_text_from_ctf_file(filename)
    number_of_tables_in_ctf_links, number_of_figures_in_ctf_links = 0, 0
    if len(links) != 0:
        number_of_tables_in_ctf_links = find_table_references_in_links(links)
        number_of_figures_in_ctf_links = find_figure_references_in_links(links)
    number_of_tables_in_ctf_text = find_number_of_tables_in_paper(text)
    number_of_figures_in_ctf_text = find_number_of_figures_in_paper(text)
    return max(number_of_tables_in_ctf_text, number_of_tables_in_ctf_links), \
           max(number_of_figures_in_ctf_text, number_of_figures_in_ctf_links)


def get_display_items_from_grobid_file(filename):
    text = extract_text_from_grobid_file(filename)
    number_of_tables_in_grobid = find_number_of_tables_in_paper(text)
    number_of_figures_in_grobid = find_number_of_figures_in_paper(text)
    return number_of_tables_in_grobid, number_of_figures_in_grobid


if __name__ == "__main__":
    # input the xml file
    # file_type = "ctf"
    # input_file = "./input/papers/XMLFileIntersection/Abendroth_AmSocioRev_2014_G8Lr.xml"
    file_type = "grobid"
    input_file = "./input/papers/grobid-tei-xml/Fujiwara_Econometrica_2015_BbLg.xml"
    output_file = "./output/paper_level/output.json"

    print("Processing " + input_file)

    if file_type == "ctf":
        number_of_tables, number_of_figures = get_display_items_from_ctf_file(input_file)
    else:
        number_of_tables, number_of_figures = get_display_items_from_grobid_file(input_file)
    json_out = common.create_json(number_of_tables, number_of_figures)
    common.write_to_json(json_out, output_file)
