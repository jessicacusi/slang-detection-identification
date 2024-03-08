import argparse
import pandas as pd
from openai import OpenAI
import stanza


def generate_random_sentences(num_choices):
    """
        Generate sentences using GPT-3.5 where the term is used in its literal sense. Exports sentences to a text file.

        Args:
            num_choices (int): Number of choices to generate.
    """

    client = OpenAI()

    # Generate sentences using GPT-3.5's chat completions
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "text"},
        messages=[
            {"role": "system", "content": f"From now on, act as an human adult. Imagine you're conversing with your friends. 
             Provide 10 individual sentences that a person your age would say, where each sentence must be different. 
             It can be about any topic. However, make sure not to include any of the following words in your sentences: 
             cap, drip, extra, shook, salty, mid, and lit."
}
        ],
        n=num_choices,
        frequency_penalty=1.0,
    )

    # Extract text content from all choices
    outputs = [choice.message.content for choice in completion.choices]


    # Save to file
    output_file = f'random_sentences_adult2.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        for sentence in outputs:
            file.write(sentence + '\n')

    print("Output saved to", output_file)


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
parser.add_argument("-n", "--num_choices", type=int, default=9, help="Number of outputs to generate. Default is 9.")

args = parser.parse_args()
generate_random_sentences(args.num_choices)
sentence_parser(args.term)
