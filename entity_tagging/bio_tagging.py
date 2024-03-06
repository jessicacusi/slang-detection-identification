# Adapted from: https://medium.com/thecyphy/training-custom-ner-model-using-flair-df1f9ea9c762
# Description: This script takes the csv file with the text and annotations and creates a txt file with BIO-tagged text
# Note: may create extra entities that are not B-SLANG or B-LITERAL -- manual check is needed
# Input: csv file with columns 'text' and 'annotation' where 'annotation' is a list of tuples (from create_slang_ner.py)
# Output: txt file with BIO-tagged text

import pandas as pd
from tqdm import tqdm
from difflib import SequenceMatcher
import ast

def matcher(string, pattern):
    match_list = []
    pattern = pattern.strip()
    seqMatch = SequenceMatcher(None, string, pattern, autojunk=False)
    match = seqMatch.find_longest_match(0, len(string), 0, len(pattern))
    if match.size == len(pattern):
        start = match.a
        end = match.a + match.size
        match_tup = (start, end)
        string = string.replace(pattern, "X" * len(pattern), 1)
        match_list.append(match_tup)

    return match_list, string

def mark_sentence(s, match_list):
    word_dict = {}
    for word in s.split():
        word_dict[word] = 'O'

    for start, end, e_type in match_list:
        temp_str = s[start:end]
        tmp_list = temp_str.split()
        if len(tmp_list) > 1:
            word_dict[tmp_list[0]] = 'B-' + e_type
            for w in tmp_list[1:]:
                word_dict[w] = 'I-' + e_type
        else:
            word_dict[temp_str] = 'B-' + e_type
    return word_dict

def clean(text):
    filters = ["!", "#", "$", "%", "&", "(", ")", "/", "*", ".", ":", ";", "<", "=", ">", "?", "@", "[",
               "\\", "]", "_", "`", "{", "}", "~", "'"]
    for i in text:
        if i in filters:
            text = text.replace(i, " " + i)

    return text

def create_data(df, filepath):
    with open(filepath, 'w') as f:
        for text, annotation in zip(df.text, df.annotation):
            text = clean(text)
            text_ = text
            match_list = []
            for i in annotation:
                a, text_ = matcher(text, i[0])
                if a:  # Check if match_list is not empty
                    match_list.append((a[0][0], a[0][1], i[1]))

            d = mark_sentence(text, match_list)

            for i in d.keys():
                f.writelines(i + ' ' + d[i] + '\n')
            f.writelines('\n')
            
def main():

    def create_files(set_name):
        slang_data = pd.read_csv(f'full_ner_{set_name}.csv')
        slang_data = slang_data[['text', 'annotation']]
        slang_data['annotation'] = slang_data['annotation'].apply(ast.literal_eval)
        slang_filepath = f'full_bio_{set_name}.txt'
        create_data(slang_data, slang_filepath)
        print(f"{set_name} file created")
        print(slang_data.shape)

    create_files('train')
    create_files('test')
    create_files('dev')

if __name__ == '__main__':
    main()