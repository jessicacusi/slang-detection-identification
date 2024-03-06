import argparse
import stanza
import pandas as pd
from openai import OpenAI

def generate_slang_sentences(term, slang_def, num_choices):
    """
        Generate sentences using GPT-3.5 where the term is used in its slang sense. Exports sentences to a text file.

        Args:
            term (str): Term you'd like to generate sentences for.
            slang_def (str): Slang definition for term.
            num_choices (int): Number of choices to generate.
    """

    client = OpenAI()

    # Generate sentences using GPT-3.5's chat completions
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "text"},
        messages=[
            {"role": "system", "content": f"From now on, act as a high school or college student between the ages 15 and 21. 
             Imagine you’re conversing with your friends. Provide 10 sentences that a person your age would say, where each 
             sentence must include the word “{term}” where “{term}” is used in its slang form where it means {slang_def}."}
        ],
        n=num_choices,
        frequency_penalty=1.0,
    )

    # Extract text content from all choices
    outputs = [choice.message.content for choice in completion.choices]


    # Save to file
    slang_output_file = f'{term}_slang_sentences.txt'
    with open(slang_output_file, 'w', encoding='utf-8') as file:
        for sentence in outputs:
            file.write(sentence + '\n')

    print("Output saved to", slang_output_file)

def sentence_parser(term):
    """
        Parses sentences using stanza and exports them to a text file.
    """
    # stanza.download('en')
    print(term)
    nlp = stanza.Pipeline('en')

    # slang sentences
    slang_f = open(f"{term}_slang_sentences.txt", "r")
    text = slang_f.read()

    doc = nlp(text)
    sentences_list = [sentence.text for sentence in doc.sentences]

    # save data into DF and export into text file
    slang_df = pd.DataFrame({"Sentence": sentences_list})
    slang_output_file_path = f"{term}_slang_sentences_parsed.txt"
    slang_df.to_csv(slang_output_file_path, index=False)

    print(f"Slang text file has been created: {slang_output_file_path}")


# Parse arguments
parser = argparse.ArgumentParser(description="Generate sentences using GPT-3.5.")
parser.add_argument("-t", "--term", required=True, help="Term you'd like to generate sentences for.")
parser.add_argument("-y", "--slang_def", required=True, help="Slang definition for term.")
parser.add_argument("-n", "--num_choices", type=int, default=9, help="Number of outputs to generate. Default is 9.")

args = parser.parse_args()

generate_slang_sentences(args.term, args.slang_def, args.num_choices)
sentence_parser(args.term)