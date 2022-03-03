import pandas as pd
import ClaimLevelExtraction

# Load the csv files
train1 = pd.read_csv('./sprint3-bushel-claims-train/SCORE_bushel_ta3_train1 - SCORE_bushel_ta3_train1.csv')
train2 = pd.read_csv('./sprint3-bushel-claims-train/SCORE_bushel_ta3_train2 - SCORE_bushel_ta3_train2.csv')

train1_claim2_abstract = train1['claim2_abstract']
train1_claim3_hypothesis = train1['claim3_hyp']
train1_coded_claim4 = train1['coded_claim4']

train2_claim2_abstract = train2['claim2_abstract']
train2_claim3_hypothesis = train2['claim3_hyp']
train2_coded_claim4 = train2['coded_claim4']

output_df = pd.DataFrame(columns=['claim', 'number_of_tables', 'number_of_figures'])


for claim in train1_claim2_abstract.tolist():
    number_of_tables, number_of_figures = ClaimLevelExtraction.get_display_items_from_claim_text(claim)
    output_df = output_df.append({'claim': claim,
                                  'number_of_tables': number_of_tables,
                                  'number_of_figures': number_of_figures},
                                 ignore_index=True)

for claim in train1_claim3_hypothesis.tolist():
    number_of_tables, number_of_figures = ClaimLevelExtraction.get_display_items_from_claim_text(claim)
    output_df = output_df.append({'claim': claim,
                                  'number_of_tables': number_of_tables,
                                  'number_of_figures': number_of_figures},
                                 ignore_index=True)

for claim in train1_coded_claim4.tolist():
    number_of_tables, number_of_figures = ClaimLevelExtraction.get_display_items_from_claim_text(claim)
    output_df = output_df.append({'claim': claim,
                                  'number_of_tables': number_of_tables,
                                  'number_of_figures': number_of_figures},
                                 ignore_index=True)

for claim in train2_claim2_abstract.tolist():
    number_of_tables, number_of_figures = ClaimLevelExtraction.get_display_items_from_claim_text(claim)
    output_df = output_df.append({'claim': claim,
                                  'number_of_tables': number_of_tables,
                                  'number_of_figures': number_of_figures},
                                 ignore_index=True)

for claim in train2_claim3_hypothesis.tolist():
    number_of_tables, number_of_figures = ClaimLevelExtraction.get_display_items_from_claim_text(claim)
    output_df = output_df.append({'claim': claim,
                                  'number_of_tables': number_of_tables,
                                  'number_of_figures': number_of_figures},
                                 ignore_index=True)

for claim in train2_coded_claim4.tolist():
    number_of_tables, number_of_figures = ClaimLevelExtraction.get_display_items_from_claim_text(claim)
    output_df = output_df.append({'claim': claim,
                                  'number_of_tables': number_of_tables,
                                  'number_of_figures': number_of_figures},
                                 ignore_index=True)

output_df.to_csv('./output/sprint3-bushel-claims/output.csv')
