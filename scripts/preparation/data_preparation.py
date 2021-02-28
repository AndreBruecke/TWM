import pandas as pd
import pyphen
import os

columns = [
    'document_id', 'ta_rule', 'ta_counter', 'ta_token', 'ta_language', 'ta_type', 'ta_type_expanded', 'ta_normalized',
    'ta_stem', 'ta_paragraph', 'ta_sentence', 'ta_created_at', 'ta_offset', 'ta_parent'
]


def prepare_data(filename):
    raw_df = pd.read_csv('data_in/hana/' + filename)
    raw_df.columns = columns

    raw_df = raw_df.drop(['ta_rule', 'ta_created_at', 'ta_language', 'ta_parent', 'ta_type_expanded'], axis='columns')
    raw_df = raw_df[raw_df.ta_type != 'punctuation']

    return raw_df


files = os.listdir('data_in/hana')

all_dfs = []
for data_file in files:
    all_dfs.append(prepare_data(data_file))

df = pd.concat(all_dfs)

doc_lengths = df[['document_id', 'ta_counter']].groupby(by='document_id').count()

"""
Empty documents
"""
before = len(df)
missing_data = doc_lengths[doc_lengths.ta_counter == 1].index.tolist()
df = df[~df.document_id.isin(missing_data)]
after = len(df)
print(before - after, "documents removed due to missing data.")

"""
Abbreviations of length 1, e.g. 'd.h.' being split into 4 tokens
"""
tokens_before = len(df)
df = df[df.ta_token.str.len() > 1]
tokens_after = len(df)
print(tokens_before - tokens_after, "abbreviations of length 1 removed.")

"""
Uncategorized tokens
"""
tokens_before = len(df)
df = df[~df.ta_type.isna()]
tokens_after = len(df)
print(tokens_before - tokens_after, "uncategorized tokens removed.")

df.to_csv('data_out/cleansed_combined.csv', index=False)


"""
Summarize
"""
meta = pd.read_csv('data_in/gutenberg_meta.csv')

doc_tokens = df[['document_id', 'ta_counter']].groupby(by='document_id', as_index=False).count()
doc_tokens.columns = ['document_id', 'token_count']

doc_sentences = df[['document_id', 'ta_sentence']].groupby(by='document_id', as_index=False).ta_sentence.nunique()
doc_sentences.columns = ['document_id', 'sentence_count']

doc_stats = meta.join(doc_tokens.set_index('document_id'), on=meta.index, how='inner')
doc_stats = doc_stats.drop('key_0', axis=1)
doc_stats = doc_stats.join(doc_sentences.set_index('document_id'), on=doc_stats.index, how='inner')
doc_stats = doc_stats.drop('key_0', axis=1)
doc_stats['avg_sentence_length'] = doc_stats['token_count'] / doc_stats['sentence_count']

de_dict = pyphen.Pyphen(lang='de')
df['syllables'] = df.ta_token.apply(lambda token: len(de_dict.inserted(token).split('-')))

avg_syllables = df[['document_id', 'syllables']].groupby(by='document_id', as_index=False).syllables.mean()
avg_syllables.columns = ['document_id', 'avg_syllables']

more_stats = doc_stats.join(avg_syllables.set_index('document_id'), on=doc_stats.index, how='inner').drop('key_0', axis=1)
more_stats.to_csv('data_out/stats.csv', index=True)

