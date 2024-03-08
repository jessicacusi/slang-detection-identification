# Create entity tag annotations for slang words to tag them as slang or literal
# Input: CSV file with 'text' and 'label' columns ('term' column is optional)
# Output: CSV file with 'text', 'annotation' columns

import pandas as pd
import numpy as np
import re
import string

# Path to file with term, text, and label columns
data = 'path/to/file.csv'

# Full data
facts = pd.read_csv(data,encoding='utf-8')
print(facts.shape)

# Split data into slang + literal uses
slang_df = facts[facts['label'] == 1][['text']]
literal_df = facts[facts['label'] == 0][['text']]
print(slang_df.shape)
print(literal_df.shape)

# List of terms
hybrid_list = ['cap', 'drip', 'extra', 'lit', 'mid', 'salty', 'shook']
# slang_only_list = ['bussin','finna','simp',r'\bsus\b','turnt'] # for tagging slang-only words

# Calculate the term index for each row
term_index = np.repeat(range(len(hybrid_list)), 500)[:3500]
# term_index = np.repeat(range(len(slang_only_list)), 300)[:1500] # for tagging slang-only words


# Add the 'Term' column to the DataFrame
slang_df['Term'] = [hybrid_list[idx] for idx in term_index]
literal_df['Term'] = [hybrid_list[idx] for idx in term_index]

print(slang_df.head())
print(literal_df.tail())

# Function to check if any word in the list is present and update 'annotation' column
def update_annotation(row, word_type):
    """
    Check if any word in the hybrid_list is present in the row['text'] and update the 'annotation' column.
    """
    for word in hybrid_list:
        if re.search(word, row['text'].lower()):
            words = row['text'].split()
            for idx, token in enumerate(words):
                cleaned_token = token.lower().strip(string.punctuation)
                if re.search(word, cleaned_token):
                    return (cleaned_token, word_type)
    return None

slang_df['annotation'] = slang_df.apply(update_annotation, axis=1, word_type='SLANG')

slang_df = slang_df.dropna(subset=['annotation'])
print(slang_df.shape)

literal_df['annotation'] = literal_df.apply(update_annotation, axis=1, word_type='LITERAL')

print(slang_df.head())
print(literal_df.tail())

slang_export = slang_df[['text', 'annotation']]
literal_export = literal_df[['text', 'annotation']]

slang_export.to_csv('slang_ner_annotations.csv', index=False,encoding='utf-8')
literal_export.to_csv('literal_ner_annotations.csv', index=False,encoding='utf-8')